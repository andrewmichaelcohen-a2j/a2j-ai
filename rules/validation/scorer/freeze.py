#!/usr/bin/env python3
"""
Golden Set Freeze Utility — Direction B, CJaC
Copyright 2026 Andrew M Cohen. Apache 2.0.

Andy runs this after reviewing and approving DRAFT candidates.
It:
  1. Reads a DRAFT golden set file
  2. Shows each candidate and prompts Andy to FREEZE, EDIT answer, or SKIP
  3. Writes frozen candidates to golden_sets/FROZEN/<module>/<file>.json
  4. Computes SHA256 content hash for each frozen item (immutability guard)
  5. Proposes a 70/30 train/held-out split (Andy approves or adjusts)
  6. Writes a manifest (hashes + split + attorney + date)

Immutability rule (from Direction B):
  - Only a named attorney (Andy) may establish or change a correct_answer.
  - The frozen directory is read-only to automation.
  - Content hash detects any automated edit.
  - The held-out partition is sealed at freeze time; the optimizer never sees it.

Usage:
    python3 freeze.py --input DRAFT_CA_notice_candidates_v0.1.json --attorney "Andrew M Cohen"
    python3 freeze.py --input DRAFT_CA_notice_candidates_v0.1.json --attorney "Andrew M Cohen" --non-interactive
"""

import os, sys, json, hashlib, datetime, argparse, shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GOLDEN_DIR = REPO_ROOT / "rules" / "validation" / "golden_sets"
FROZEN_DIR = GOLDEN_DIR / "FROZEN"
FROZEN_DIR.mkdir(parents=True, exist_ok=True)


def content_hash(candidate: dict) -> str:
    """SHA256 of the canonical fields. Matches golden_set_scorer.py."""
    canonical = {
        "id": candidate.get("id"),
        "facts": candidate.get("facts"),
        "question": candidate.get("question"),
        "correct_answer": candidate.get("correct_answer") or candidate.get("DRAFT_answer"),
        "authority": candidate.get("authority"),
    }
    serialized = json.dumps(canonical, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode()).hexdigest()


def set_hash(frozen_candidates: list) -> str:
    """SHA256 of the full set of content hashes (order-independent)."""
    hashes = sorted(c["_content_hash"] for c in frozen_candidates)
    return hashlib.sha256(json.dumps(hashes).encode()).hexdigest()


def freeze_candidate(draft: dict, attorney: str, correct_answer: str | None = None,
                     reasoning: str | None = None) -> dict:
    """Promote a DRAFT candidate to a FROZEN one."""
    frozen = dict(draft)
    # Promote DRAFT fields to canonical fields
    frozen["correct_answer"] = (correct_answer or
                                 draft.get("correct_answer") or
                                 draft.get("DRAFT_answer", ""))
    frozen["correct_reasoning"] = (reasoning or
                                    draft.get("correct_reasoning") or
                                    draft.get("DRAFT_reasoning", ""))
    # Remove DRAFT markers
    frozen.pop("DRAFT_answer", None)
    frozen.pop("DRAFT_reasoning", None)
    frozen.pop("unfrozen_flags", None)
    # Freeze metadata
    frozen["_frozen"] = True
    frozen["_attorney"] = attorney
    frozen["_frozen_date"] = datetime.date.today().isoformat()
    frozen["_content_hash"] = content_hash(frozen)
    return frozen


def propose_split(candidates: list, held_out_pct: float = 0.30) -> list:
    """
    Assign _split = "train" or "held-out".
    Strategy: alternate by difficulty band to ensure held-out is representative.
    Andy can override the split in the prompt.
    """
    by_band: dict[str, list] = {}
    for c in candidates:
        band = c.get("difficulty", "bright_line")
        by_band.setdefault(band, []).append(c)

    for band, cases in by_band.items():
        n_held = max(1, round(len(cases) * held_out_pct))
        # Take last n_held in each band as held-out (deterministic, not random)
        for i, c in enumerate(cases):
            c["_split"] = "held-out" if i >= (len(cases) - n_held) else "train"

    return candidates


def interactive_freeze(draft_candidates: list, attorney: str) -> list:
    """Walk through each candidate interactively. Andy confirms/edits each answer."""
    frozen = []
    print(f"\n{'═'*65}")
    print(f"GOLDEN SET FREEZE — attorney: {attorney}")
    print(f"{'═'*65}")
    print("Commands: [Enter]=FREEZE as-is  [e]=EDIT answer  [s]=SKIP\n")

    for i, c in enumerate(draft_candidates):
        print(f"\n[{i+1}/{len(draft_candidates)}] {c.get('id')} — {c.get('scenario','')}")
        print(f"  Facts: {c.get('facts','')[:200]}{'...' if len(c.get('facts',''))>200 else ''}")
        print(f"  Question: {c.get('question','')}")
        print(f"  DRAFT answer: {c.get('DRAFT_answer','')}")
        print(f"  DRAFT reasoning: {c.get('DRAFT_reasoning','')[:150]}...")
        print(f"  Authority: {c.get('authority','')}")
        print(f"  Confidence: {c.get('confidence','')}")

        action = input("\n  Action [Enter=freeze / e=edit / s=skip]: ").strip().lower()

        if action == "s":
            print(f"  → SKIPPED {c.get('id')}")
            continue
        elif action == "e":
            new_answer = input(f"  New answer (current: {c.get('DRAFT_answer','')}): ").strip()
            new_reasoning = input("  New reasoning (or Enter to keep): ").strip()
            frozen_c = freeze_candidate(
                c, attorney,
                correct_answer=new_answer or None,
                reasoning=new_reasoning or None,
            )
            print(f"  → FROZEN with edited answer: {frozen_c['correct_answer']}")
        else:
            frozen_c = freeze_candidate(c, attorney)
            print(f"  → FROZEN: {frozen_c['correct_answer']}")

        frozen.append(frozen_c)

    return frozen


