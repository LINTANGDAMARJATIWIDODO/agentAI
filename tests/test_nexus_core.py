"""
NEXUS AI ENTERPRISE — AUTOMATED TEST SUITE FOR THE 5 FOUNDATIONAL ENGINES
Verifies Terminal Runner, Filesystem Engine, Tool Calling (MCP), AI Brain, and Autonomous Execution.
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.nexus_core import (
    terminal_runner,
    filesystem_engine,
    mcp_registry,
    cognitive_brain,
    autonomous_executor
)


class TestNexusCoreFoundations(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(BASE_DIR, "tests", "scratch")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file_rel = "tests/scratch/test_probe.txt"

    # ==========================================
    # 1. TERMINAL RUNNER TESTS
    # ==========================================
    def test_01_terminal_execution_success(self):
        res = terminal_runner.run_command("echo 'NEXUS_CORE_ONLINE'")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["exit_code"], 0)
        self.assertIn("NEXUS_CORE_ONLINE", res["stdout"])

    def test_02_terminal_safety_guardrail(self):
        res = terminal_runner.run_command("format c: /q")
        self.assertEqual(res["status"], "BLOCKED")
        self.assertIn("Perintah diblokir", res["stderr"])

    # ==========================================
    # 2. FILESYSTEM ENGINE TESTS
    # ==========================================
    def test_03_filesystem_write_and_read(self):
        content = "Line 1: Nexus AI\nLine 2: Autonomous Agent\nLine 3: Production Ready\n"
        w_res = filesystem_engine.write_file(self.test_file_rel, content)
        self.assertEqual(w_res["status"], "SUCCESS")

        r_res = filesystem_engine.read_file(self.test_file_rel, start_line=2, end_line=3)
        self.assertEqual(r_res["status"], "SUCCESS")
        self.assertIn("Line 2: Autonomous Agent", r_res["content"])
        self.assertNotIn("Line 1", r_res["content"])

    def test_04_filesystem_surgical_edit(self):
        e_res = filesystem_engine.edit_file(
            self.test_file_rel,
            target="Line 2: Autonomous Agent",
            replacement="Line 2: Google Antigravity Level Brain"
        )
        self.assertEqual(e_res["status"], "SUCCESS")
        self.assertEqual(e_res["replacements_made"], 1)

        # Verify replacement persisted
        v_res = filesystem_engine.read_file(self.test_file_rel)
        self.assertIn("Google Antigravity Level Brain", v_res["content"])

    def test_05_filesystem_glob_and_grep(self):
        # Glob
        g_res = filesystem_engine.glob_search("*.txt", base_path="tests/scratch")
        self.assertEqual(g_res["status"], "SUCCESS")
        self.assertTrue(any("test_probe.txt" in m for m in g_res["matches"]))

        # Grep
        grep_res = filesystem_engine.grep_search("Antigravity", base_path="tests/scratch")
        self.assertEqual(grep_res["status"], "SUCCESS")
        self.assertTrue(len(grep_res["matches"]) > 0)

    # ==========================================
    # 3. TOOL CALLING ENGINE (MCP) TESTS
    # ==========================================
    def test_06_tool_registry_mcp_listing(self):
        tools = mcp_registry.list_tools()
        tool_names = [t["name"] for t in tools]
        self.assertIn("terminal_execute", tool_names)
        self.assertIn("fs_read", tool_names)
        self.assertIn("fs_write", tool_names)
        self.assertIn("qa_syntax_check", tool_names)

    def test_07_tool_calling_validation(self):
        # Missing required parameter should fail gracefully with schema error
        res = mcp_registry.call_tool("fs_write", {"path": "test.txt"})  # missing 'content'
        self.assertTrue(res["isError"])
        self.assertIn("Validation Error", res["content"][0]["text"])

    def test_08_tool_calling_execution(self):
        call_res = mcp_registry.call_tool("sec_sanitize_xss", {"input": "<b>Safe</b><script>bad()</script>"})
        self.assertFalse(call_res["isError"])
        self.assertNotIn("<script>", call_res["content"][0]["text"])

    # ==========================================
    # 4. AI BRAIN (COGNITIVE REACT) TESTS
    # ==========================================
    def test_09_cognitive_brain_decomposition(self):
        plan = cognitive_brain.decompose_goal("Buat portal manajemen inventaris terintegrasi")
        self.assertTrue(len(plan) >= 5)
        owners = [p["owner"] for p in plan]
        self.assertIn("RAKA", owners)
        self.assertIn("FARREL", owners)

    # ==========================================
    # 5. AUTONOMOUS EXECUTION TESTS
    # ==========================================
    def test_10_autonomous_goal_execution(self):
        summary = autonomous_executor.execute_goal("Audit kesiapan sistem dan cetak rekapitulasi performa")
        self.assertEqual(summary["engine"], "ANTIGRAVITY UNIVERSAL AGENT BRAIN")
        self.assertEqual(summary["phase"], "COMPLETED")
        self.assertTrue(summary["total_steps"] >= 5)
        self.assertTrue(len(summary["history"]) >= 5)


if __name__ == "__main__":
    unittest.main()
