#!/usr/bin/env python3
"""
run_protocol.py — CJaC Validation Runner (Level 1)
====================================================
Single entrypoint for all validation protocols. Runs unattended:
  - Checkpoint-based resumption (crash at case 30/51 → resume at 31)
  - Transient-error retry with exponential backoff + jitter
  - GPT-empty fallback (retry trimmed → Claude-haiku; independence preserved)
  - Provenance enforcement (single-model → single-model-preliminary, always)
  - Completion summary written to results/

Usage:
  python3 rules/validation/run_protocol.py \\
    --protocol retaliation_holdings_v3 \\
    --states AZ,DC,IA,KY,MA,ME,MN,NE,NH,RI,WA,DE,AR,IN,MO,VA \\
    --sleep 10

  # Resume a failed run (same command — checkpoint auto-detected):
  python3 rules/validation/run_protocol.py --protocol retaliation_holdings_v3 \\
    --states AZ,DC,... --sleep 10

  # Force clean start:
  python3 rules/validation/run_protocol.py --protocol retaliation_holdings_v3 \\
    --states AZ,DC,... --sleep 10 --fresh

Launch unattended (fire-and-forget, survives terminal close, keeps Mac awake):
  cd /Users/andrewcohen/Documents/GitHub/a2j-ai
  caffeinate -ims nohup python3 rules/validation/run_protocol.py \\
    --protocol retaliation_holdings_v3 \\
    --states AZ,DC,IA,KY,MA,ME,MN,NE,NH,RI,WA,DE,AR,IN,MO,VA \\
    --sleep 10 \\
    > rules/validation/logs/holdings_v3_$(date +%Y%m%d_%H%M).log 2>&1 &

  # Check progress (Ctrl-C doesn't kill the run):
  tail -f rules/validation/logs/holdings_v3_*.log

tmux alternative (can reattach to watch):
  tmux new -s val
  caffeinate -ims python3 rules/validation/run_protocol.py --protocol ... --sleep 10
  # detach: Ctrl-b d     reattach: tmux attach -t val

Available protocols: retaliation_holdings_v3
  (add more by dropping a module in rules/validation/protocols/ with
   PROTOCOL_NAME, get_units(states), run_unit(unit))

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import argparse
import importlib
import sys
import uuid
from pathlib import Path

# ---- repo root on sys.path ----
_REPO_ROOT  = Path(__file__).parent.parent.parent
_VAL_ROOT   = Path(__file__).parent
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_VAL_ROOT))

from harness import ValidationHarness  # noqa: E402

# ---- Directory layout ----
CHECKPOINT_DIR = _VAL_ROOT / ".checkpoints"
LOG_DIR        = _VAL_ROOT / "logs"
RESULTS_DIR    = _VAL_ROOT / "results"
OUTPUT_DIR     = _VAL_ROOT / "l2" / "output"


def load_protocol(protocol_name: str):
    """Dynamically import a protocol module from protocols/."""
    try:
        mod = importlib.import_module(f"protocols.{protocol_name}")
    except ModuleNotFoundError:
        print(f"ERROR: No protocol module 'protocols/{protocol_name}.py' found.")
        print("Available protocols: retaliation_holdings_v3")
        sys.exit(1)
    for attr in ("PROTOCOL_NAME", "get_units", "run_unit"):
        if not hasattr(mod, attr):
            print(f"ERROR: Protocol module missing required attribute '{attr}'")
            sys.exit(1)
    return mod


def main():
    parser = argparse.ArgumentParser(
        description="CJaC Validation Runner — launch once, runs to completion unattended."
    )
    parser.add_argument("--protocol", required=True,
                        help="Protocol name, e.g. retaliation_holdings_v3")
    parser.add_argument("--states", required=True,
                        help="Comma-separated state codes, e.g. AZ,DC,IA")
    parser.add_argument("--sleep", type=float, default=10.0,
                        help="Seconds to sleep between cases (default: 10)")
    parser.add_argument("--fresh", action="store_true",
                        help="Ignore existing checkpoint and restart clean")
    parser.add_argument("--run-id",
                        help="Override run ID (default: new UUID per run, or resumed from checkpoint)")
    parser.add_argument("--max-retries", type=int, default=4,
                        help="Max retry attempts per unit on transient errors (default: 4)")
    args = parser.parse_args()

    states = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    if not states:
        print("ERROR: --states produced an empty list")
        sys.exit(1)

    protocol = load_protocol(args.protocol)

    # run_id: stable across resumes (stored in checkpoint), new on --fresh
    run_id = args.run_id or uuid.uuid4().hex[:8]

    print("=" * 60)
    print(f"CJaC Validation Runner")
    print(f"Protocol : {args.protocol}")
    print(f"States   : {', '.join(states)} ({len(states)} total)")
    print(f"Run ID   : {run_id}")
    print(f"Sleep    : {args.sleep}s between cases")
    print(f"Fresh    : {args.fresh}")
    print(f"Max retry: {args.max_retries}")
    print("=" * 60)
    print("CRITICAL: machine-verified is BELOW the attorney line.")
    print("A result is only real if this run exits cleanly and writes a raw output file.")
    print()

    units = protocol.get_units(states)
    print(f"Units to process: {len(units)}")

    harness = ValidationHarness(
        protocol_name=args.protocol,
        units=units,
        run_id=run_id,
        checkpoint_dir=CHECKPOINT_DIR,
        log_dir=LOG_DIR,
        results_dir=RESULTS_DIR,
        output_dir=OUTPUT_DIR,
        inter_case_sleep=args.sleep,
        max_retry_attempts=args.max_retries,
        retry_base_sleep=15.0,
        fresh=args.fresh,
    )

    results = harness.run(protocol.run_unit)

    mv  = sum(1 for r in results if r.get("disposition") == "machine-verified")
    smp = sum(1 for r in results if r.get("disposition") == "single-model-preliminary")
    na  = sum(1 for r in results if r.get("disposition") == "needs-attorney")
    print()
    print("=" * 60)
    print(f"Done. {len(results)} units.")
    print(f"  machine-verified:         {mv}")
    print(f"  single-model-preliminary: {smp}")
    print(f"  needs-attorney:           {na}")
    print(f"  other:                    {len(results) - mv - smp - na}")
    print()
    print(f"Summary in: {RESULTS_DIR}/")
    print(f"Raw output: {OUTPUT_DIR}/")
    print()
    print("⚠️  STOP AND REPORT. Share output filename with Cowork for ingestion.")
    print("=" * 60)


if __name__ == "__main__":
    main()
