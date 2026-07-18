# Dispatcher launchd Plist — Hardening Proposal (B-4)

*Cowork Change Directive — Dispatcher Resilience & Overnight-Environment Forensics, 2026-07-16, Part B item B-4. This is a PROPOSAL only — Cowork has not installed or modified the live launch agent. Installing launch agents and changing power settings are Andy-side actions (his machine, his call), per the directive's Part A / Part B scope split.*

## Why this doc exists

Three consecutive dispatcher-side missed fires (07-16, 07-17, 07-18) were diagnosed jointly with Andy on 2026-07-17: the Mac's idle-sleep timer was set to 1 minute, and lid-close (clamshell) sleep was also in play — either one kills the machine's network (and, if severe enough, the ability for launchd to fire at all) before the nightly 02:15 job runs. Andy has already applied `sudo pmset -c sleep 0` (disables idle sleep while on AC power) and adopted the lid-open-overnight practice. This document proposes the remaining belt-and-suspenders options on the launchd/pmset side, for Andy to evaluate and apply at his discretion — none of it is required if the sleep-timer + lid-open fix proves sufficient on its own over the next several nights (now directly measurable via B-1/B-2/B-3's heartbeat log — see `classify_last_night()` in `dispatch.py`).

## Current plist (`rules/validation/com.cjac.validation.plist`) — unchanged, for reference

- `StartCalendarInterval`: Hour=2, Minute=15 (local time). Retained as-is — no proposed change to the fire time itself.
- `ProgramArguments`: `/usr/bin/python3 dispatch.py` (single-shot mode — no `--drain` flag, so this always runs `main_single()`, the now-self-evidencing path).
- `RunAtLoad`: `false`. This is deliberate and should stay `false` — see "Why not RunAtLoad" below.
- No `KeepAlive` key present. This is deliberate and should stay absent — see "Why NOT KeepAlive" below.

## Proposed additions (Andy applies, if desired)

### 1. `AbandonProcessGroup` → `true`

```xml
<key>AbandonProcessGroup</key>
<true/>
```

**Rationale:** without this, launchd's default behavior on agent unload/stop is to send `SIGTERM` to the entire process group spawned by the job, including any grandchild processes `dispatch.py` itself spawns (the `caffeinate -ims python3 ...` subprocess chain for the actual protocol/scorer runner). Setting `AbandonProcessGroup` to `true` means that if the launchd agent is reloaded or the Mac is put to sleep mid-run, an in-flight job subprocess is not forcibly killed as a side effect of launchd's own bookkeeping — it either completes or dies from the actual sleep/network interruption, not from launchd cleanup. This makes `finalize_job()`'s success/failure classification (and the new B-1 ABORTED heartbeat) reflect what actually happened to the job, not an artifact of process-group signaling.

### 2. Do NOT add `KeepAlive`

`KeepAlive` (in any form — `true`, or the dictionary form with `SuccessfulExit`/`Crashed` conditions) tells launchd to treat the agent as a long-running daemon: restart it immediately whenever it exits, keep it running continuously, etc. That is the wrong model here. `dispatch.py`'s single-shot mode is a **scheduled job**, not a daemon — it is meant to run once at 02:15, do at most one unit of work, and exit. Adding `KeepAlive` would fight `StartCalendarInterval` (launchd would keep relaunching the process outside the scheduled window, defeating the whole point of the daytime-only guardrails already built into `dev_set_monitor.py` and any future scorer/protocol jobs with similar windows) and would turn a single missed-fire diagnosis problem into a much harder "why is this running constantly" problem. **Recommendation: leave `KeepAlive` absent, as it is today.**

### 3. Why not `RunAtLoad`

`RunAtLoad=true` would fire the job immediately whenever the agent is loaded (e.g., on every login/reboot), in addition to the scheduled 02:15 fire. This is tempting as a way to "catch up" a missed night, but it's the wrong fix for the wrong layer: it would fire during the day (violating the scorer's own daytime/evening self-throttle is fine, since that guardrail is enforced in `dev_set_monitor.py` itself — but a `protocol`/`l2_module` job with no such self-throttle would run at an arbitrary time of day, including possibly while Andy is actively using the Mac for other things). **Recommendation: leave `RunAtLoad=false`, as it is today.** The correct fix for "missed fire" is making the machine reliably awake at 02:15 (below), not making the job willing to run at any time.

### 4. Companion `pmset repeat wakeorpoweron` (only if B-1/B-2/B-3 heartbeat data shows continued `fired-late-on-wake` classifications after the sleep-timer fix)

If, after a week or two of the `sudo pmset -c sleep 0` + lid-open fix, `python3 rules/validation/dispatch.py --heartbeat-status` still shows `fired-late-on-wake` nights (i.e., the machine is still asleep at 02:15 for some other reason — e.g. a night the lid genuinely does get closed), the most direct fix is to have the Mac schedule its own wake a few minutes before the job needs to run, independent of whatever put it to sleep:

```
sudo pmset repeat wakeorpoweron MTWRFSU 02:10:00
```

This tells the Mac's firmware to wake (or power on, if fully off) at 02:10 every day, giving a 5-minute margin before the 02:15 launchd fire. This is a real hardware/firmware wake, not a launchd construct, so it works even through a full sleep that `AbandonProcessGroup`/`KeepAlive` settings can't reach. It does **not** override lid-close (clamshell) sleep by itself — the lid-open practice is still needed on nights the job must run, unless an external display/keyboard/mouse is connected (which macOS treats as clamshell-mode-eligible while on power).

To remove it later: `sudo pmset repeat cancel`.

**Recommendation: hold this in reserve.** Applying it now, before there's heartbeat evidence the sleep-timer fix was insufficient, adds a second moving part to a problem that may already be solved. The heartbeat log (B-1/B-2/B-3) now gives a direct, no-guesswork way to tell whether it's needed — check `classify_last_night()`'s output over the next several mornings before deciding.

## Summary of recommendation

| Change | Recommend applying now? | Why |
|---|---|---|
| `AbandonProcessGroup: true` | Yes, low-risk | Prevents launchd cleanup from masquerading as a job failure in the new ABORTED heartbeat classification. |
| Add `KeepAlive` | **No** | Wrong model — this is a scheduled job, not a daemon. Would fight `StartCalendarInterval` and the daytime-only guardrails. |
| Change `RunAtLoad` to `true` | **No** | Would fire at arbitrary times outside the intended window; the right fix is a reliable wake, not a willing-to-run-anytime job. |
| `pmset repeat wakeorpoweron 02:10:00` | Hold in reserve | Apply only if heartbeat data (B-3) shows the sleep-timer fix wasn't sufficient. |

*This proposal does not modify `rules/validation/com.cjac.validation.plist` in the repo or the installed `~/Library/LaunchAgents/com.cjac.validation.plist` on Andy's machine. If Andy wants item 1 applied, the concrete diff is a two-line addition inside the existing `<dict>` block; Cowork can prepare that diff on request.*

---
*Copyright 2026 Andrew M Cohen. Apache 2.0.*
