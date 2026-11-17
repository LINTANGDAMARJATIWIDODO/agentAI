"""
NEXUS AI ENTERPRISE — CORE ENGINES PACKAGE
Implements the 5 Foundational Engines of Autonomous AI Agents:
1. AI Brain (Cognitive ReAct Loop & StateGraph)
2. Tool Calling (MCP-compliant schema & execution engine)
3. Terminal Runner (Safe process executor with timeout & output capture)
4. Filesystem Engine (Surgical edit, windowed read, write, glob, grep)
5. Autonomous Execution (Multi-step goal convergence & 3D office sync)
"""

from services.nexus_core.terminal_runner import terminal_runner, TerminalRunner
from services.nexus_core.filesystem_engine import filesystem_engine, FilesystemEngine
from services.nexus_core.tool_registry import mcp_registry, MCPToolRegistry
from services.nexus_core.ai_brain import cognitive_brain, CognitiveBrain, AgentState
from services.nexus_core.autonomous_executor import autonomous_executor, AutonomousExecutor

__all__ = [
    "terminal_runner",
    "TerminalRunner",
    "filesystem_engine",
    "FilesystemEngine",
    "mcp_registry",
    "MCPToolRegistry",
    "cognitive_brain",
    "CognitiveBrain",
    "AgentState",
    "autonomous_executor",
    "AutonomousExecutor"
]
