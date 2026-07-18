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

CHANGES (2026-07-16 directive — Dispatcher Resilience & Overnight-Environment
Forensics, Part B, items B-1/B-2/B-3): the launchd single-shot path
(main_single, the one launchd actually fires nightly) is now self-evidencing.
Previously a missed launchd fire was distinguishable from a fired-and-idled
night only by the *absence* of a log line — forensic guesswork. Now every
invocation of main_single() appends to an append-only
`logs/dispatcher_heartbeat.log` (JSONL, one event per line):
  1. LOADED            — proof launchd ran this process at all (first statement).
  2. FIRED              — scheduled-vs-actual delta (a `FIRED` at 7:04 AM with
                           delta +4h49m against the 02:15 schedule IS the sleep
                           diagnosis — launchd coalesces a missed
                           StartCalendarInterval fire onto the next wake).
  3. PREFLIGHT_DNS       — B-2: DNS resolution OK/FAIL+errno for the three
                           endpoints this repo depends on (CourtListener,
                           Gemini, OpenAI), logged on every fire at zero
                           marginal cost — turns every night into a DNS data
                           point for the overnight-environment RED.
  4. exactly one terminal outcome — IDLED-EMPTY-QUEUE / COMPLETED-RUN /
     ABORTED. Wrapped in try/except/finally so an uncaught exception still
     writes ABORTED rather than leaving the cycle silently unresolved.
classify_last_night() (B-3) reads this log and reports one of exactly four
states for "last night": no-heartbeat, fired-and-idled, fired-and-ran,
fired-late-on-wake — see that function's docstring. Invoke via
`python3 dispatch.py --heartbeat-status` (read-only, prints JSON) for the
morning report to consume instead of inferring from log absence.

This is separate from write_heartbeat()'s existing `logs/heartbeat.json`
snapshot (Change 4, below), which is a --drain-mode stall-detection
mechanism polled every cycle; that mechanism is untouched by this change.

JOB SCHEMA (all fields except job_id are optional unless noted):
  {
    "job_id": "unique-id",           # required
    "job_type": "protocol",          # "protocol" (default), "l2_module", or "scorer"
    "protocol": "...",               # required for protocol jobs
    "runner": "path/to/runner.py",   # required for l2_module jobs; naming hint for scorer jobs
    "states": "AK,AL,...",           # required for protocol/l2_module jobs
    "sleep": 10,
    "fresh": false,
    "force": false,                  # scorer jobs only: bypass time-window/cadence guards
    "dry_run": false,                # scorer jobs only: mocked predictions, no API calls
    "uses": ["openai", "gemini"],    # resource tags; omit = default to ["openai","gemini"]
    "live_verified": true,           # Change 3: must be true or job is skipped
    "created": "ISO8601",
    "note": "..."
  }

  scorer jobs (Item 13, Direction D-1, added 2026-07-15):
    Runs rules/validation/scorer/dev_set_monitor.py, which self-throttles on
    both a daytime/evening time window (avoids the overnight Gemini-endpoint
    DNS RED) and a 3-day cadence — safe to queue for frequent dispatcher
    drain cycles; it defers itself rather than trusting external cron timing.
    Scores the v0.2 dev split ONLY (non-held-out); never touches the held-out
    set or any rules file.

Directory layout (all under rules/validation/):
    queue/     ← job files dropped here
    done/      ← completed jobs
    failed/    ← failed jobs
    results/   ← SUMMARY_*.md files
    logs/      ← dispatch logs + heartbeat.json + dispatcher_heartbeat.log
    l2/output/ ← L2 runner output JSON

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

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
    elif job_type == "scorer":
        cmd = _build_scorer_cmd(job)
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


def _build_scorer_cmd(job: dict) -> List:
    """Item 13 (2026-07-15): Direction D-1 dev-set monitor. No --states — the
    scorer works off the frozen golden-set file, not a state list. The script
    itself enforces the daytime-window and 3-day-cadence guardrails, so it is
    safe for the dispatcher to attempt this job on every drain cycle; it will
    self-defer (exit 0, no scoring, no writes) when it is not yet due."""
    script_path = _VAL_ROOT / "scorer" / "dev_set_monitor.py"
    cmd = ["caffeinate", "-ims", PYTHON, str(script_path)]
    if job.get("force"):
        cmd.append("--force")
    if job.get("dry_run"):
        cmd.append("--dry-run")
    cmd += ["--sleep", str(job.get("sleep", 2))]
    return cmd


