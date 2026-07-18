#!/usr/bin/env python3
"""
Regression tests for dispatch.py's self-evidencing heartbeat forensics
(2026-07-16 directive — Dispatcher Resilience & Overnight-Environment
Forensics, Part B: B-1 heartbeat log, B-2 preflight DNS probe, B-3
classify_last_night()).

No live subprocess launches and no real network calls — main_single()'s
side effects are exercised via mocks on pick_eligible_jobs / launch_job /
finalize_job / _preflight_dns_probe, and classify_last_night() is tested
directly against synthetic heartbeat-log fixtures written to a tempdir.

Run with:
  python3 rules/validation/tests/test_dispatcher_heartbeat.py

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation"))

import dispatch  # noqa: E402

_PASS = []
_FAIL = []


def test(name: str, condition: bool, detail: str = ""):
    if condition:
        _PASS.append(name)
        print(f"  ✓  {name}")
    else:
        _FAIL.append(name)
        print(f"  ✗  {name}{' — ' + detail if detail else ''}")


def _read_heartbeat_entries(path: Path):
    if not path.exists():
        return []
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


# ══════════════════════════════════════════════════════════════════════════════
# B-1/B-2: main_single() writes LOADED / FIRED / PREFLIGHT_DNS / one outcome
# ══════════════════════════════════════════════════════════════════════════════

def test_main_single_idle_queue_writes_full_event_sequence():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        log_dir = Path(tmp)
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path), \
             patch.object(dispatch, "LOG_DIR", log_dir), \
             patch.object(dispatch, "QUEUE_DIR", log_dir), \
             patch.object(dispatch, "DONE_DIR", log_dir), \
             patch.object(dispatch, "FAILED_DIR", log_dir), \
             patch.object(dispatch, "RESULTS_DIR", log_dir), \
             patch.object(dispatch, "_preflight_dns_probe", return_value={"courtlistener": {"ok": True}}), \
             patch.object(dispatch, "pick_eligible_jobs", return_value=[]):
            dispatch.main_single()

        entries = _read_heartbeat_entries(hb_path)
        events = [e["event"] for e in entries]
        test("empty-queue run writes LOADED, FIRED, PREFLIGHT_DNS, IDLED-EMPTY-QUEUE in order",
             events == ["LOADED", "FIRED", "PREFLIGHT_DNS", "IDLED-EMPTY-QUEUE"], events)
        test("exactly one terminal outcome event was written (dry-run: empty queue)",
             sum(1 for e in events if e in ("IDLED-EMPTY-QUEUE", "COMPLETED-RUN", "ABORTED")) == 1,
             events)
        fired = entries[1]
        test("FIRED entry carries a delta_seconds field", "delta_seconds" in fired, fired)
        preflight = entries[2]
        test("PREFLIGHT_DNS entry carries the mocked probe payload",
             preflight.get("probes") == {"courtlistener": {"ok": True}}, preflight)


def test_main_single_completed_run_writes_completed_event():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        log_dir = Path(tmp)
        fake_job = {"job_id": "job_fake_ok"}
        fake_proc = MagicMock()
        fake_proc.returncode = 0
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path), \
             patch.object(dispatch, "LOG_DIR", log_dir), \
             patch.object(dispatch, "QUEUE_DIR", log_dir), \
             patch.object(dispatch, "DONE_DIR", log_dir), \
             patch.object(dispatch, "FAILED_DIR", log_dir), \
             patch.object(dispatch, "RESULTS_DIR", log_dir), \
             patch.object(dispatch, "_preflight_dns_probe", return_value={}), \
             patch.object(dispatch, "pick_eligible_jobs", return_value=[(Path(tmp) / "job_fake_ok.json", fake_job)]), \
             patch.object(dispatch, "launch_job", return_value=fake_proc), \
             patch.object(dispatch, "finalize_job", return_value=True):
            dispatch.main_single()

        entries = _read_heartbeat_entries(hb_path)
        events = [e["event"] for e in entries]
        test("a real job run writes COMPLETED-RUN as its terminal outcome",
             events == ["LOADED", "FIRED", "PREFLIGHT_DNS", "COMPLETED-RUN"], events)
        test("COMPLETED-RUN entry names the run_id", entries[-1].get("run_id") == "job_fake_ok", entries[-1])


def test_main_single_job_failure_writes_aborted_not_silent():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        log_dir = Path(tmp)
        fake_job = {"job_id": "job_fake_fail"}
        fake_proc = MagicMock()
        fake_proc.returncode = 1
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path), \
             patch.object(dispatch, "LOG_DIR", log_dir), \
             patch.object(dispatch, "QUEUE_DIR", log_dir), \
             patch.object(dispatch, "DONE_DIR", log_dir), \
             patch.object(dispatch, "FAILED_DIR", log_dir), \
             patch.object(dispatch, "RESULTS_DIR", log_dir), \
             patch.object(dispatch, "_preflight_dns_probe", return_value={}), \
             patch.object(dispatch, "pick_eligible_jobs", return_value=[(Path(tmp) / "job_fake_fail.json", fake_job)]), \
             patch.object(dispatch, "launch_job", return_value=fake_proc), \
             patch.object(dispatch, "finalize_job", return_value=False):
            try:
                dispatch.main_single()
            except SystemExit:
                pass  # expected: non-zero returncode -> sys.exit(1)

        entries = _read_heartbeat_entries(hb_path)
        events = [e["event"] for e in entries]
        test("a failed job writes ABORTED (not silently swallowed)",
             events == ["LOADED", "FIRED", "PREFLIGHT_DNS", "ABORTED"], events)
        test("exactly one terminal outcome — finally clause does not double-write",
             sum(1 for e in events if e in ("IDLED-EMPTY-QUEUE", "COMPLETED-RUN", "ABORTED")) == 1,
             events)


def test_main_single_uncaught_exception_still_writes_aborted_via_finally():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        log_dir = Path(tmp)
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path), \
             patch.object(dispatch, "LOG_DIR", log_dir), \
             patch.object(dispatch, "QUEUE_DIR", log_dir), \
             patch.object(dispatch, "DONE_DIR", log_dir), \
             patch.object(dispatch, "FAILED_DIR", log_dir), \
             patch.object(dispatch, "RESULTS_DIR", log_dir), \
             patch.object(dispatch, "_preflight_dns_probe", return_value={}), \
             patch.object(dispatch, "pick_eligible_jobs", side_effect=RuntimeError("simulated crash pre-outcome")):
            try:
                dispatch.main_single()
                raised = False
            except RuntimeError:
                raised = True

        test("the simulated crash propagates (not swallowed)", raised)
        entries = _read_heartbeat_entries(hb_path)
        events = [e["event"] for e in entries]
        test("uncaught exception still writes ABORTED via the except/finally path",
             events == ["LOADED", "FIRED", "PREFLIGHT_DNS", "ABORTED"], events)
        test("ABORTED entry names the exception", "RuntimeError" in entries[-1].get("reason", ""), entries[-1])


# ══════════════════════════════════════════════════════════════════════════════
# B-3: classify_last_night() — the four states
# ══════════════════════════════════════════════════════════════════════════════

def _write_lines(path: Path, entries):
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def test_classify_no_heartbeat_when_log_missing():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "does_not_exist.log"
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path):
            result = dispatch.classify_last_night()
        test("missing heartbeat log classifies as no-heartbeat",
             result["state"] == "no-heartbeat", result)


def test_classify_no_heartbeat_when_entries_are_stale():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        now = datetime(2026, 7, 18, 12, 0, tzinfo=timezone.utc)
        stale_ts = (now - timedelta(hours=40)).isoformat()  # older than the 30h lookback
        _write_lines(hb_path, [{"ts": stale_ts, "event": "LOADED", "pid": 1}])
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path):
            result = dispatch.classify_last_night(now_utc=now)
        test("a LOADED entry older than the lookback window still classifies as no-heartbeat",
             result["state"] == "no-heartbeat", result)


def test_classify_fired_and_idled():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        now = datetime(2026, 7, 18, 9, 20, tzinfo=timezone.utc)
        fired_ts = now - timedelta(minutes=5)
        _write_lines(hb_path, [
            {"ts": fired_ts.isoformat(), "event": "LOADED", "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "FIRED", "delta_seconds": 120, "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "PREFLIGHT_DNS", "probes": {}, "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "IDLED-EMPTY-QUEUE", "pid": 1},
        ])
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path):
            result = dispatch.classify_last_night(now_utc=now)
        test("on-time fire with an empty queue classifies as fired-and-idled",
             result["state"] == "fired-and-idled", result)


def test_classify_fired_and_ran_completed():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        now = datetime(2026, 7, 18, 9, 20, tzinfo=timezone.utc)
        fired_ts = now - timedelta(minutes=5)
        _write_lines(hb_path, [
            {"ts": fired_ts.isoformat(), "event": "LOADED", "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "FIRED", "delta_seconds": 90, "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "PREFLIGHT_DNS", "probes": {}, "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "COMPLETED-RUN", "run_id": "job_x", "pid": 1},
        ])
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path):
            result = dispatch.classify_last_night(now_utc=now)
        test("on-time fire that completed a run classifies as fired-and-ran",
             result["state"] == "fired-and-ran", result)


def test_classify_fired_late_on_wake():
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        # 02:15 PT ~= 09:15 UTC (PDT, summer). Simulate a fire at ~14:04 UTC —
        # roughly the directive's own example: "FIRED at 7:04 AM with delta
        # +4h49m" against a 02:15 schedule.
        now = datetime(2026, 7, 18, 14, 4, tzinfo=timezone.utc)
        fired_ts = now
        _write_lines(hb_path, [
            {"ts": fired_ts.isoformat(), "event": "LOADED", "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "FIRED", "delta_seconds": 4 * 3600 + 49 * 60, "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "PREFLIGHT_DNS", "probes": {}, "pid": 1},
            {"ts": fired_ts.isoformat(), "event": "IDLED-EMPTY-QUEUE", "pid": 1},
        ])
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path):
            result = dispatch.classify_last_night(now_utc=now)
        test("a large FIRED delta classifies as fired-late-on-wake regardless of outcome",
             result["state"] == "fired-late-on-wake", result)
        test("fired-late-on-wake result still surfaces the fired_entry for the delta",
             result["fired_entry"] is not None and result["fired_entry"]["delta_seconds"] > dispatch.LATE_THRESHOLD_SECONDS,
             result)


def test_classify_uses_most_recent_loaded_cycle_only():
    """Two cycles in the log (e.g. a manual re-run after a bad night) —
    classification must reflect the latest LOADED, not an earlier one."""
    with tempfile.TemporaryDirectory() as tmp:
        hb_path = Path(tmp) / "dispatcher_heartbeat.log"
        now = datetime(2026, 7, 18, 9, 20, tzinfo=timezone.utc)
        old_ts = now - timedelta(hours=6)
        new_ts = now - timedelta(minutes=2)
        _write_lines(hb_path, [
            {"ts": old_ts.isoformat(), "event": "LOADED", "pid": 1},
            {"ts": old_ts.isoformat(), "event": "FIRED", "delta_seconds": 4 * 3600, "pid": 1},
            {"ts": old_ts.isoformat(), "event": "ABORTED", "reason": "old crash", "pid": 1},
            {"ts": new_ts.isoformat(), "event": "LOADED", "pid": 2},
            {"ts": new_ts.isoformat(), "event": "FIRED", "delta_seconds": 60, "pid": 2},
            {"ts": new_ts.isoformat(), "event": "PREFLIGHT_DNS", "probes": {}, "pid": 2},
            {"ts": new_ts.isoformat(), "event": "IDLED-EMPTY-QUEUE", "pid": 2},
        ])
        with patch.object(dispatch, "HEARTBEAT_LOG", hb_path):
            result = dispatch.classify_last_night(now_utc=now)
        test("classification reflects the most recent LOADED cycle, not an earlier stale one",
             result["state"] == "fired-and-idled" and result["last_heartbeat"]["pid"] == 2, result)


# ══════════════════════════════════════════════════════════════════════════════
# _scheduled_fire_time_utc — sanity checks on the delta baseline
# ══════════════════════════════════════════════════════════════════════════════

def test_scheduled_fire_time_is_before_now_when_invoked_after_schedule():
    now = datetime(2026, 7, 18, 9, 20, tzinfo=timezone.utc)  # ~02:20 PT
    scheduled = dispatch._scheduled_fire_time_utc(now)
    test("scheduled fire time resolves to a real datetime (zoneinfo available)",
         scheduled is not None, scheduled)
    if scheduled is not None:
        test("scheduled fire time is at or before 'now' for a same-day post-schedule check",
             scheduled <= now, (scheduled, now))


def test_scheduled_fire_time_rolls_back_a_day_when_invoked_before_schedule():
    # A daytime manual --heartbeat-status check, well before tonight's 02:15 PT.
    now = datetime(2026, 7, 18, 20, 0, tzinfo=timezone.utc)  # ~13:00 PT, daytime
    scheduled = dispatch._scheduled_fire_time_utc(now)
    if scheduled is not None:
        test("a daytime check resolves 'scheduled' to today's already-passed 02:15, not a future one",
             scheduled <= now, (scheduled, now))


# ══════════════════════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} test functions...\n")
    for t in tests:
        t()
    print(f"\nResults: {len(_PASS)}/{len(_PASS) + len(_FAIL)} passed")
    if _FAIL:
        print(f"FAILED: {_FAIL}")
        sys.exit(1)
