---
name: test-driven-development
description: Enforce strict Red-Green-Refactor development cycles. Author automated tests that fail before writing implementation code, verify edge cases, and eliminate regressions. Use when authoring or refactoring software modules.
---

# SKILL: Test-Driven Development (TDD) Protocol

> **Origin Repository:** https://github.com/obra/superpowers  
> **Source License:** MIT License  
> **Attribution:** Adapted from `superpowers` (Jesse Vincent) for Enterprise Python & TypeScript environments.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To guarantee zero-regression software development by requiring tests to be written, executed, and observed to fail *prior* to writing the implementation code, followed by writing the minimal code needed to pass, and subsequent refactoring.

## 2. SCOPE
- Unit testing, integration testing, and API contract validation.
- Frameworks: `pytest`, `unittest`, `Jest`, `Vitest`.
- Enforcing test coverage and failure-mode verification.

## 3. METHODOLOGY: THE RED-GREEN-REFACTOR CYCLE
1. **RED:** Write a test describing the desired behavior. Execute it. Confirm that it **fails** for the expected reason (e.g. missing function, assertion failure).
2. **GREEN:** Write the absolute simplest implementation code that satisfies the test. Re-execute the test suite. Confirm all tests **pass**.
3. **REFACTOR:** Clean up code structure, enhance readability, optimize performance, and remove duplication while ensuring tests remain **green**.

## 4. STEP-BY-STEP PROCEDURE
1. **Define Test Scenarios:**
   - Happy path (standard operational input).
   - Edge cases (null/empty inputs, boundary values, type mismatches).
   - Error cases (network timeouts, disk errors, unauthorized access).
2. **Create Test File:** Place in `tests/test_<module>.py` or `tests/<module>.test.ts`.
3. **Execute & Observe Failure:** Run test runner (e.g. `pytest tests/test_<module>.py`).
4. **Implement Code:** Write minimal logic in the target module.
5. **Verify Suite:** Run full test suite to guarantee no regressions.

## 5. QUALITY STANDARDS & METRICS
- Minimum 85% branch coverage on core business logic.
- Tests must be completely deterministic (no reliance on random unseeded data or live third-party network services).
- Test execution must be fast (< 5 seconds for unit suite).

## 6. CONSTRAINTS & SECURITY RULES
- Never mock away the actual behavior being tested (over-mocking antipattern).
- Do not commit disabled or skipped tests without explicit documented defect tracking.
- Sensitive environment secrets must be replaced with dummy test tokens in test suites.

## 7. EXAMPLE USAGE
RAKA writes `test_orchestrator.py` asserting that invalid task states throw `ValueError` before implementing the status transition validation function.