def finalize_job(proc: subprocess.Popen):
    """Move the job to done/ or failed/ after proc exits -- UNLESS the job is
    marked `"recurring": true` (added 2026-07-18, alongside the noon
    dispatcher fire), in which case it stays in queue/ untouched.

    Why: a one-shot job (protocol/l2_module run) genuinely completes and
    should leave the queue. A recurring job (e.g. Item 13's dev-set monitor,
    `job_dev_set_monitor_20260715.json`) is a *standing* descriptor whose own
    script self-throttles on a time-window/cadence and legitimately exits 0
    on nights/slots it declines to do real work -- that is not "done", it's
    "checked in and deferred". Before this fix, finalize_job() could not
    tell the difference: any exit 0, including a silent self-defer, would
    unlink() the job file from queue/ after its very first dispatcher
    pickup, permanently breaking the job's cadence (it would never be
    reconsidered again without a human manually re-dropping the file).
    Discovered while wiring the second daytime fire, since the dispatcher had
    never yet successfully picked up the scorer job to expose the bug.
    """
    job = proc._job
    job_path = proc._job_path
    proc._log_f.close()

    success = proc.returncode == 0

    if job.get("recurring", False):
        icon = "✅" if success else "❌"
        print(
            f"[dispatch] {icon} {job.get('job_id','?')} (recurring — staying in queue/, "
            f"returncode={proc.returncode})",
            flush=True,
        )
        return success

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
# Heartbeat (Change 4 — monitoring; --drain-mode stall detection)
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
# Self-evidencing dispatcher forensics (2026-07-16 directive, B-1/B-2/B-3)
# ---------------------------------------------------------------------------

HEARTBEAT_LOG = LOG_DIR / "dispatcher_heartbeat.log"

# Mirrors com.cjac.validation.plist's StartCalendarInterval entries (local
# time — the plist does not pin a timezone, and the machine's local tz is
# what launchd actually uses; Pacific matches this repo's other
# timezone-aware component, dev_set_monitor.py). Two fire times as of
# 2026-07-18: the original 02:15 overnight safety-net fire, plus a 12:00
# daytime fire added specifically to give Item 13's dev-set monitor (which
# self-throttles to a 09:00-23:00 window) an automatic driver -- the
# overnight fire alone can never satisfy that window. Keep this list in sync
# with the plist's StartCalendarInterval array.
DISPATCH_TZ_NAME = "America/Los_Angeles"
SCHEDULED_TIMES = [(2, 15), (12, 0)]  # (hour, minute) pairs, 24h local time

# A FIRED delta beyond this is classified "fired-late-on-wake" (launchd
# coalesced a missed StartCalendarInterval fire onto the next wake) rather
# than ordinary scheduling jitter.
LATE_THRESHOLD_SECONDS = 30 * 60

# B-2: the three endpoints this repo's overnight jobs depend on.
PREFLIGHT_ENDPOINTS: Dict[str, str] = {
    "courtlistener": "www.courtlistener.com",
    "gemini": "generativelanguage.googleapis.com",
    "openai": "api.openai.com",
}

# How far back "last night" counts as, when classify_last_night() looks for
# the most recent LOADED entry. Generously wide (covers a late-morning
# heartbeat-status check the day after a very-late-on-wake fire).
HEARTBEAT_LOOKBACK_HOURS = 30


