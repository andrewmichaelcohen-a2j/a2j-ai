#!/bin/bash
# run_now.sh — Parallel job launcher (manual trigger)
# Runs queued jobs immediately in background without waiting for 2:15 AM launchd.
# Usage: bash rules/validation/run_now.sh
#
# CURRENT JOBS (2026-06-26 evening):
#   Job 1: notice tiebreaker (7 states — GA CRITICAL + AR/MN/OR/SD/WY/TN)
#   Job 2: NJ failure_to_attach probe (diagnostic — 3 probe queries)
#
# Copyright 2026 Andrew M Cohen. Apache 2.0.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG_DIR="$REPO_ROOT/rules/validation/logs"
PYTHON="/usr/bin/python3"

mkdir -p "$LOG_DIR"

TS=$(date -u +"%Y%m%d_%H%M")

echo "[run_now] $(date) — launching jobs"

# Job 1: notice tiebreaker (7 states — GA CRITICAL + AR/MN/OR/SD/WY/TN)
LOG1="$LOG_DIR/notice_tiebreaker_${TS}.log"
echo "[run_now] Job 1: notice tiebreaker (7 states) → $LOG1"
"$PYTHON" -u "$REPO_ROOT/rules/validation/l2/notice_tiebreaker_20260626.py" \
    > "$LOG1" 2>&1 &
PID1=$!

# Job 2: NJ failure_to_attach probe (diagnostic — 3 probes)
LOG2="$LOG_DIR/nj_attach_probe_${TS}.log"
echo "[run_now] Job 2: NJ attach probe → $LOG2"
"$PYTHON" -u "$REPO_ROOT/rules/validation/l2/nj_attach_probe_20260626.py" \
    > "$LOG2" 2>&1 &
PID2=$!

echo ""
echo "[run_now] Both jobs running in background."
echo "  notice tiebreaker PID: $PID1  | tail -f $LOG1"
echo "  NJ attach probe   PID: $PID2  | tail -f $LOG2"
echo ""
echo "Monitor:"
echo "  tail -f $LOG1"
echo "  tail -f $LOG2"
echo ""
echo "Output files when done:"
echo "  rules/validation/l2/output/notice_tiebreaker_20260626.json"
echo "  rules/validation/l2/output/nj_attach_probe_20260626.json"
echo ""
echo "Send both output filenames to Cowork for ingestion."

wait $PID1
echo "[run_now] Job 1 (notice tiebreaker) done — exit $?"

wait $PID2
echo "[run_now] Job 2 (NJ probe) done — exit $?"
