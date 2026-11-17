---
name: systematic-debugging
description: Execute systematic multi-phase root-cause debugging. Reproduce bugs with minimal test cases, formulate and test hypotheses, isolate defects, and verify fixes without introducing collateral regressions. Use when fixing errors.
---

# SKILL: Systematic Root-Cause Debugging Protocol

> **Origin Repository:** https://github.com/obra/superpowers  
> **Source License:** MIT License  
> **Attribution:** Adapted from `superpowers` (Jesse Vincent) for Enterprise Software Engineering.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To eliminate guessing, trial-and-error patching, and superficial workarounds by enforcing a strict scientific method for discovering, isolating, explaining, and permanently resolving software defects.

## 2. SCOPE
- Error stack trace analysis, runtime exceptions, logic bugs, race conditions, memory leaks, and performance bottlenecks across backend, frontend, and distributed workers.

## 3. THE 4-PHASE INVESTIGATION METHODOLOGY
1. **Phase 1: Deterministic Reproduction:** Create an automated, minimal reproducible test case. If you cannot reproduce the bug reliably, you cannot prove you fixed it.
2. **Phase 2: Hypothesis Formulation:** Formulate 1-3 falsifiable hypotheses regarding the root cause based on evidence, stack traces, and variable states.
3. **Phase 3: Controlled Experimentation:** Test each hypothesis by inspecting state, inserting structured logging, or running an isolated debugger without altering production logic.
4. **Phase 4: Targeted Fix & Regression Proof:** Apply the minimal required fix, run the reproduction test to prove it now passes, and run the entire regression test suite.

## 4. STEP-BY-STEP PROCEDURE
1. **Analyze Bug Report:** Extract exact error message, stack trace, input payload, and environment details.
2. **Write Failing Test:** Encode the exact reproduction scenario into an automated test.
3. **Trace Execution Path:** Walk backward through call stack from the failure point to the source of corrupted state.
4. **Identify Flaw:** Pinpoint the exact line and logic violation (e.g. unhandled NoneType, off-by-one, race condition).
5. **Implement Remediation:** Correct the root cause cleanly.
6. **Verify Fix:** Confirm reproduction test passes and all existing tests remain green.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- No fix is accepted without an accompanying regression test that previously failed.
- Root cause must be documented in the commit/log message with "Why it broke" and "How this fixes it".
- No suppression of errors (e.g. empty try/except).

## 6. CONSTRAINTS
- Never apply shotgun debugging (changing multiple files blindly hoping the bug disappears).
- Never modify tests to pass the broken code without formal specification approval.

## 7. EXAMPLE USAGE
RAKA resolves a JSON serialization crash in `orchestrator.py` by isolating the non-serializable datetime object and implementing a custom ISO encoder.
