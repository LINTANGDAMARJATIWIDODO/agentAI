"""
NEXUS AI ENTERPRISE — MCP Safe CLI Tool Dispatcher
Reads JSON payload from stdin to avoid shell escaping issues on Windows/Linux.
"""

import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.nexus_core.tool_registry import mcp_registry


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"isError": True, "error": "No input provided"}))
            return

        payload = json.loads(raw_input)
        tool_name = payload.get("tool", "")
        params = payload.get("params", {})

        result = mcp_registry.call_tool(tool_name, params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"isError": True, "error": str(e)}))


if __name__ == "__main__":
    main()
