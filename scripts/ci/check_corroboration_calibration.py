#!/usr/bin/env python3
"""
check_corroboration_calibration.py -- freeze item 3 (2026-08-31, round 26):
"no runner change ships, and no live run is requested from Andy, unless
calibration and replay pass first."

Runs `scripts/corroboration/run_corroboration.py --replay` -- the full
corroboration pipeline exercised offline against the frozen calibration
fixture set (no keys, no network, no cost) -- and asserts both per-fixture
known-answer outcomes and the aggregate demo-gate metrics. See
scripts/corroboration/calibration_fixtures/ for the fixture set itself and
docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md S4's round-26 entry for the
discipline this mirrors (Open Question #11 / the eviction scorer's
known-answer calibration suite).

Usage: python3 scripts/ci/check_corroboration_calibration.py
Exit code 0 = calibration + replay pass; 1 = any fixture or metric assertion
failed, or no fixtures were found.

This check does not require the debt schema or frozen-artifact checks to
have passed first, and vice versa -- all three are independent, run
together at the end of every round per the standing verification discipline.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "scripts" / "corroboration" / "run_corroboration.py"


def main():
    if not RUNNER.exists():
        print(f"FAIL: {RUNNER} not found.")
        sys.exit(1)
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--replay"],
        cwd=str(REPO_ROOT),
    )
    if result.returncode == 0:
        print("\nPASS: corroboration-runner calibration + replay suite passed. "
              "Runner changes may ship; a live run may be requested from Andy.")
        sys.exit(0)
    else:
        print("\nFAIL: corroboration-runner calibration + replay suite failed "
              "(see fixture-level output above). Per the 2026-08-31 live-run "
              "freeze, no runner change ships and no live run is requested "
              "from Andy until this passes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
