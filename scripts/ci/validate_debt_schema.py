#!/usr/bin/env python3
"""
validate_debt_schema.py -- ENG_HARDENING Task 2 (CI pipeline: schema validation),
folded into Phase A per DEBT_PROJECT_ARCHITECTURE_SPEC.md v4 section 3.

Validates every *.json file under rules/debt/ against rules/schema/debt_schema_v1.0.json.
Skips nothing silently -- if a debt-track JSON file can't be schema-validated,
that's a build failure, not a warning, per the "structurally enforced, not
directive-invoked" goal of this task.

Usage: python3 scripts/ci/validate_debt_schema.py
Exit code 0 = all files valid; 1 = one or more files failed validation.
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("FAIL: jsonschema package not installed. `pip install jsonschema` (or "
          "`pip install jsonschema --break-system-packages` in externally-managed envs).")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "rules" / "schema" / "debt_schema_v1.0.json"
DEBT_DIR = REPO_ROOT / "rules" / "debt"


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"FAIL: schema not found at {SCHEMA_PATH}")
        return 1

    schema = json.loads(SCHEMA_PATH.read_text())

    if not DEBT_DIR.exists():
        print(f"WARNING: {DEBT_DIR} does not exist -- nothing to validate.")
        return 0

    rule_files = sorted(DEBT_DIR.rglob("*.json"))
    if not rule_files:
        print(f"WARNING: no .json files found under {DEBT_DIR} -- nothing to validate.")
        return 0

    failures = []
    checked = 0
    for path in rule_files:
        rel = path.relative_to(REPO_ROOT)
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            failures.append(f"{rel}: not valid JSON -- {e}")
            continue

        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            failures.append(f"{rel}: schema validation failed -- {e.message} (path: {list(e.absolute_path)})")
            continue

        # Structural sanity checks beyond bare schema validity, per house discipline:
        for node in data.get("nodes", []):
            node_id = node.get("node_id", "<missing node_id>")
            tier = node.get("tier")
            if tier not in ("DRAFT", "CORROBORATED", "VALIDATED"):
                failures.append(f"{rel}: node {node_id} has invalid tier {tier!r}")
            if tier == "VALIDATED":
                cert = node.get("provenance", {}).get("ratification", {})
                if not cert.get("certifying_attorney"):
                    failures.append(
                        f"{rel}: node {node_id} is tagged VALIDATED but has no certifying_attorney "
                        f"in provenance.ratification -- per spec section 3(g), VALIDATED requires "
                        f"named-attorney release certification, never self-certified."
                    )

        checked += 1
        print(f"OK: {rel} ({len(data.get('nodes', []))} node(s))")

    if failures:
        print("\n".join(f"FAIL: {f}" for f in failures))
        print(f"\nFAIL: {len(failures)} issue(s) across {checked} file(s) checked.")
        return 1

    print(f"\nPASS: all {checked} debt-track rules file(s) valid against {SCHEMA_PATH.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
