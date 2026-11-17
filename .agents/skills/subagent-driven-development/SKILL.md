---
name: subagent-driven-development
description: Orchestrate parallel and staged multi-agent execution, break down complex work streams into discrete subagent briefs, enforce automated review loops, and synthesize results. Use when delegating tasks across specialized agents.
---

# SKILL: Subagent-Driven Development & Orchestration

> **Origin Repository:** https://github.com/obra/superpowers  
> **Source License:** MIT License  
> **Attribution:** Adapted from Jesse Vincent's `superpowers` agentic framework for Antigravity Multi-Agent Systems.  
> **Target Owner:** ARKA (Chief Executive & Strategy Officer) | Shared: All Directors

---

## 1. PURPOSE & OBJECTIVE
To provide a disciplined, repeatable methodology for decomposing complex engineering, research, and corporate tasks into bounded, independent work packages delegated to autonomous subagents, followed by mandatory review loops and executive aggregation.

## 2. SCOPE
- Defining clear subagent contracts (context, bounds, definition of done).
- Managing execution lifecycles (serial pipelines vs. concurrent waves).
- Enforcing subagent verification gates before accepting deliverables.
- Synthesizing heterogeneous agent outputs into a unified deliverable.

## 3. METHODOLOGY & PROTOCOL
1. **Context Boundary Enforcement:** Never pass unbounded conversation history to a subagent. Provide only the minimum necessary briefing, reference links, and target output schemas.
2. **Deterministic Role Assignment:** Pin subagents to explicit roles and specific skill subsets.
3. **Double-Check Review Gate:** A subagent's output must never be marked `COMPLETED` without verification against the initial brief.

## 4. STEP-BY-STEP PROCEDURE
1. **Draft Assignment Brief:** Detail exact task ID, domain, objective, constraints, and target output path.
2. **Dispatch Subagent:** Launch subagent with tool access restricted to its competency.
3. **Monitor Execution State:** Track transitions (`ASSIGNED` -> `IN PROGRESS` -> `UNDER REVIEW`).
4. **Peer Review Trigger:** Route draft to an assigned peer reviewer agent.
5. **Reconciliation & Merge:** Verify no contradictions, update activity ledger, and integrate into main deliverable.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- Zero cross-talk or role pollution between subagents.
- All generated files must be saved under configured project paths.
- All state changes logged to `logs/activity_log.json`.

## 6. CONSTRAINTS & SECURITY RULES
- Do not grant shell/destructive execution privileges to untrusted subagents.
- Subagents must not access or output credentials or sensitive tokens.
- Halts execution and flags human if subagent triggers an unrecoverable failure.

## 7. EXAMPLE USAGE
ARKA delegates market sizing to NAYA and server topology to RAKA concurrently, gathers their drafts, and verifies them before initiating SEKAR's financial model.
