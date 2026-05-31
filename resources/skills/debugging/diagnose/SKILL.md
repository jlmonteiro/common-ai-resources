---
name: "diagnose"
description: "Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says 'diagnose this', 'debug this', reports a bug, says something is broken/throwing/failing, 'troubleshoot this', or describes a performance regression."
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

## Prerequisites

- Read the project's `project-context.md` for a mental model of relevant modules
- Search the **testing** knowledge base for test structure conventions
- Search the **observability** knowledge base for instrumentation patterns

## Phase 1 — Build a Feedback Loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause.

Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.

### Ways to construct one — try in order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e
2. **HTTP script** against a running dev server
3. **CLI invocation** with fixture input, diffing stdout against known-good
4. **Headless browser script** — drives UI, asserts on DOM/console/network
5. **Replay a captured trace** — save a real request/event, replay in isolation
6. **Throwaway harness** — minimal subset of the system exercising the bug path
7. **Property/fuzz loop** — 1000 random inputs looking for the failure mode
8. **Bisection harness** — automate "boot at state X, check, repeat" for `git bisect run`
9. **Differential loop** — same input through old vs new version, diff outputs

### Iterate on the loop

- Can I make it faster? (Cache setup, skip unrelated init, narrow scope)
- Can I make the signal sharper? (Assert on specific symptom, not "didn't crash")
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem)

### Non-deterministic bugs

Goal: raise reproduction rate until debuggable. Loop 100×, parallelise, add stress, narrow timing windows. A 50%-flake is debuggable; 1% is not.

### When you cannot build a loop

Stop and say so. List what you tried. Ask the user for:
- Access to the reproducing environment
- A captured artifact (log dump, core dump, screen recording)
- Permission to add temporary instrumentation

Do NOT proceed to Phase 2 without a loop.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear. Confirm:

- [ ] The loop produces the failure the **user** described — not a different nearby failure
- [ ] Reproducible across multiple runs (or high enough rate for non-deterministic)
- [ ] Exact symptom captured (error message, wrong output, timing)

Do not proceed until reproduced.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any. Each must be falsifiable:

> "If X is the cause, then changing Y will make the bug disappear / changing Z will make it worse."

If you cannot state the prediction, discard the hypothesis.

Show the ranked list to the user before testing — they often have domain knowledge that re-ranks instantly.

## Phase 4 — Instrument

Each probe maps to a specific prediction from Phase 3. Change one variable at a time.

Tool preference:
1. **Debugger / REPL** — one breakpoint beats ten logs
2. **Targeted logs** at boundaries that distinguish hypotheses
3. Never "log everything and grep"

Tag every debug log with a unique prefix: `[DEBUG-a4f2]`. Cleanup becomes a single grep.

For **performance regressions**: logs are usually wrong. Establish a baseline measurement (profiler, timing harness, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + Regression Test

Write the regression test **before the fix** (TDD):

1. Turn the minimised repro into a failing test
2. Watch it fail
3. Apply the fix
4. Watch it pass
5. Re-run the Phase 1 loop against the original scenario

If no correct test seam exists, document it — the architecture is preventing the bug from being locked down.

## Phase 6 — Cleanup + Post-Mortem

Before declaring done:

- [ ] Original repro no longer reproduces
- [ ] Regression test passes (or absence of seam documented)
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] Correct hypothesis stated in commit message

Then ask: **what would have prevented this bug?** If the answer involves architectural change, document the recommendation in the PR.
