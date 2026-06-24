#!/usr/bin/env python3
"""
dispatch.py — CJaC Validation Dispatcher (Level 2)
====================================================
Picks one job from queue/, launches it, then moves it to done/ or failed/.

Called by launchd on schedule — Andy does NOT launch this manually after setup.

JOB TYPES
---------
1. Protocol jobs (holdings validation via run_protocol.py):
    {
        "job_id": "job_20260624_0215_abc123",
        "protocol": "retaliation_holdings_v3",
        "states": "AZ,DC,IA,KY,...",
        "sleep": 10,
        "fresh": false,
        "created": "2026-06-24T02:00:00Z",
        "note": "Batch 1"
    }

2. L2 module jobs (L2 multi-model runners, e.g. l2_procedural_defects_runner):
    {
        "job_id": "job_20260625_0215_l2_proc",
        "job_type": "l2_module",
        "runner": "rules/validation/l2/l2_procedural_defects_runner.py",
        "states": "AK,AL,AR,...",   (comma-separated, or "ALL")
        "defects": "premature,court,attach,summons",   (or omit for all)
        "sleep": 2,
        "created": "2026-06-24T22:00:00Z",
        "note": "Full 51-state procedural defects run"
    }

Cowork drops job files in queue/. Dispatcher picks one per fire (to keep
nights bounded). Done jobs move to done/ with completion info added.

Directory layout (all under rules/validation/):
    queue/     ← Cowork drops .json job files here
    done/      ← Completed jobs
    failed/    ← Failed jobs
    results/   ← SUMMARY_*.md files (from protocol jobs)
    logs/      ← log files
    l2/output/ ← L2 runner output JSON files
    .checkpoints/ ← Checkpoint files (harness resume)

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_VAL_ROOT = Path(__file__).parent
QUEUE_DIR  = _VAL_ROOT / "queue"
DONE_DIR   = _VAL_ROOT / "done"
FAILED_DIR = _VAL_ROOT / "failed"
RESULTS_DIR = _VAL_ROOT / "results"
LOG_DIR    = _VAL_ROOT / "logs"

RUNNER = _VAL_ROOT / "run_protocol.py"
PYTHON  = sys.executable  # same interpreter that launched dispatch.py

ALL_STATES = (
    "AK,AL,AR,AZ,CA,CO,CT,DC,DE,FL,GA,HI,IA,ID,IL,IN,KS,KY,LA,MA,"
    "MD,ME,MI,MN,MO,MS,MT,NC,ND,NE,NH,NJ,NM,NV,NY,OH,OK,OR,PA,RI,"
    "SC,SD,TN,TX,UT,VA,VT,WA,WI,WV,WY"
)


def pick_next_job() -> Path | None:
    """Return the oldest .json job file in queue/, or None if empty."""
    jobs = sorted(QUEUE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
    return jobs[0] if jobs else None


def load_job(job_path: Path) -> dict:
    with open(job_path) as f:
        return json.load(f)


def run_job(job: dict) -> tuple[bool, str]:
    """
    Dispatch a job based on its job_type.
    Returns (success: bool, message: str).
    """
    job_type = job.get("job_type", "protocol")
    if job_type == "l2_module":
        return run_l2_module_job(job)
    else:
        return run_protocol_job(job)


def run_protocol_job(job: dict) -> tuple[bool, str]:
    """
    Launch run_protocol.py for a holdings/protocol job.
    `caffeinate -ims` keeps Mac awake for the duration.
    """
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    log_path = LOG_DIR / f"dispatch_{job['protocol']}_{ts}.log"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

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

    return _run_subprocess(cmd, log_path, job)


def run_l2_module_job(job: dict) -> tuple[bool, str]:
    """
    Launch an L2 module runner (e.g. l2_procedural_defects_runner.py).
    Job fields:
      runner   — path relative to repo root (e.g. rules/validation/l2/l2_procedural_defects_runner.py)
      states   — comma-separated state codes, or "ALL"
      defects  — comma-separated defect keys (optional; omit for all)
      sleep    — seconds between API calls (default 2)
    """
    repo_root = _VAL_ROOT.parent.parent
    runner_path = repo_root / job["runner"]

    if not runner_path.exists():
        return False, f"Runner not found: {runner_path}"

    states = job.get("states", "ALL")
    if states.upper() == "ALL":
        states = ALL_STATES

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    runner_name = Path(job["runner"]).stem
    log_path = LOG_DIR / f"dispatch_{runner_name}_{ts}.log"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        "caffeinate", "-ims",
        PYTHON, str(runner_path),
        "--states", states,
        "--sleep",  str(job.get("sleep", 2)),
    ]
    if job.get("defects"):
        cmd += ["--defects", job["defects"]]

    return _run_subprocess(cmd, log_path, job)


def _run_subprocess(cmd: list, log_path: Path, job: dict) -> tuple[bool, str]:
    """Shared subprocess runner with caffeinate fallback."""
    print(f"[dispatch] Launching: {' '.join(str(c) for c in cmd)}", flush=True)
    print(f"[dispatch] Log: {log_path}", flush=True)

    repo_root = _VAL_ROOT.parent.parent

    with open(log_path, "w") as log_f:
        log_f.write(f"# Dispatched: {datetime.now(timezone.utc).isoformat()}\n")
        log_f.write(f"# Job: {json.dumps(job)}\n\n")
        log_f.flush()

        try:
            result = subprocess.run(
                cmd,
                stdout=log_f,
                stderr=subprocess.STDOUT,
                cwd=str(repo_root),
            )
        except FileNotFoundError:
            cmd_no_caf = cmd[2:]  # strip caffeinate -ims
            result = subprocess.run(
                cmd_no_caf,
                stdout=log_f,
                stderr=subprocess.STDOUT,
                cwd=str(repo_root),
            )

    success = result.returncode == 0
    message = f"Completed with returncode={result.returncode}. Log: {log_path}"
    return success, message


def move_job(job_path: Path, dest_dir: Path, extra_fields: dict):
    """Load job JSON, add extra_fields, write to dest_dir, remove from queue."""
    job = load_job(job_path)
    job.update(extra_fields)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / job_path.name
    with open(dest_path, "w") as f:
        json.dump(job, f, indent=2)
    job_path.unlink()
    return dest_path


def find_latest_summary(protocol: str) -> str | None:
    """Find the most-recently-written SUMMARY for this protocol."""
    summaries = sorted(RESULTS_DIR.glob(f"SUMMARY_{protocol}_*.md"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
    return str(summaries[0]) if summaries else None


def main():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    job_path = pick_next_job()
    if not job_path:
        print("[dispatch] Queue is empty — nothing to do.")
        return

    job = load_job(job_path)
    print(f"[dispatch] Starting job: {job.get('job_id','?')} — "
          f"{job.get('protocol')} / {job.get('states','?')[:60]}")

    success, message = run_job(job)

    if success:
        summary_path = find_latest_summary(job.get("protocol", ""))
        dest = move_job(job_path, DONE_DIR, {
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "result": "success",
            "message": message,
            "summary_path": summary_path,
        })
        print(f"[dispatch] ✅ Job succeeded → {dest}")
        if summary_path:
            print(f"[dispatch] Summary: {summary_path}")
    else:
        dest = move_job(job_path, FAILED_DIR, {
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "result": "failure",
            "message": message,
        })
        print(f"[dispatch] ❌ Job failed → {dest}")
        print(f"[dispatch] Check logs in {LOG_DIR}/")
        sys.exit(1)


if __name__ == "__main__":
    main()
