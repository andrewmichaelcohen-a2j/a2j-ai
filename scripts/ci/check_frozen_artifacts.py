#!/usr/bin/env python3
"""
check_frozen_artifacts.py -- ENG_HARDENING Task 2, folded into Phase A per
DEBT_PROJECT_ARCHITECTURE_SPEC.md v4 section 3.

Recomputes SHA256 of every file listed in scripts/ci/frozen_artifact_manifest.json
and compares against the committed hash. Any drift fails the build. This is the
CI-structural enforcement of the standing discipline "never write to vProof1,
never re-score v0.3 held-out" -- previously enforced only by directive, not by
a machine check.

Usage: python3 scripts/ci/check_frozen_artifacts.py
Exit code 0 = all frozen artifacts match; 1 = drift detected or a listed file
is missing.
"""
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "scripts" / "ci" / "frozen_artifact_manifest.json"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"FAIL: manifest not found at {MANIFEST_PATH}")
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text())
    entries = manifest.get("frozen_files", [])
    if not entries:
        print("WARNING: manifest has no frozen_files entries -- nothing checked.")
        return 0

    failures = []
    for entry in entries:
        rel_path = entry["path"]
        expected_sha = entry["sha256"]
        label = entry.get("label", "")
        full_path = REPO_ROOT / rel_path

        if not full_path.exists():
            failures.append(f"MISSING: {rel_path} ({label}) -- file listed in manifest does not exist")
            continue

        actual_sha = sha256_of(full_path)
        if actual_sha != expected_sha:
            failures.append(
                f"DRIFT: {rel_path} ({label})\n"
                f"  expected sha256: {expected_sha}\n"
                f"  actual   sha256: {actual_sha}\n"
                f"  This file is frozen. If this change was intentional (e.g. a deliberate,\n"
                f"  ratified re-freeze), update the manifest explicitly and say so in the\n"
                f"  commit message -- do not let this check pass silently."
            )
        else:
            print(f"OK: {rel_path} matches frozen hash")

    if failures:
        print("\n".join(failures))
        print(f"\nFAIL: {len(failures)} frozen-artifact check(s) failed.")
        return 1

    print(f"\nPASS: all {len(entries)} frozen artifact(s) match their committed hash.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
