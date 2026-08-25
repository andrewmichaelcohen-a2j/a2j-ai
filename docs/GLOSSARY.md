# CJaC — Glossary

Shared vocabulary used across the validation record, roadmap, and specs. One line each; follow the link for the full definition where one exists.

**Band 1 — deterministic.** Notice periods, day counts, service methods, statutory thresholds. Outcomes are freezable ground truth. This is where all current validation claims live. See [`OPEN_QUESTIONS_AND_LIMITATIONS.md`](OPEN_QUESTIONS_AND_LIMITATIONS.md) Q10.

**Band 2 — structured-subjective.** Habitability, retaliation, waiver, and similar defenses: the *application* is judgment, but the *structure* is lookup-able law (elements, burdens of proof, statutory presumptions, relevant-evidence checklists). Ground truth here is process-correctness, not outcome-correctness — did the system identify the right elements and refuse to predict the result. Currently a hypothesis, not yet proven; see Q10 and the planned CA §1942.5 retaliation proof cycle.

**Band 3 — genuinely discretionary.** Relief from forfeiture, credibility determinations, judicial discretion. CJaC's only honest product here is the boundary marker itself — flagging that a judgment call exists and naming what courts weigh, never predicting the outcome. This is a permanent boundary, not a target to eventually cross.

**AMPVR — attorney-minutes per validated rule.** The core efficiency metric for the ratification pipeline: attorney time spent per rule that reaches VALIDATED status. Success is a falling AMPVR at constant-or-better validation quality, not falling AMPVR alone. Defined in `docs/directives/COWORK_DIRECTION_DIRECTION_E_20260724.md` Task 3.

**Ratification-queue-health.** A metric tracking the state of the unratified-proposal queue: count, age distribution, inflow/outflow rate. Used to throttle proposal generation when the queue ages past a threshold, so throughput on one end doesn't outrun attorney review capacity on the other.

**Tier 1 (Narrative-perturbation testing).** A lower-bound testing method: the same underlying fact pattern is restated in varied narrative forms (register, order, omitted-vs-implied facts) to test whether the system's outcome is stable under surface rewording rather than dependent on a specific phrasing. Defined in `docs/directives/COWORK_DIRECTION_DIRECTION_E_20260724.md` Task 1.

**Tier 2 (Interactive elicitation harness).** A lower-bound testing method: a multi-turn harness that elicits facts from a simulated user conversationally, rather than being handed a complete fact pattern up front, to test whether the system asks the right questions when facts are incomplete. Defined in `docs/directives/COWORK_DIRECTION_DIRECTION_E_20260724.md` Task 2.

**VALIDATED / status ladder.** See [`STATUS_LABELS.md`](STATUS_LABELS.md) for the full advancement rules and definitions of each status a rule can hold.
