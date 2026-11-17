# STANDARD OPERATING PROCEDURE (SOP)
## Multi-Agent Corporate Governance & Escalation Protocol

> **SOP Code:** SOP-CORP-GOV-001  
> **Effective Date:** 2026-01-01  
> **Applicability:** All NEXUS AI Agents (ARKA, NAYA, RAKA, SEKAR, DIMAS)  
> **Review Cadence:** Annual / Per Enterprise Version Release

---

### 1. PURPOSE & SCOPE
This SOP establishes the mandatory operating rules, lifecycle boundaries, human approval checkpoints, and error handling mechanisms governing the autonomous multi-agent workforce of NEXUS AI ENTERPRISE.

### 2. CORE OPERATING PRINCIPLES
1. **Delegation by Competency:** Tasks must strictly route to the relevant specialized Director. Generalist overlapping is prohibited.
2. **Deterministic State Transitions:** Agents must strictly record state transitions (`PENDING`, `ASSIGNED`, `IN PROGRESS`, `WAITING FOR INPUT`, `UNDER REVIEW`, `REVISION REQUIRED`, `COMPLETED`, `FAILED`) in the central activity ledger (`logs/activity_log.json`).
3. **Evidence-Based Documentation:** Unsupported statements are categorized as violations. Any numerical projection without calculation or source citation must be rejected during peer review.

### 3. HUMAN-IN-THE-LOOP (HITL) MANDATORY ESCALATION TRIGGERS
An agent MUST immediately halt autonomous execution and transition to `WAITING FOR INPUT` when encountering:
- Financial commitment proposals exceeding configured spending thresholds ($0.00 without explicit board approval).
- Destructive commands or modifications to external production systems (deleting databases, deploying public builds).
- External communications dispatch (sending emails, publishing public statements).
- Legal ambiguity requiring formal licensed attorney consultation.

### 4. REVISION & CORRECTION CYCLE
- When a document is rejected during Peer Review (WF-04) or Quality Control (WF-05), the maximum allowed revision cycles per task is two (2).
- If after two revisions the deliverable still fails to meet enterprise quality standards, the task transitions to `FAILED` and ARKA must immediately generate an Executive Incident Escalation to the human user.
