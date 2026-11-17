"""
NEXUS AI ENTERPRISE — CORE ENGINE 3: TOOL REGISTRY & CALLING ENGINE
Modeled after Model Context Protocol (MCP - tools/list & tools/call) and Function Calling.
Enforces strict JSON Schemas, parameter validation, role permissions, and uniform output formatting.
"""

import json
from typing import Dict, List, Any, Callable, Optional
from services.nexus_core.terminal_runner import terminal_runner
from services.nexus_core.filesystem_engine import filesystem_engine


class ToolValidationError(Exception):
    pass


class MCPToolRegistry:
    """
    Standardized MCP-compliant tool registration and invocation engine.
    """

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable[[Dict[str, Any]], Dict[str, Any]],
        owner_agent: str = "ARKA",
        category: str = "General"
    ) -> None:
        """
        Registers a new tool with a formal MCP JSON Schema.
        """
        self._tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "handler": handler,
            "owner_agent": owner_agent,
            "category": category
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Returns all registered tools in MCP standard format (tools/list).
        """
        result = []
        for name, t in self._tools.items():
            result.append({
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["parameters"],
                "owner_agent": t["owner_agent"],
                "category": t["category"]
            })
        return result

    def validate_params(self, schema: Dict[str, Any], params: Dict[str, Any]) -> None:
        """
        Validates parameters against basic JSON Schema rules (required fields and types).
        """
        required = schema.get("required", [])
        for req in required:
            if req not in params:
                raise ToolValidationError(f"Parameter wajib '{req}' tidak ditemukan.")

        properties = schema.get("properties", {})
        for k, v in params.items():
            if k in properties:
                expected_type = properties[k].get("type")
                if expected_type == "string" and not isinstance(v, str):
                    raise ToolValidationError(f"Parameter '{k}' harus bertipe string.")
                elif expected_type == "integer" and not isinstance(v, int):
                    raise ToolValidationError(f"Parameter '{k}' harus bertipe integer.")
                elif expected_type == "boolean" and not isinstance(v, bool):
                    raise ToolValidationError(f"Parameter '{k}' harus bertipe boolean.")
                elif expected_type == "array" and not isinstance(v, list):
                    raise ToolValidationError(f"Parameter '{k}' harus bertipe array/list.")
                elif expected_type == "object" and not isinstance(v, dict):
                    raise ToolValidationError(f"Parameter '{k}' harus bertipe object/dict.")

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a registered tool following MCP standard (tools/call).
        Returns { content: [...], isError: bool, metadata: {...} }.
        """
        if tool_name not in self._tools:
            return {
                "content": [{"type": "text", "text": f"Tool '{tool_name}' tidak terdaftar."}],
                "isError": True,
                "metadata": {"tool": tool_name}
            }

        tool_def = self._tools[tool_name]
        try:
            # 1. Parameter Schema Validation
            self.validate_params(tool_def["parameters"], arguments)

            # 2. Handler Invocation
            result = tool_def["handler"](arguments)

            return {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)}],
                "isError": False if result.get("status") in ["SUCCESS", "PASS", None] else True,
                "raw_result": result,
                "metadata": {
                    "tool": tool_name,
                    "owner_agent": tool_def["owner_agent"],
                    "category": tool_def["category"]
                }
            }
        except ToolValidationError as val_err:
            return {
                "content": [{"type": "text", "text": f"Validation Error: {str(val_err)}"}],
                "isError": True,
                "metadata": {"tool": tool_name}
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Execution Error: {str(e)}"}],
                "isError": True,
                "metadata": {"tool": tool_name}
            }

    def _register_default_tools(self) -> None:
        # 1. Terminal Runner
        self.register_tool(
            name="terminal_execute",
            description="Executes a shell command synchronously and returns stdout, stderr, and exit_code.",
            parameters={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command line to execute in shell."},
                    "cwd": {"type": "string", "description": "Optional working directory."},
                    "timeout": {"type": "integer", "description": "Maximum seconds to wait (default 45)."}
                },
                "required": ["command"]
            },
            handler=lambda p: terminal_runner.run_command(p["command"], p.get("cwd"), p.get("timeout")),
            owner_agent="RAKA",
            category="Terminal & OS"
        )

        # 2. Filesystem: Read
        self.register_tool(
            name="fs_read",
            description="Reads contents of a file within a line range safely.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to file in workspace."},
                    "start_line": {"type": "integer", "description": "First line to read (1-based)."},
                    "end_line": {"type": "integer", "description": "Last line to read (inclusive)."}
                },
                "required": ["path"]
            },
            handler=lambda p: filesystem_engine.read_file(p["path"], p.get("start_line", 1), p.get("end_line")),
            owner_agent="RAKA",
            category="Filesystem"
        )

        # 3. Filesystem: Write
        self.register_tool(
            name="fs_write",
            description="Creates or overwrites a file with content.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to file in workspace."},
                    "content": {"type": "string", "description": "Text content to write."},
                    "overwrite": {"type": "boolean", "description": "Whether to overwrite existing file."}
                },
                "required": ["path", "content"]
            },
            handler=lambda p: filesystem_engine.write_file(p["path"], p["content"], p.get("overwrite", True)),
            owner_agent="RAKA",
            category="Filesystem"
        )

        # 4. Filesystem: Edit
        self.register_tool(
            name="fs_edit",
            description="Surgically replaces a specific string block with new text in a file.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to file in workspace."},
                    "target": {"type": "string", "description": "Exact text substring to replace."},
                    "replacement": {"type": "string", "description": "New replacement content."}
                },
                "required": ["path", "target", "replacement"]
            },
            handler=lambda p: filesystem_engine.edit_file(p["path"], p["target"], p["replacement"]),
            owner_agent="RAKA",
            category="Filesystem"
        )

        # 5. Filesystem: List Directory
        self.register_tool(
            name="fs_list",
            description="Lists entries in a directory.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative directory path."},
                    "recursive": {"type": "boolean", "description": "Whether to traverse subdirectories."}
                },
                "required": []
            },
            handler=lambda p: filesystem_engine.list_directory(p.get("path", ""), p.get("recursive", False)),
            owner_agent="NAYA",
            category="Filesystem"
        )

        # 6. Filesystem: Glob Search
        self.register_tool(
            name="fs_glob",
            description="Finds files matching wildcard pattern across directories.",
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern (e.g. **/*.js, public/*.html)."},
                    "base_path": {"type": "string", "description": "Starting directory."}
                },
                "required": ["pattern"]
            },
            handler=lambda p: filesystem_engine.glob_search(p["pattern"], p.get("base_path", "")),
            owner_agent="NAYA",
            category="Filesystem"
        )

        # 7. Filesystem: Grep Code Search
        self.register_tool(
            name="fs_grep",
            description="Searches code text across workspace files matching regex or literal query.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or regex pattern."},
                    "file_pattern": {"type": "string", "description": "File wildcard filter (e.g. *.py, *.html)."}
                },
                "required": ["query"]
            },
            handler=lambda p: filesystem_engine.grep_search(p["query"], file_pattern=p.get("file_pattern", "*.*")),
            owner_agent="NAYA",
            category="Filesystem"
        )

        # 8. QA Syntax Check
        self.register_tool(
            name="qa_syntax_check",
            description="Validates code syntax for Python or JavaScript files.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to validate."}
                },
                "required": ["path"]
            },
            handler=self._handle_syntax_check,
            owner_agent="FARREL",
            category="Quality Assurance"
        )

        # 9. Security XSS Sanitizer
        self.register_tool(
            name="sec_sanitize_xss",
            description="Sanitizes user input string against HTML/XSS injection.",
            parameters={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Raw input string to sanitize."}
                },
                "required": ["input"]
            },
            handler=lambda p: {
                "status": "SUCCESS",
                "sanitized": p["input"].replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")
            },
            owner_agent="BIMA",
            category="Cybersecurity"
        )

        # 10. Document Generator Excel
        self.register_tool(
            name="doc_generate_xlsx",
            description="Creates a styled Microsoft Excel spreadsheet (.xlsx).",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Document title."},
                    "output_filename": {"type": "string", "description": "File name ending in .xlsx."},
                    "sheets": {"type": "array", "description": "List of sheet specifications."}
                },
                "required": ["title", "output_filename", "sheets"]
            },
            handler=self._handle_excel_gen,
            owner_agent="TARA",
            category="Document Agent"
        )

    def _handle_syntax_check(self, p: Dict[str, Any]) -> Dict[str, Any]:
        from services.tool_execution_service import tool_executor
        return tool_executor.execute_tool("code_syntax_check", {"path": p["path"]})

    def _handle_excel_gen(self, p: Dict[str, Any]) -> Dict[str, Any]:
        from services.file_generation_service import file_generator
        path = file_generator.generate_xlsx(p["title"], p["sheets"], p["output_filename"])
        return {"status": "SUCCESS", "filepath": path, "download_url": f"/api/download/{p['output_filename']}"}


# Global singleton
mcp_registry = MCPToolRegistry()
