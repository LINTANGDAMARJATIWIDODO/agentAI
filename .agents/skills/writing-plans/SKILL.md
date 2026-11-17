---
name: writing-plans
description: Author actionable, bite-sized implementation plans and execution roadmaps. Break initiatives into incremental tasks with explicit verification steps and rollback strategies. Use when planning complex features or projects.
---

# SKILL: Technical Implementation Planning & Roadmapping

> **Origin Repository:** https://github.com/obra/superpowers  
> **Source License:** MIT License  
> **Attribution:** Adapted from `superpowers` (Jesse Vincent) for Enterprise Planning.  
> **Target Owner:** ARKA (CEO) | DIMAS (Director of Operations)

---

## 1. PURPOSE & OBJECTIVE
To prevent project drift, unmanaged scope expansion, and execution paralysis by structuring complex projects into small, verifiable, incremental work steps where each step leaves the system in a working, testable state.

## 2. SCOPE
- Technical specs, architectural migration plans, sprint task breakdowns, and cross-divisional execution roadmaps.

## 3. PLANNING PRINCIPLES
1. **Incremental Completeness:** Each step must be self-contained and verifiable.
2. **Explicit Verification Check:** Every task must specify exactly how to verify success before moving to the next.
3. **Risk & Rollback Pre-Planning:** Identify potential failure points upfront with pre-defined rollback actions.

## 4. STEP-BY-STEP PROCEDURE
1. **Context & Goals:** Clearly state the problem, business outcome, non-goals, and constraints.
2. **Architectural Decisions:** Document key technical or operational choices and their rationale.
3. **Task Breakdown:** Split the work into numbered phases and bite-sized steps (15-60 min each).
4. **Define Verification Steps:** Write the exact commands, tests, or inspection criteria for each step.
5. **Review & Approval:** Get sign-off from relevant division heads before starting execution.

## 5. STANDARD PLAN TEMPLATE
- **Overview & Objective**
- **Prerequisites & Dependencies**
- **Phase Breakdown (Step 1, Step 2, ... Step N)**
  - *Action to take*
  - *Files touched*
  - *Verification command / criteria*
- **Rollback / Contingency Strategy**
- **Acceptance Sign-off Criteria**

## 6. CONSTRAINTS
- Never create monolithic "black box" tasks (e.g. "Implement entire backend").
- Do not plan more than 2-3 sprints ahead without empirical feedback checkpoints.
