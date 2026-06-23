#!/usr/bin/env python3
"""
Shared Validation Harness — CJaC
=================================
Provides reliability, checkpointing, provenance enforcement, and summary
writing for every validation protocol. Protocols import this; they do not
copy reliability logic.

Usage pattern:
    from harness import (ValidationHarness, TransientError, PermanentError,
                         call_claude_fallback)
    harness = ValidationHarness(protocol_name, units, config, dirs)
    results = harness.run(protocol_run_unit_fn)

Provenance rule (NON-NEGOTIABLE):
    A unit is `machine-verified` only if two distinct models returned
    parseable data AND those model names differ. Any other outcome →
    `single-model-preliminary`. The string "validated" is never emitted.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

from __future__ import annotations

import json
import logging
import os
import random
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Exception types (protocol code raises these to signal retry vs. give-up)
# ---------------------------------------------------------------------------

class TransientError(Exception):
    """Raise for 429s, network timeouts, session-quota exhaustion.
    Harness will retry with exponential backoff."""

class PermanentError(Exception):
    """Raise when the unit cannot succeed regardless of retries (wrong-doc,
    missing case data, etc.). Harness records failure and moves on."""


# ---------------------------------------------------------------------------
# Checkpoint  (write each unit result as it finishes; resume skips done units)
# ---------------------------------------------------------------------------

class Checkpoint:
    def __init__(self, path: Path):
        self.path = path
        self._data: dict = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            try:
                with open(self.path) as f:
                    return json.load(f)
            except Exception:
                pass
        return {"completed": {}, "meta": {}}

    def is_done(self, unit_id: str) -> bool:
        return unit_id in self._data["completed"]

    def record(self, unit_id: str, result: dict):
        self._data["completed"][unit_id] = result
        self._save()

    def get_result(self, unit_id: str) -> dict | None:
        return self._data["completed"].get(unit_id)

    def all_results(self) -> list[dict]:
        return list(self._data["completed"].values())

    def set_meta(self, key: str, value: Any):
        self._data["meta"][key] = value
        self._save()

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
        tmp.replace(self.path)


# ---------------------------------------------------------------------------
# Logger  (append-only, timestamped)
# ---------------------------------------------------------------------------

def make_logger(name: str, log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s",
                                          datefmt="%Y-%m-%dT%H:%M:%S"))
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("%(asctime)s  %(message)s", datefmt="%H:%M:%S"))
        logger.addHandler(sh)
    return logger


# ---------------------------------------------------------------------------
# Retry with backoff + jitter
# ---------------------------------------------------------------------------

def run_with_retry(
    fn: Callable,
    args: tuple = (),
    kwargs: dict | None = None,
    max_attempts: int = 4,
    base_sleep: float = 15.0,
    logger: logging.Logger | None = None,
    label: str = "",
) -> Any:
    """
    Call fn(*args, **kwargs). On TransientError: sleep with exponential
    backoff + jitter and retry up to max_attempts. On PermanentError or
    unexpected exception after max_attempts: re-raise.
    """
    kwargs = kwargs or {}
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except PermanentError:
            raise
        except TransientError as e:
            last_exc = e
            if attempt == max_attempts:
                break
            wait = base_sleep * (2 ** (attempt - 1)) + random.uniform(0, 5)
            msg = f"[retry {attempt}/{max_attempts}] TransientError on {label}: {e}. Sleeping {wait:.0f}s."
            if logger:
                logger.warning(msg)
            else:
                print(msg)
            time.sleep(wait)
        except Exception as e:
            last_exc = e
            if attempt == max_attempts:
                break
            wait = base_sleep * attempt + random.uniform(0, 3)
            msg = f"[retry {attempt}/{max_attempts}] Unexpected error on {label}: {e}. Sleeping {wait:.0f}s."
            if logger:
                logger.warning(msg)
            else:
                print(msg)
            time.sleep(wait)
    raise TransientError(f"All {max_attempts} attempts failed for {label}: {last_exc}") from last_exc


# ---------------------------------------------------------------------------
# Provenance enforcement  (NON-NEGOTIABLE)
# ---------------------------------------------------------------------------

def enforce_provenance(result: dict) -> dict:
    """
    If the result doesn't have two distinct parseable-data models, downgrade
    to single-model-preliminary. Never emits 'validated'. 'machine-verified'
    is the ceiling this harness assigns.

    Reads:
        result["provenance"]["generate_model"]   — model that generated
        result["provenance"]["verify_model"]     — model that verified
        result["provenance"]["verify_actually_answered"]  — bool (optional)

    Returns the (possibly downgraded) result dict.
    """
    prov = result.get("provenance") or {}
    gen_model  = prov.get("generate_model") or ""
    ver_model  = prov.get("verify_model") or ""
    ver_answered = prov.get("verify_actually_answered", True)

    two_distinct = (
        bool(gen_model) and bool(ver_model)
        and gen_model != ver_model
        and ver_answered
    )

    if not two_distinct and result.get("disposition") == "machine-verified":
        result["disposition"] = "single-model-preliminary"
        result["disposition_note"] = (
            "[Harness downgrade] machine-verified requires two distinct models with "
            f"parseable output. generate={gen_model or 'none'}, "
            f"verify={ver_model or 'none'}, verify_answered={ver_answered}."
        )
        result.setdefault("provenance", {})["harness_downgraded"] = True

    # Safety belt: never let "validated" out
    if result.get("disposition") == "validated":
        result["disposition"] = "machine-verified"
        result.setdefault("provenance", {})["note"] = (
            "Downgraded from 'validated' — this harness never emits validated. "
            "Machine-verified is below the attorney line."
        )

    return result


# ---------------------------------------------------------------------------
# Claude fallback verifier
# ---------------------------------------------------------------------------

def call_claude_fallback(prompt: str, max_tokens: int = 1000) -> dict:
    """
    Claude-haiku as fallback VERIFIER when GPT-4o (primary verifier) fails.
    Different provider from Gemini (generator) — satisfies independence rule.
    Returns parsed JSON dict or {"error": "..."}.
    """
    try:
        import anthropic
        import re
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        r = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": prompt + "\n\nReturn valid JSON only — no markdown fences.",
            }],
        )
        text = (r.content[0].text or "").strip()
        if not text:
            return {"error": "empty response"}
        # strip markdown fences if present
        text = re.sub(r"^```json?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Summary writer
# ---------------------------------------------------------------------------

def write_summary(
    protocol: str,
    run_id: str,
    results: list[dict],
    raw_output_path: Path,
    summary_dir: Path,
    log_path: Path,
    elapsed_secs: float,
) -> Path:
    """Write SUMMARY_<protocol>_<timestamp>.md to summary_dir."""
    summary_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    summary_path = summary_dir / f"SUMMARY_{protocol}_{ts}.md"

    total = len(results)
    mv  = sum(1 for r in results if r.get("disposition") == "machine-verified")
    smp = sum(1 for r in results if r.get("disposition") == "single-model-preliminary")
    na  = sum(1 for r in results if r.get("disposition") == "needs-attorney")
    pf  = sum(1 for r in results if r.get("disposition") == "permanent-failure")
    tf  = sum(1 for r in results if r.get("disposition") == "transient-failure")
    ci  = sum(1 for r in results if r.get("queue_routing") == "CONFIRM-INFERENCE")
    rc  = sum(1 for r in results if r.get("queue_routing") == "RE-CHARACTERIZE")
    wd  = sum(1 for r in results if r.get("queue_routing") == "WRONG-DOC")

    lines = [
        f"# Validation Summary — {protocol}",
        f"**Run ID:** {run_id}  ",
        f"**Completed:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        f"**Elapsed:** {elapsed_secs/60:.1f} min  ",
        f"**Raw output:** `{raw_output_path}`  ",
        f"**Log:** `{log_path}`  ",
        "",
        "## Results",
        "",
        f"| Grade | Count | % |",
        f"|-------|-------|---|",
        f"| machine-verified | {mv} | {mv/total:.0%} |" if total else "| (no units) | — | — |",
        f"| single-model-preliminary | {smp} | {smp/total:.0%} |" if total else "",
        f"| needs-attorney | {na} | {na/total:.0%} |" if total else "",
        f"| permanent-failure | {pf} | {pf/total:.0%} |" if total else "",
        f"| transient-failure (retry exhausted) | {tf} | {tf/total:.0%} |" if total else "",
        "",
        "## Attorney Queue Counts",
        "",
        f"- CONFIRM-INFERENCE: {ci}",
        f"- RE-CHARACTERIZE:   {rc}",
        f"- WRONG-DOC:         {wd}",
        "",
        "## Provenance",
        "",
        "- machine-verified is BELOW the attorney line. Nothing here is `validated`.",
        "- Per-case generate_model + verify_model in raw output JSON.",
        "",
        "## What Needs a Human",
        "",
    ]

    needs_human = [r for r in results
                   if r.get("disposition") in ("needs-attorney", "single-model-preliminary",
                                                "transient-failure", "permanent-failure")]
    if needs_human:
        for r in needs_human[:20]:  # cap at 20 in summary
            lines.append(f"- **{r.get('case_name','?')}** ({r.get('state','?')}): "
                         f"{r.get('disposition','?')} — {str(r.get('disposition_note',''))[:120]}")
        if len(needs_human) > 20:
            lines.append(f"- … and {len(needs_human)-20} more. See raw output.")
    else:
        lines.append("- None — all units machine-verified or needs-attorney only.")

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path


# ---------------------------------------------------------------------------
# Validation Harness  (main orchestrator)
# ---------------------------------------------------------------------------

class ValidationHarness:
    """
    Orchestrates running a protocol across a list of units with:
      - Checkpoint-based resumption
      - Retry with backoff for transient errors
      - Provenance enforcement per unit
      - Timestamped logging
      - Completion summary
    """

    def __init__(
        self,
        protocol_name: str,
        units: list[dict],
        run_id: str,
        checkpoint_dir: Path,
        log_dir: Path,
        results_dir: Path,
        output_dir: Path,
        inter_case_sleep: float = 10.0,
        max_retry_attempts: int = 4,
        retry_base_sleep: float = 15.0,
        fresh: bool = False,
    ):
        self.protocol_name     = protocol_name
        self.units             = units
        self.run_id            = run_id
        self.inter_case_sleep  = inter_case_sleep
        self.max_retry_attempts = max_retry_attempts
        self.retry_base_sleep  = retry_base_sleep

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
        ckpt_path = checkpoint_dir / f"{protocol_name}_{run_id}.ckpt.json"
        log_path  = log_dir / f"{protocol_name}_{ts}.log"

        self.log_path     = log_path
        self.results_dir  = results_dir
        self.output_dir   = output_dir
        self.checkpoint   = Checkpoint(ckpt_path)
        self.logger       = make_logger(f"harness.{protocol_name}", log_path)

        if fresh and ckpt_path.exists():
            ckpt_path.unlink()
            self.checkpoint = Checkpoint(ckpt_path)
            self.logger.info("[fresh] Deleted checkpoint — starting clean.")

        self.checkpoint.set_meta("protocol", protocol_name)
        self.checkpoint.set_meta("run_id", run_id)
        self.checkpoint.set_meta("total_units", len(units))

    def run(self, run_unit_fn: Callable[[dict], dict]) -> list[dict]:
        """
        Main loop. Calls run_unit_fn(unit) for each unit not yet in checkpoint.
        Returns list of all results (completed + resumed).
        """
        total = len(self.units)
        self.logger.info(f"Starting {self.protocol_name} | run_id={self.run_id} | "
                         f"{total} units | sleep={self.inter_case_sleep}s between cases")
        start_time = time.time()

        pending = [u for u in self.units if not self.checkpoint.is_done(u["unit_id"])]
        resumed = total - len(pending)
        if resumed:
            self.logger.info(f"Resuming — {resumed} units already checkpointed, {len(pending)} remaining.")

        for i, unit in enumerate(pending, start=resumed + 1):
            uid   = unit["unit_id"]
            label = f"{unit.get('state','?')} / {unit.get('case_name','?')}"
            self.logger.info(f"[{i}/{total}] {label}")

            try:
                result = run_with_retry(
                    fn=run_unit_fn,
                    args=(unit,),
                    max_attempts=self.max_retry_attempts,
                    base_sleep=self.retry_base_sleep,
                    logger=self.logger,
                    label=label,
                )
            except TransientError as e:
                self.logger.error(f"[{i}/{total}] TRANSIENT-FAILURE (retries exhausted): {label} — {e}")
                result = {
                    "unit_id": uid,
                    "state": unit.get("state"),
                    "case_name": unit.get("case_name"),
                    "disposition": "transient-failure",
                    "disposition_note": str(e),
                    "provenance": {"harness_exhausted_retries": True},
                }
            except PermanentError as e:
                self.logger.error(f"[{i}/{total}] PERMANENT-FAILURE: {label} — {e}")
                result = {
                    "unit_id": uid,
                    "state": unit.get("state"),
                    "case_name": unit.get("case_name"),
                    "disposition": "permanent-failure",
                    "disposition_note": str(e),
                    "provenance": {"harness_permanent_skip": True},
                }
            except Exception as e:
                tb = traceback.format_exc()
                self.logger.error(f"[{i}/{total}] UNEXPECTED: {label} — {e}\n{tb}")
                result = {
                    "unit_id": uid,
                    "state": unit.get("state"),
                    "case_name": unit.get("case_name"),
                    "disposition": "permanent-failure",
                    "disposition_note": f"Unexpected exception: {e}",
                    "provenance": {"traceback": tb[:500]},
                }

            result = enforce_provenance(result)
            self.checkpoint.record(uid, result)
            self.logger.info(f"[{i}/{total}] → {result['disposition']} | "
                             f"queue={result.get('queue_routing','—')}")

            if i < total:
                time.sleep(self.inter_case_sleep)

        all_results = self.checkpoint.all_results()
        elapsed = time.time() - start_time

        # Write raw output JSON
        self.output_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        raw_path = self.output_dir / f"{self.protocol_name}_{today}_{self.run_id}.json"
        with open(raw_path, "w") as f:
            json.dump({
                "protocol": self.protocol_name,
                "run_id": self.run_id,
                "run_date": today,
                "runner_version": "harness-v1",
                "total_units": total,
                "machine_verified": sum(1 for r in all_results if r.get("disposition") == "machine-verified"),
                "single_model_preliminary": sum(1 for r in all_results if r.get("disposition") == "single-model-preliminary"),
                "needs_attorney": sum(1 for r in all_results if r.get("disposition") == "needs-attorney"),
                "elapsed_secs": round(elapsed),
                "results": all_results,
            }, f, indent=2, ensure_ascii=False)

        summary_path = write_summary(
            protocol=self.protocol_name,
            run_id=self.run_id,
            results=all_results,
            raw_output_path=raw_path,
            summary_dir=self.results_dir,
            log_path=self.log_path,
            elapsed_secs=elapsed,
        )

        self.logger.info(f"Run complete. Raw: {raw_path}")
        self.logger.info(f"Summary: {summary_path}")
        self.logger.info(f"⚠️ machine-verified is below the attorney line.")

        return all_results