def _append_heartbeat(event: str, **fields) -> dict:
    """B-1: append one line to the self-evidencing dispatcher heartbeat log.

    Separate from write_heartbeat()'s JSON snapshot above (that one is a
    --drain-mode stall-detection mechanism, overwritten each cycle). This one
    is append-only and exists specifically so a missed launchd fire is
    distinguishable from 'I ran and found nothing to do' or 'I ran and
    something broke' by direct evidence, not by the absence of a log line.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry: Dict = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "pid": os.getpid(),
    }
    entry.update(fields)
    with open(HEARTBEAT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def _scheduled_fire_time_utc(now_utc: datetime) -> Optional[datetime]:
    """Best-effort reconstruction of the most recent scheduled fire time
    (per com.cjac.validation.plist's SCHEDULED_TIMES), for computing the
    FIRED delta -- i.e. whichever of today's (or, before the first slot of
    the day, yesterday's) scheduled fire times is most recently in the past
    relative to `now_utc`.

    This matters with two fire times: a naive "always compare against 02:15"
    would misreport every noon fire as wildly late (~10h delta against a
    02:15 baseline). Picking the nearest-preceding slot keeps the delta
    meaningful for both fires independently.

    Returns None if zoneinfo is unavailable — the delta is then omitted
    rather than fabricated from a guessed offset.
    """
    if ZoneInfo is None:  # pragma: no cover
        return None
    tz = ZoneInfo(DISPATCH_TZ_NAME)
    now_local = now_utc.astimezone(tz)

    candidates = []
    for day_offset in (0, -1):
        base = now_local + timedelta(days=day_offset)
        for hour, minute in SCHEDULED_TIMES:
            candidate = base.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if candidate <= now_local:
                candidates.append(candidate)

    if not candidates:  # pragma: no cover (only if now_local < every slot, incl. yesterday's)
        return None
    return max(candidates).astimezone(timezone.utc)


def _preflight_dns_probe(timeout: float = 5.0) -> Dict[str, dict]:
    """B-2: resolve DNS for the three endpoints this dispatcher's jobs depend
    on. Cheap (resolution only, no payload) and logged on every fire, turning
    every future night into a DNS data point for the overnight-environment
    RED at zero marginal cost — replacing the need for run-level forensics
    like run 9ae49b97's after-the-fact reconstruction.
    """
    results: Dict[str, dict] = {}
    prev_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        for name, host in PREFLIGHT_ENDPOINTS.items():
            try:
                ip = socket.gethostbyname(host)
                results[name] = {"host": host, "ok": True, "ip": ip}
            except OSError as e:
                results[name] = {
                    "host": host,
                    "ok": False,
                    "errno": getattr(e, "errno", None),
                    "error": str(e),
                }
    finally:
        socket.setdefaulttimeout(prev_timeout)
    return results


def classify_last_night(now_utc: Optional[datetime] = None) -> dict:
    """B-3: read dispatcher_heartbeat.log and classify the prior overnight
    window into exactly one of four states — ending the ambiguity where a
    missed fire, an idled night, and a crashed run all used to look the same
    (an absent or unremarkable log line) until someone reconstructed events
    by hand.

      - "no-heartbeat":       no LOADED entry in the lookback window. Means
                               the machine was off/asleep-without-wake, or
                               the launchd agent is unloaded — launchd never
                               ran this process at all.
      - "fired-late-on-wake": LOADED+FIRED seen, but the FIRED delta exceeds
                               LATE_THRESHOLD_SECONDS. launchd coalesced a
                               missed StartCalendarInterval fire onto the
                               next wake; the delta itself is the sleep
                               diagnosis (e.g. delta +4h49m means the machine
                               was asleep from ~02:15 until ~07:04).
      - "fired-and-idled":    ran on schedule, found an empty/ineligible
                               queue (IDLED-EMPTY-QUEUE), exited clean.
      - "fired-and-ran":      ran on schedule and attempted a job
                               (COMPLETED-RUN or ABORTED) — or LOADED/FIRED
                               were seen but no terminal outcome has been
                               recorded yet (still running, or crashed before
                               any outcome was written); treated
                               conservatively as this state rather than
                               silently omitted.

    Pure/read-only — never writes to the heartbeat log. Returns a dict with
    the classification plus the raw entries a morning report would want to
    quote (last_heartbeat, fired_entry, outcome_entry, preflight_dns).
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=HEARTBEAT_LOOKBACK_HOURS)

    entries: List[dict] = []
    if HEARTBEAT_LOG.exists():
        with open(HEARTBEAT_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                try:
                    ts = datetime.fromisoformat(entry["ts"])
                except (KeyError, ValueError, TypeError):
                    continue
                if ts >= cutoff:
                    entries.append(entry)

    loaded = [e for e in entries if e.get("event") == "LOADED"]
    if not loaded:
        return {
            "state": "no-heartbeat",
            "last_heartbeat": entries[-1] if entries else None,
            "fired_entry": None,
            "outcome_entry": None,
            "preflight_dns": None,
        }

    last_loaded = loaded[-1]
    last_loaded_ts = datetime.fromisoformat(last_loaded["ts"])
    cycle_entries = [e for e in entries if datetime.fromisoformat(e["ts"]) >= last_loaded_ts]

    fired_entry = next((e for e in cycle_entries if e.get("event") == "FIRED"), None)
    outcome_entry = next(
        (e for e in cycle_entries if e.get("event") in ("IDLED-EMPTY-QUEUE", "COMPLETED-RUN", "ABORTED")),
        None,
    )
    preflight_entry = next((e for e in cycle_entries if e.get("event") == "PREFLIGHT_DNS"), None)

    delta = fired_entry.get("delta_seconds") if fired_entry else None
    if delta is not None and delta > LATE_THRESHOLD_SECONDS:
        state = "fired-late-on-wake"
    elif outcome_entry is not None and outcome_entry.get("event") == "IDLED-EMPTY-QUEUE":
        state = "fired-and-idled"
    else:
        # COMPLETED-RUN, ABORTED, or no terminal outcome recorded yet — all
        # mean "a job was (or would have been) attempted this cycle".
        state = "fired-and-ran"

    return {
        "state": state,
        "last_heartbeat": last_loaded,
        "fired_entry": fired_entry,
        "outcome_entry": outcome_entry,
        "preflight_dns": preflight_entry,
    }


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
    Used as safety-net for launchd scheduled fires — this is the function
    launchd actually invokes at 02:15 daily via com.cjac.validation.plist.

    Self-evidencing (2026-07-16 directive, B-1/B-2): every invocation
    appends LOADED, FIRED (with scheduled-vs-actual delta), a PREFLIGHT_DNS
    probe, and exactly one terminal outcome
    (IDLED-EMPTY-QUEUE / COMPLETED-RUN / ABORTED) to
    logs/dispatcher_heartbeat.log — wrapped so an uncaught exception still
    writes ABORTED via the finally clause, rather than leaving the cycle
    silently unresolved. See classify_last_night() for how a morning report
    reads this back.
    """
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    _append_heartbeat("LOADED")

    now_utc = datetime.now(timezone.utc)
    scheduled_utc = _scheduled_fire_time_utc(now_utc)
    delta_seconds = (now_utc - scheduled_utc).total_seconds() if scheduled_utc else None
    _append_heartbeat(
        "FIRED",
        scheduled=scheduled_utc.isoformat() if scheduled_utc else None,
        delta_seconds=delta_seconds,
    )

    _append_heartbeat("PREFLIGHT_DNS", probes=_preflight_dns_probe())

    outcome_written = False
    try:
        eligible = pick_eligible_jobs(set())
        if not eligible:
            _append_heartbeat("IDLED-EMPTY-QUEUE")
            outcome_written = True
            print("[dispatch] Queue is empty or no eligible jobs — nothing to do.", flush=True)
            return

        job_path, job = eligible[0]
        print(f"[dispatch] Single-shot: {job.get('job_id','?')}", flush=True)
        proc = launch_job(job_path, job)
        proc.wait()
        success = finalize_job(proc)
        if success:
            _append_heartbeat("COMPLETED-RUN", run_id=job.get("job_id", "?"))
        else:
            _append_heartbeat(
                "ABORTED",
                reason=f"job returncode={proc.returncode}",
                run_id=job.get("job_id", "?"),
            )
        outcome_written = True
        if not success:
            sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        _append_heartbeat("ABORTED", reason=f"{type(e).__name__}: {e}")
        outcome_written = True
        raise
    finally:
        if not outcome_written:
            _append_heartbeat(
                "ABORTED",
                reason="dispatcher exited without recording a terminal outcome (uncaught early exit)",
            )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CJaC Validation Dispatcher")
    parser.add_argument(
        "--drain",
        action="store_true",
        default=False,
        help="Drain the full queue (parallel, continuous). Default: single-shot legacy mode.",
    )
    parser.add_argument(
        "--heartbeat-status",
        action="store_true",
        default=False,
        help=(
            "B-3: classify the prior overnight window from "
            "logs/dispatcher_heartbeat.log (no-heartbeat / fired-and-idled / "
            "fired-and-ran / fired-late-on-wake) and print as JSON. "
            "Read-only; for a morning report to consume."
        ),
    )
    args = parser.parse_args()

    if args.heartbeat_status:
        print(json.dumps(classify_last_night(), indent=2))
    elif args.drain:
        drain()
    else:
        main_single()
