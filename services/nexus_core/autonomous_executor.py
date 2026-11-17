"""
NEXUS AI ENTERPRISE — CORE ENGINE 5: AUTONOMOUS EXECUTION ENGINE
Modeled after Google Antigravity Agent Goal Execution and Claude Code Autonomous Loops.
Drives end-to-end task convergence, verifiable deliverables generation, and 3D office synchronization.
"""

import os
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime

from services.nexus_core.ai_brain import cognitive_brain, AgentState
from services.nexus_core.tool_registry import mcp_registry

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_FILE = os.path.join(BASE_DIR, "logs", "activity_log.json")
REPORT_JSON = os.path.join(BASE_DIR, "reports", "laporan.json")


class AutonomousExecutor:
    """
    Executes autonomous multi-step goals from initiation to verified completion.
    """

    def __init__(self, brain=None):
        self.brain = brain or cognitive_brain

    def execute_goal(self, goal_text: str, on_step_callback: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes a user goal through iterative cognitive loops until convergence.
        """
        state = AgentState(goal=goal_text)
        state.phase = "PLANNING"
        state.plan = self.brain.decompose_goal(goal_text)
        state.phase = "EXECUTING"

        print(f"\n[AUTONOMOUS AGENT BRAIN] Memulai eksekusi sasaran: '{goal_text}'")
        print(f"[DAG PLAN] Tersusun {len(state.plan)} fase pekerjaan otonom.")

        while state.phase == "EXECUTING":
            step_result = self.brain.step(state)

            # Sync with 3D Office Bubbles
            if state.history:
                last_step = state.history[-1]
                owner_key = self._find_agent_by_tool(last_step["tool"])
                self._update_office_bubble(owner_key, last_step["thought"], last_step["action"])

            if on_step_callback:
                on_step_callback(state, step_result)

            if step_result.get("status") in ["GOAL_ACHIEVED", "MAX_STEPS_REACHED"]:
                break

            time.sleep(0.1)

        # Finalize and persist executive report
        final_summary = self._finalize_execution(state)
        return final_summary

    def _find_agent_by_tool(self, tool_name: str) -> str:
        for t in mcp_registry.list_tools():
            if t["name"] == tool_name:
                return t["owner_agent"].lower()
        return "arka"

    def _update_office_bubble(self, agent_id: str, text: str, action: str):
        try:
            if os.path.exists(LOGS_FILE):
                with open(LOGS_FILE, "r", encoding="utf-8") as f:
                    log_data = json.load(f)
            else:
                log_data = {"agent_bubbles": {}}

            log_data.setdefault("agent_bubbles", {})
            log_data["agent_bubbles"][agent_id] = {
                "text": text[:120],
                "action": action,
                "updated_at": datetime.now().isoformat(),
                "active": True
            }
            with open(LOGS_FILE, "w", encoding="utf-8") as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _finalize_execution(self, state: AgentState) -> Dict[str, Any]:
        summary = {
            "system": "NEXUS AI ENTERPRISE",
            "version": "4.0.0",
            "engine": "ANTIGRAVITY UNIVERSAL AGENT BRAIN",
            "mandate_id": state.mandate_id,
            "goal": state.goal,
            "phase": state.phase,
            "total_steps": state.current_step,
            "plan_completed": sum(1 for p in state.plan if p.get("completed")),
            "started_at": state.started_at,
            "completed_at": state.completed_at or datetime.now().isoformat(),
            "history": state.history,
            "deliverables": [
                {
                    "title": f"Dokumen Rekapitulasi Eksekusi ({state.mandate_id})",
                    "file": f"DELIVERABLE_{state.mandate_id}.xlsx",
                    "download_url": f"/api/download/DELIVERABLE_{state.mandate_id}.xlsx"
                }
            ]
        }

        try:
            with open(REPORT_JSON, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        return summary


# Global singleton
autonomous_executor = AutonomousExecutor()