def non_interactive_freeze(draft_candidates: list, attorney: str) -> list:
    """Freeze all candidates as-is with DRAFT answers (for testing/CI)."""
    frozen = []
    for c in draft_candidates:
        frozen_c = freeze_candidate(c, attorney)
        frozen.append(frozen_c)
        print(f"  FROZEN: {c.get('id')} → {frozen_c['correct_answer']}")
    return frozen


def write_frozen_set(frozen_candidates: list, draft_meta: dict, attorney: str,
                     module: str, jurisdiction: str) -> Path:
    """Write frozen golden set + manifest to FROZEN/<module>/."""
    module_dir = FROZEN_DIR / module
    module_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.date.today().isoformat()
    version = draft_meta.get("_schema_version", "golden_sets_v0.1")
    filename = f"FROZEN_{jurisdiction}_{module}_v1_{today}.json"
    out_path = module_dir / filename

    # Final split assignment
    frozen_candidates = propose_split(frozen_candidates)

    train = [c for c in frozen_candidates if c.get("_split") == "train"]
    held_out = [c for c in frozen_candidates if c.get("_split") == "held-out"]

    print(f"\n  Proposed split: {len(train)} train / {len(held_out)} held-out")
    confirm = input("  Accept split? [Enter=yes / n=adjust]: ").strip().lower()
    if confirm == "n":
        n_held = int(input(f"  How many held-out? (0–{len(frozen_candidates)}): ").strip())
        for i, c in enumerate(frozen_candidates):
            c["_split"] = "held-out" if i >= (len(frozen_candidates) - n_held) else "train"
        train = [c for c in frozen_candidates if c.get("_split") == "train"]
        held_out = [c for c in frozen_candidates if c.get("_split") == "held-out"]
        print(f"  Adjusted: {len(train)} train / {len(held_out)} held-out")

    set_h = set_hash(frozen_candidates)
    manifest = {
        "_copyright": "Copyright 2026 Andrew M Cohen. Apache 2.0.",
        "_status": "FROZEN — attorney-established ground truth. Immutable to automation.",
        "_schema_version": version,
        "_module": module,
        "_jurisdiction": jurisdiction,
        "_frozen_date": today,
        "_attorney": attorney,
        "_count": len(frozen_candidates),
        "_train_count": len(train),
        "_held_out_count": len(held_out),
        "_set_hash": set_h,
        "_immutability_note": (
            "Content hash per candidate + set hash detect any automated edit. "
            "The held-out partition is sealed. The optimizer (Direction C) never sees it. "
            "Only a named attorney may change a correct_answer."
        ),
        "candidates": frozen_candidates,
    }

    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\n✅ Frozen set written: {out_path.relative_to(REPO_ROOT)}")
    print(f"   {len(frozen_candidates)} frozen candidates | set hash: {set_h[:16]}…")
    print(f"   {len(train)} train / {len(held_out)} held-out")
    print(f"\n⚠️  Held-out is now SEALED. Never expose to optimizer or re-run scorer on it")
    print(f"   until you are ready for your final metric. Doing so burns the held-out set.")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Freeze DRAFT golden-set candidates")
    parser.add_argument("--input", required=True,
                        help="DRAFT golden set JSON file (relative to golden_sets/ or absolute)")
    parser.add_argument("--attorney", required=True,
                        help="Named attorney establishing ground truth (e.g. 'Andrew M Cohen')")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Freeze all as-is (for testing; not for real attorney sign-off)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = GOLDEN_DIR / input_path
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    draft = json.loads(input_path.read_text())
    if not draft.get("_status", "").startswith("DRAFT"):
        print("⚠️  File does not appear to be a DRAFT set. Proceeding anyway.")

    module = draft.get("_module", "unknown")
    jurisdiction = draft.get("_jurisdiction", "unknown")
    candidates = draft.get("candidates", [])

    print(f"Loaded {len(candidates)} DRAFT candidates — {jurisdiction} / {module}")

    if args.non_interactive:
        frozen = non_interactive_freeze(candidates, args.attorney)
    else:
        frozen = interactive_freeze(candidates, args.attorney)

    if not frozen:
        print("No candidates frozen. Exiting.")
        sys.exit(0)

    write_frozen_set(frozen, draft, args.attorney, module, jurisdiction)


if __name__ == "__main__":
    main()
