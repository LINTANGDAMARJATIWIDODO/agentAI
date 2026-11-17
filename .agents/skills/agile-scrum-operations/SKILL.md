---
name: agile-scrum-operations
description: Govern enterprise Agile Scrum execution, sprint backlogs, user story estimation (Story Points), daily standup tracking, and retrospectives. Use when managing sprints, backlogs, or agile ceremonies.
---

# SKILL: Enterprise Agile Scrum Operations & Sprint Governance

> **Origin Repository:** https://github.com/bughunt8/skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `bughunt8/skills` Operations & Execution category.  
> **Target Owner:** DIMAS (Director of Operations & Business Growth)

---

## 1. PURPOSE & OBJECTIVE
To enforce a structured, predictable, and transparent 2-week sprint development cadence across multi-agent engineering and cross-divisional initiatives, maximizing velocity while preserving quality.

## 2. SCOPE
- Product backlog grooming, sprint planning, user story authoring with acceptance criteria (Gherkin syntax), velocity tracking, sprint burn-down analysis, and retrospective action items.

## 3. AGILE GOVERNANCE CADENCE (2-WEEK SPRINT CYCLE)
- **Day 1: Sprint Planning:** ARKA & DIMAS review backlog, size stories, and commit to sprint goal.
- **Day 2-9: Sprint Execution:** Parallel daily standup checkpoints (`What was done`, `What is planned`, `Blockers`).
- **Day 10: Sprint Review & Demo:** Present completed deliverables (`Definition of Done` verified) to stakeholders.
- **Day 10: Retrospective:** Document `Keep Doing`, `Stop Doing`, and `Start Doing` improvements.

## 4. USER STORY & ACCEPTANCE CRITERIA STANDARD (GHERKIN)
```gherkin
Feature: Enterprise Activity Audit Log

  Scenario: Task state transition is recorded immutably
    Given an active task with ID "TASK-101"
    When ARKA updates the task status to "COMPLETED"
    Then the task status in "logs/activity_log.json" becomes "COMPLETED"
    And a timestamp and verification signature are appended
```

## 5. QUALITY STANDARDS & DEFINITION OF DONE (DOD)
A user story is only marked **Done** when:
1. Code/document adheres to corporate style guides.
2. 100% of unit tests pass with required coverage.
3. Peer review is completed and approved.
4. Documentation is updated.

## 6. CONSTRAINTS
- Never bring unrefined stories into an active sprint without acceptance criteria.
- Protect sprint scope from mid-sprint unplanned disruptions without explicit ARKA sign-off.
