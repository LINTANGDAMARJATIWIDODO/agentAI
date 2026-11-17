---
name: requesting-code-review
description: Prepare structured, context-rich code review submissions, execute rigorous peer reviews covering architecture, performance, security, and maintainability, and document actionable critique. Use during code reviews.
---

# SKILL: Enterprise Code Review & Critique Protocol

> **Origin Repository:** https://github.com/obra/superpowers  
> **Source License:** MIT License  
> **Attribution:** Adapted from `superpowers` (Jesse Vincent) for Enterprise Peer Review.  
> **Target Owner:** RAKA (Director of Technology) | Shared: ARKA (CEO / QA)

---

## 1. PURPOSE & OBJECTIVE
To elevate software quality, eliminate security vulnerabilities, maintain architectural consistency, and enforce documentation standards through structured, objective, and empathetic peer code reviews.

## 2. SCOPE
- Pull request (PR) reviews, changeset audits, architectural compliance checks, security vulnerability screening, and test coverage evaluation.

## 3. REVIEW PILLARS (THE 5 CHECKPOINTS)
1. **Correctness & Logic:** Does the code solve the intended problem accurately? Are edge cases handled?
2. **Security & Vulnerabilities:** Are inputs sanitized? Any SQLi, XSS, SSRF, or exposed secrets?
3. **Performance & Scalability:** Are database queries indexed? Any N+1 query problems, unbounded loops, or memory leaks?
4. **Readability & Maintainability:** Are variables clearly named? Does it follow SOLID and Clean Code principles?
5. **Test Completeness:** Are unit and integration tests present and passing?

## 4. STEP-BY-STEP PROCEDURE
1. **Self-Review First:** The author must inspect their own diff, verify test execution, and remove debug logs before requesting review.
2. **Prepare Review Packet:** Include summary of changes, rationale, linked task/issue ID, and testing evidence.
3. **Reviewer Audit:** Peer reviewer walks through diff systematically using the 5 Checkpoints.
4. **Issue Constructive Feedback:** Clearly tag comments: `[BLOCKER]`, `[SUGGESTION]`, `[QUESTION]`, or `[NITPICK]`.
5. **Resolution & Sign-off:** Author resolves all blockers, reviewer validates adjustments and issues formal approval.

## 5. QUALITY STANDARDS
- All blocker comments must include an explicit explanation of why it is problematic and a suggested alternative.
- Approvals must state what was verified (e.g. "Verified unit tests, security posture, and error handling").

## 6. CONSTRAINTS
- Never approve code with failing tests or unaddressed security warnings.
- Avoid subjective stylistic bikeshedding; defer formatting to automated linters/formatters.
