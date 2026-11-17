---
name: mcp-builder
description: Design, build, test, and package Model Context Protocol (MCP) servers and tools. Expose enterprise databases, APIs, and CLI tools securely to AI agents. Use when integrating custom tools or MCP services.
---

# SKILL: Model Context Protocol (MCP) Server Engineering

> **Origin Repository:** https://github.com/anthropics/skills  
> **Source License:** Apache License 2.0  
> **Attribution:** Adapted from Anthropic's official `skills/mcp-builder` for Antigravity MCP Integration.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To author modular, secure, and production-ready Model Context Protocol (MCP) servers and tools that safely expose enterprise internal data stores, command-line utilities, and business APIs to autonomous agents using stdio and SSE/HTTP transports.

## 2. SCOPE
- MCP server architecture (TypeScript / Python FastMCP), JSON-RPC 2.0 protocol handling, tool definition schemas (JSON Schema), resource endpoints, prompt templates, and security sandboxing.

## 3. CORE ARCHITECTURAL PRINCIPLES
1. **Schema Explicitness:** Tool parameters must feature detailed descriptions, strict types, and required field lists so the LLM invokes them accurately.
2. **Graceful Error Encapsulation:** MCP tools must catch execution exceptions and return informative JSON error objects rather than crashing the protocol server.
3. **Least Privilege Tool Boundaries:** Expose only the specific functions required; do not expose arbitrary shell execution or raw database query tools without strict guardrails.

## 4. STEP-BY-STEP PROCEDURE
1. **Define Tool Manifest:** List tool names, descriptions, input schemas, and expected return types.
2. **Implement Protocol Server:** Use `@modelcontextprotocol/sdk` (TypeScript) or `fastmcp` (Python).
3. **Add Input Validation:** Validate all input parameters with Zod or Pydantic before executing business logic.
4. **Implement Handlers:** Connect tool handlers to backend data services with connection pooling and timeouts.
5. **Configure Client Integration:** Add server configuration block to `.gemini/antigravity/mcp_config.json` with absolute `cwd` and environment variables.
6. **Integration Testing:** Run automated MCP client simulation tests to verify tool invocation and output formatting.

## 5. STANDARD TOOL DEFINITION EXAMPLE (FASTMCP)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nexus-enterprise-tools")

@mcp.tool()
def get_task_audit_log(task_id: str) -> dict:
    """Retrieve verified activity log for a specific enterprise task."""
    # Validation and secure fetch logic here
    return {"task_id": task_id, "status": "COMPLETED"}
```

## 6. CONSTRAINTS & SECURITY RULES
- Never expose environment variables containing API keys or database passwords through MCP resources or tool outputs.
- Enforce strict parameter type checking to prevent command injection.
