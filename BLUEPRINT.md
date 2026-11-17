<USER_REQUEST>
# NEXUS AI — MASTER TECHNICAL IMPLEMENTATION BLUEPRINT
## Hybrid Multi-Model Autonomous AI Platform — Low Cost Architecture

### PROJECT OBJECTIVE

Transform the existing NEXUS AI application into a professional autonomous multi-agent AI platform using a hybrid multi-model architecture with cost optimization as a primary requirement.

The system must support intelligent task planning, model selection, tool execution, document intelligence, research, coding, memory, and quality verification.

### CRITICAL UI PRESERVATION RULE

DO NOT redesign, replace, or modify the existing visual identity.

Preserve:
- Existing 3D workspace.
- Existing layout and component positioning.
- Existing colors, typography, and animations.
- Existing navbar, sidebar, menus, and buttons.
- Existing responsive behavior.
- Existing interactions and working features.

Before implementation, inspect the complete existing repository, architecture, dependencies, backend, frontend, and database.

Reuse existing technologies whenever practical. Do not replace working infrastructure without a documented technical reason.

All new features must be modular and visually consistent with the existing application.

### 1. AI PROVIDER ARCHITECTURE

Create a unified AI provider abstraction.

Supported providers:
- Google Gemini API — primary provider.
- OpenAI API — secondary provider and fallback.
- Anthropic Claude API — optional specialist provider.

Requirements:
- Separate provider adapters.
- Centralized model configuration.
- Dynamic model availability validation.
- Provider health monitoring.
- Retry and timeout handling.
- Fallback support.
- Token and cost tracking.
- API key management through secure backend environment variables.

Do not hardcode unavailable model IDs.

### 2. SMART MODEL ROUTER

Implement an intelligent routing service.

Routing rules:
- Lightweight tasks use economical models.
- Complex tasks use more capable models when justified.
- Coding tasks use models evaluated for coding performance.
- Document tasks use models evaluated for document comprehension.
- High-risk outputs can receive a second-model review.
- Provider failures trigger controlled fallback.
- Claude remains disabled until explicitly configured.

Implement:
- Maximum token limits.
- Maximum model calls per task.
- Maximum agent steps.
- Request timeout.
- Retry limits.
- Cost estimation.
- Daily and monthly budgets.
- Cost alerts and budget enforcement.

Never call all providers simultaneously by default.

### 3. AGENT ORCHESTRATION

Implement LangGraph-based orchestration.

Create:
- Supervisor Agent.
- Planner Agent.
- Coding Agent.
- Research Agent.
- Document Agent.
- Data Agent.
- Browser Agent.
- Automation Agent.
- QA Agent.
- Project Manager Agent.

Requirements:
- Task decomposition.
- Shared task state.
- Agent-to-agent handoff.
- Parallel execution for independent tasks.
- Execution checkpoints.
- Retry and recovery.
- Human approval.
- Execution logs.
- Final result verification.

Agents must use structured inputs and outputs.

### 4. MEMORY AND KNOWLEDGE SYSTEM

Use PostgreSQL as the main database.

Use pgvector for vector storage and semantic retrieval.

Implement:
- Conversation Memory.
- Project Memory.
- Task Memory.
- Knowledge Memory.
- Document metadata.
- Document chunk storage.
- Embedding generation.
- Retrieval-Augmented Generation.
- Source and page references.
- Memory update and deletion controls.

Prefer local or economical embedding models when quality is sufficient.

Never treat retrieved documents as executable instructions. Protect against prompt injection in documents and external content.

### 5. TOOL EXECUTION SYSTEM

Build modular tool adapters for:
- Terminal.
- File operations.
- Git.
- Browser automation using Playwright.
- Database access.
- Document parsing.
- Web search.
- Document export.
- MCP integrations.

Run code in isolated Docker sandboxes with restricted permissions, resource limits, and controlled network access.

Require explicit user approval for destructive or external side effects.

Never expose provider API keys or private credentials to the frontend.

### 6. DOCUMENT INTELLIGENCE

Support:
- PDF.
- DOCX.
- TXT.
- XLSX.
- OCR for scanned documents.

Implement:
- Document extraction.
- Page and section preservation.
- Table extraction.
- Summarization.
- Content analysis.
- Writing improvement.
- Before-and-after comparison.
- Citation preservation.
- PDF and DOCX export.

