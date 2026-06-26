#!/usr/bin/env python3
"""
dispatch.py — CJaC Validation Dispatcher (Direction A Rev 2)
=============================================================
Continuous queue-draining dispatcher with parallel execution of independent jobs.

CHANGES FROM REV 1:
- Continuous drain: runs until queue is empty, then exits. Intended to be called
  by a tight loop (launchd every 5 min, or Cowork-run loop) rather than once/night.
- Parallel execution: independent jobs run concurrently (via subprocess).
  Dependency defined by `uses` resource tag — two jobs sharing a rate-limited
  resource (e.g. `courtlistener`) are serialized; otherwise parallelized.
- Max concurrency: 3 simultaneous jobs; only 1 CourtListener-bound job at a time.
- Resource tags in job JSON: `uses: ["courtlistener"]` / `uses: ["openai","gemini"]`
  / `uses: []`. Missing `uses` defaults to `["openai","gemini"]` (most runners).
- Live-run-before-queue (Change 3): jobs with `live_verified: false` are skipped
  with a warning until Cowork sets `live_verified: true` after a confirmed live run.
- Heartbeat: writes `logs/heartbeat.json` on every cycle so monitoring can detect stalls.
- Self-monitoring: if a job crashes, surfaces it immediately rather than silently
  waiting for the next scheduled fire.

JOB SCHEMA (all fields except job_id are optional unless noted):
  {
    "job_id": "unique-id",           # required
    "job_type": "protocol",          # "protocol" (default) or "l2_module"
    "protocol": "...",               # required for protocol jobs
    "runner": "path/to/runner.py",   # required for l2_module jobs
    "states": "AK,AL,...",           # required
    "sleep": 10,
    "fresh": false,
    "uses": ["openai", "gemini"],    # resource tags; omit = default to ["openai","gemini"]
    "live_verified": true,           # Change 3: must be true or job is skipped
    "created": "ISO8601",
    "note": "..."
  }

Directory layout (all under rules/validation/):
    queue/     ← job files dropped here
    done/      ← completed jobs
    failed/    ← failed jobs
    results/   ← SUMMARY_*.md files
    logs/      ← dispatch logs + heartbeat.json
    l2/output/ ← L2 runner output JSON

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

_VAL_ROOT = Path(__file__).parent
QUEUE_DIR   = _VAL_ROOT / "queue"
DONE_DIR    = _VAL_ROOT / "done"
FAILED_DIR  = _VAL_ROOT / "failed"
RESULTS_DIR = _VAL_ROOT / "results"
LOG_DIR     = _VAL_ROOT / "logs"

RUNNER      = _VAL_ROOT / "run_protocol.py"
PYTHON      = sys.executable

# --- Concurrency limits (Direction A Rev 2 Change 2) ---
MAX_CONCURRENT_JOBS     = 3
MAX_CONCURRENT_PER_RESOURCE: Dict[str, int] = {
    "courtlistener": 1,   # rate-limited; only 1 CL job at a time
    "openai":        2,   # generous but cap to avoid thrash
    "gemini":        2,
}

ALL_STATES = (
    "AK,AL,AR,AZ,CA,CO,CT,DC,DE,FL,GA,HI,IA,ID,IL,IN,KS,KY,LA,MA,"
    "MD,ME,MI,MN,MO,MS,MT,NC,ND,NE,NH,NJ,NM,NV,NY,OH,OK,OR,PA,RI,"
    "SC,SD,TN,TX,UT,VA,VT,WA,WI,WV,WY"
)

# ---------------------------------------------------------------------------
# Job file helpers
# ---------------------------------------------------------------------------

def pick_eligible_jobs(running_resources: Set[str]) -> List[Tuple[Path, dict]]:
    """
    Return all jobs from queue/ that are eligible to start now, given the set
    of resources currently in use by running jobs.

    Eligibility rules:
    1. live_verified must be true (or absent from old-schema jobs with a warning).
    2. The job's `uses` resources must not exceed per-resource concurrency limits
       when combined with `running_resources`.
    3. Total running jobs must be < MAX_CONCURRENT_JOBS.
    """
    jobs = sorted(QUEUE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
    eligible = []

    # Count current usage per resource
    resource_counts: Dict[str, int] = {}
    for r in running_resources:
        resource_counts[r] = resource_counts.get(r, 0) + 1

    for job_path in jobs:
        if job_path.name.startswith(".") or job_path.suffix != ".json":
            continue
        if job_path.name == "SAMPLE_JOB_FORMAT.json.example":
            continue
        try:
            job = load_job(job_path)
        except Exception as e:
            print(f"[dispatch] ⚠️  Could not load {job_path.name}: {e}", flush=True)
            continue

        # Change 3: live_verified gate
        if not job.get("live_verified", False):
            print(
                f"[dispatch] ⏭  Skipping {job.get('job_id','?')} — live_verified=false. "
                "Run it once from Terminal and set live_verified=true before queuing for unattended execution.",
                flush=True,
            )
            continue

        # Resource check
        job_uses = _job_resources(job)
        conflict = False
        for resource in job_uses:
            limit = MAX_CONCURRENT_PER_RESOURCE.get(resource, MAX_CONCURRENT_JOBS)
            current = resource_counts.get(resource, 0)
            if current >= limit:
                print(
                    f"[dispatch] ⏳  Deferring {job.get('job_id','?')} — "
                    f"resource '{resource}' at limit ({current}/{limit})",
                    flush=True,
                )
                conflict = True
                break
        if not conflict:
            eligible.append((job_path, job))

    return eligible


def _job_resources(job: dict) -> List[str]:
    """Return the resource list for a job, with a sensible default."""
    uses = job.get("uses")
    if uses is None:
        # Legacy jobs without a uses tag: assume openai+gemini
        job_type = job.get("job_type", "protocol")
        if "courtlistener" in job.get("protocol", "") or "holdings_v" in job.get("protocol", ""):
            return ["courtlistener", "openai", "gemini"]
        return ["openai", "gemini"]
    return list(uses)


def load_job(job_path: Path) -> dict:
    with open(job_path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Job runners
# ---------------------------------------------------------------------------

def launch_job(job_path: Path, job: dict) -> subprocess.Popen:
    """
    Launch a job as a background subprocess. Returns the Popen handle.
    The caller is responsible for waiting and moving to done/failed.
    """
    job_type = job.get("job_type", "protocol")
    if job_type == "l2_module":
        cmd = _build_l2_cmd(job)
    else:
        cmd = _build_protocol_cmd(job)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    protocol_or_runner = job.get("protocol") or Path(job.get("runner", "l2_module")).stem
    log_path = LOG_DIR / f"dispatch_{protocol_or_runner}_{ts}.log"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    repo_root = _VAL_ROOT.parent.parent

    print(f"[dispatch] 🚀 Launching: {job.get('job_id','?')} | cmd: {' '.join(str(c) for c in cmd[:5])}...", flush=True)
    print(f"[dispatch]    Log: {log_path}", flush=True)

    log_f = open(log_path, "w")
    log_f.write(f"# Dispatched: {datetime.now(timezone.utc).isoformat()}\n")
    log_f.write(f"# Job: {json.dumps(job)}\n\n")
    log_f.flush()

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            cwd=str(repo_root),
        )
    except FileNotFoundError:
        # caffeinate not available (Linux/sandbox)
        cmd_no_caf = [c for c in cmd if c not in ("caffeinate", "-ims")]
        proc = subprocess.Popen(
            cmd_no_caf,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            cwd=str(repo_root),
        )

    proc._log_f = log_f          # keep file handle alive with proc
    proc._log_path = log_path
    proc._job_path = job_path
    proc._job = job
    return proc


def _build_protocol_cmd(job: dict) -> List:
    cmd = [
        "caffeinate", "-ims",
        PYTHON, str(RUNNER),
        "--protocol", job["protocol"],
        "--states",   job["states"],
        "--sleep",    str(job.get("sleep", 10)),
    ]
    if job.get("fresh"):
        cmd.append("--fresh")
    if job.get("run_id"):
        cmd += ["--run-id", job["run_id"]]
    return cmd


def _build_l2_cmd(job: dict) -> List:
    repo_root = _VAL_ROOT.parent.parent
    runner_path = repo_root / job["runner"]
    states = job.get("states", "ALL")
    if states.upper() == "ALL":
        states = ALL_STATES
    cmd = [
        "caffeinate", "-ims",
        PYTHON, str(runner_path),
        "--states", states,
        "--sleep",  str(job.get("sleep", 2)),
    ]
    if job.get("defects"):
        cmd += ["--defects", job["defects"]]
    return cmd


def finalize_job(proc: subprocess.Popen):
    """Move the job to done/ or failed/ after proc exits."""
    job = proc._job
    job_path = proc._job_path
    proc._log_f.close()

    success = proc.returncode == 0
    summary_path = _find_latest_summary(job.get("protocol", ""))
    dest_dir = DONE_DIR if success else FAILED_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)

    extra = {
        "completed_at" if success else "failed_at": datetime.now(timezone.utc).isoformat(),
        "result": "success" if success else "failure",
        "message": f"returncode={proc.returncode}. Log: {proc._log_path}",
        "summary_path": summary_path,
    }
    job_data = load_job(job_path)
    job_data.update(extra)
    dest_path = dest_dir / job_path.name
    with open(dest_path, "w") as f:
        json.dump(job_data, f, indent=2)
    job_path.unlink()

    icon = "✅" if success else "❌"
    print(f"[dispatch] {icon} {job.get('job_id','?')} → {dest_path}", flush=True)
    return success


def _find_latest_summary(protocol: str) -> Optional[str]:
    if not protocol:
        return None
    summaries = sorted(
        RESULTS_DIR.glob(f"SUMMARY_{protocol}_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return str(summaries[0]) if summaries else None


# ---------------------------------------------------------------------------
# Heartbeat (Change 4 — monitoring)
# ---------------------------------------------------------------------------

def write_heartbeat(running: List, completed: int, skipped: int):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    heartbeat = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "running_jobs": [p._job.get("job_id", "?") for p in running],
        "completed_this_cycle": completed,
        "skipped_live_verify": skipped,
        "queue_depth": len(list(QUEUE_DIR.glob("*.json"))) - 1,  # subtract .gitkeep
    }
    with open(LOG_DIR / "heartbeat.json", "w") as f:
        json.dump(heartbeat, f, indent=2)


# ---------------------------------------------------------------------------
# Main drain loop
# ---------------------------------------------------------------------------

def drain():
    """
    Drain the queue continuously until empty or no eligible jobs remain.
    Intended to be called by a tight external loop (every few minutes).
    """
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    running: List[subprocess.Popen] = []
    completed_count = 0
    skipped_count = 0

    print(f"[dispatch] ▶  drain() start {datetime.now(timezone.utc).isoformat()}", flush=True)

    while True:
        # --- Reap finished processes ---
        still_running = []
        for proc in running:
            ret = proc.poll()
            if ret is not None:
                finalize_job(proc)
                completed_count += 1
            else:
                still_running.append(proc)
        running = still_running

        # --- Collect resources currently in use ---
        running_resources: Set[str] = set()
        for proc in running:
            for r in _job_resources(proc._job):
                running_resources.add(r)

        # --- Check capacity ---
        if len(running) >= MAX_CONCURRENT_JOBS:
            write_heartbeat(running, completed_count, skipped_count)
            time.sleep(5)
            continue

        # --- Pick eligible jobs ---
        eligible = pick_eligible_jobs(running_resources)

        if not eligible and not running:
            # Queue drained
            write_heartbeat(running, completed_count, skipped_count)
            print(
                f"[dispatch] ✔  Queue drained. "
                f"Completed: {completed_count}. Skipped (live_verified=false): {skipped_count}.",
                flush=True,
            )
            return

        if not eligible:
            # Running jobs are consuming all capacity; wait for one to finish
            write_heartbeat(running, completed_count, skipped_count)
            time.sleep(5)
            continue

        # --- Launch as many eligible jobs as capacity allows ---
        slots = MAX_CONCURRENT_JOBS - len(running)
        to_launch = eligible[:slots]

        for job_path, job in to_launch:
            # Re-check resources (could have filled up in this batch)
            for r in _job_resources(job):
                running_resources.add(r)
            proc = launch_job(job_path, job)
            running.append(proc)

        write_heartbeat(running, completed_count, skipped_count)
        time.sleep(2)


# ---------------------------------------------------------------------------
# CLI: single-shot legacy mode (for launchd safety-net fires)
# ---------------------------------------------------------------------------

def main_single():
    """
    Single-shot mode: pick ONE eligible job, run it synchronously, exit.
    Used as safety-net for launchd scheduled fires.
    """
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    eligible = pick_eligible_jobs(set())
    if not eligible:
        print("[dispatch] Queue is empty or no eligible jobs — nothing to do.", flush=True)
        return

    job_path, job = eligible[0]
    print(f"[dispatch] Single-shot: {job.get('job_id','?')}", flush=True)
    proc = launch_job(job_path, job)
    proc.wait()
    success = finalize_job(proc)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CJaC Validation Dispatcher")
    parser.add_argument(
        "--drain",
        action="store_true",
        default=False,
        help="Drain the full queue (parallel, continuous). Default: single-shot legacy mode.",
    )
    args = parser.parse_args()

    if args.drain:
        drain()
    else:
        main_single()
