#!/bin/bash
# run_dispatch.sh — CJaC Dispatcher Shell Wrapper
# =================================================
# Launchd safety-net wrapper. Launchd calls THIS script (which has Full Disk
# Access via its enclosing application) rather than calling python3 directly.
# The script resolves the correct Python and hands off to dispatch.py.
#
# To set up FDA:
#   1. In System Settings → Privacy & Security → Full Disk Access, add /bin/bash
#      (or confirm that the Terminal.app that runs this already has FDA).
#   2. Update the launchd plist ProgramArguments to call this script instead of
#      python3 directly:
#        <string>/bin/bash</string>
#        <string>/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/run_dispatch.sh</string>
#
# For --drain mode (continuous, called from a loop):
#   bash run_dispatch.sh --drain
#
# For single-shot mode (launchd safety-net):
#   bash run_dispatch.sh
#
# Copyright 2026 Andrew M Cohen. Apache 2.0.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DISPATCH_PY="$REPO_ROOT/rules/validation/dispatch.py"

# Resolve Python: prefer a Python 3.10+ from common locations
for PY in \
    /opt/homebrew/bin/python3 \
    /usr/local/bin/python3 \
    /usr/bin/python3 \
    python3; do
    if command -v "$PY" &>/dev/null; then
        PY_VERSION=$("$PY" -c "import sys; print(sys.version_info[:2])" 2>/dev/null || echo "(0, 0)")
        if "$PY" -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)" 2>/dev/null; then
            PYTHON="$PY"
            break
        fi
    fi
done

if [ -z "${PYTHON:-}" ]; then
    echo "[run_dispatch.sh] ERROR: No Python 3.9+ found" >&2
    exit 1
fi

echo "[run_dispatch.sh] Using Python: $PYTHON ($("$PYTHON" --version 2>&1))"
echo "[run_dispatch.sh] Dispatch script: $DISPATCH_PY"
echo "[run_dispatch.sh] Mode: ${1:---single}"

if [ "${1:-}" = "--drain" ]; then
    exec caffeinate -ims "$PYTHON" "$DISPATCH_PY" --drain
else
    exec caffeinate -ims "$PYTHON" "$DISPATCH_PY"
fi