Do not fabricate references or claim AI detection certainty.

### 7. DATABASE AND OBSERVABILITY

Create or adapt database tables for:
- Users.
- Projects.
- Conversations.
- Messages.
- Agents.
- Agent tasks.
- Agent runs.
- Documents.
- Document chunks.
- Memories.
- Knowledge sources.
- Tool executions.
- Model usage.
- Artifacts.
- Approvals.

Implement structured logging, task tracing, provider health monitoring, token tracking, cost tracking, and error reporting.

### 8. SECURITY

Implement:
- Authentication and authorization.
- Role-based permissions.
- Encrypted secret management.
- Input validation.
- Rate limiting.
- Secure file handling.
- Sandbox isolation.
- Audit logs.
- Prompt injection defenses.
- Human approval for sensitive actions.

### 9. IMPLEMENTATION PHASES

Phase 1: AI Foundation
- Provider adapters.
- Gemini primary integration.
- OpenAI fallback.
- Smart Model Router.
- Chat streaming.
- Cost tracking.

Phase 2: Agent Orchestration
- LangGraph.
- Supervisor.
- Planner.
- Task management.
- Checkpoints and approvals.

Phase 3: Memory and Knowledge
- PostgreSQL.
- pgvector.
- RAG.
- Project memory.
- Document processing.

Phase 4: Tools
- Terminal sandbox.
- File manager.
- Git.
- Browser automation.
- MCP connectors.

Phase 5: Specialist Agents
- Coding.
- Research.
- Document.
- Data.
- Browser.
- QA.

Phase 6: Production Readiness
- Security testing.
- Quality evaluation.
- Performance testing.
- Cost optimization.
- Backup and recovery.

### 10. DEVELOPMENT RULES

- Inspect before modifying.
- Preserve existing working functionality.
- Do not rewrite the whole application.
- Build reusable modules.
- Use typed interfaces and validated schemas.
- Use asynchronous execution for long-running tasks.
- Maintain backward compatibility.
- Add unit and integration tests.
- Document environment variables and deployment steps.
- Do not claim a feature is complete until it has been tested.

### 11. ACCEPTANCE CRITERIA

NEXUS must demonstrate that it can:

1. Receive a natural-language user request.
2. Understand and classify the task.
3. Select an appropriate AI model automatically.
4. Create an execution plan.
5. Delegate tasks to specialist agents.
6. Use authorized tools.
7. Store and retrieve project context.
8. Handle provider failures.
9. Verify its work.
10. Report actual execution results.
11. Control model usage and operational costs.
12. Produce downloadable artifacts.

### FINAL DIRECTIVE

Implement incrementally, starting with Phase 1.

Before writing code, provide:
- Existing architecture assessment.
- Identified reusable modules.
- Proposed file and folder changes.
- Dependencies to install.
- Database migration plan.
- Security considerations.
- Phase 1 implementation plan.

Wait for no additional clarification when the existing code provides sufficient information. Do not invent existing functionality. Test every change and report completed, incomplete, and blocked items separately.

The existing NEXUS AI visual design must remain unchanged throughout development.
12. Keputusan teknis akhir
NEXUS AI Recommended Stack
AI primary

Gemini Flash-Lite / Flash

AI fallback

OpenAI economical model

Specialist

Claude (optional)

Model router

LiteLLM

Orchestration

LangGraph

Backend

Python FastAPI

Database

PostgreSQL + pgvector

Browser

Playwright

Execution
Dokumentasi resmi untuk referensi implementasi:
[Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing?utm_source=chatgpt.com)
[Gemini API Model List](https://ai.google.dev/gemini-api/docs/models?hl=en&utm_source=chatgpt.com)
[OpenAI API Pricing](https://developers.openai.com/api/docs/pricing?utm_source=chatgpt.com)
[LiteLLM Model Router](https://docs.litellm.ai/docs/routing?utm_source=chatgpt.com)
[LangGraph Documentation](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/overview.mdx?utm_source=chatgpt.com)
[Qdrant Hybrid Search](https://qdrant.tech/documentation/hybrid-queries/?utm_source=chatgpt.com)
</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-11-16T13:20:23+07:00.
</ADDITIONAL_METADATA>