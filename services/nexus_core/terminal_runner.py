"""
NEXUS AI ENTERPRISE — CORE ENGINE 1: TERMINAL RUNNER
Modeled after Claude Code (Bash tool) and Google Antigravity (run_command).
Provides robust subprocess execution with timeout, output capture, exit code inspection,
and Zero-Trust security guardrails.
"""

import os
import sys
import time
import subprocess
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SecurityPolicyViolation(Exception):
    """Raised when a command violates enterprise zero-trust DLP or safety guardrails."""
    pass


class TerminalRunner:
    """
    Production-grade Terminal execution engine for autonomous agents.
    Executes shell commands with strict timeout bounds, stream capture, and safety checks.
    """

    def __init__(self, workspace_dir: Optional[str] = None, default_timeout: int = 45):
        self.workspace_dir = os.path.abspath(workspace_dir or BASE_DIR)
        self.default_timeout = default_timeout
        self.history: list = []

    def _validate_safety(self, command: str) -> None:
        """
        Guards against accidental catastrophic filesystem mutations and unauthorized destructive actions.
        """
        cmd_lower = command.lower().strip()
        destructive_patterns = [
            "format c:", "rmdir /s /q c:\\windows", "del /f /s /q c:\\windows",
            ":(){ :|:& };:", "drop database", "sudo rm -rf /"
        ]
        for pattern in destructive_patterns:
            if pattern in cmd_lower:
                raise SecurityPolicyViolation(f"Perintah diblokir oleh Enterprise Security Guardrail: '{pattern}'")

    def run_command(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: Optional[int] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executes a shell command synchronously within the specified working directory.
        Captures stdout, stderr, exit code, and execution time.
        """
        target_cwd = os.path.abspath(cwd or self.workspace_dir)
        exec_timeout = timeout or self.default_timeout
        start_time = time.time()

        try:
            self._validate_safety(command)
        except SecurityPolicyViolation as sec_err:
            return {
                "status": "BLOCKED",
                "exit_code": -1,
                "stdout": "",
                "stderr": str(sec_err),
                "execution_time_ms": 0.0,
                "command": command,
                "cwd": target_cwd
            }

        shell_env = os.environ.copy()
        if env:
            shell_env.update(env)

        # Determine appropriate shell for Windows vs Unix
        if sys.platform == "win32":
            shell_cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", command]
        else:
            shell_cmd = ["/bin/bash", "-c", command]

        try:
            proc = subprocess.run(
                shell_cmd,
                cwd=target_cwd,
                capture_output=True,
                text=True,
                timeout=exec_timeout,
                env=shell_env,
                encoding="utf-8",
                errors="replace"
            )
            duration_ms = round((time.time() - start_time) * 1000, 2)
            exit_code = proc.returncode

            result = {
                "status": "SUCCESS" if exit_code == 0 else "FAILED",
                "exit_code": exit_code,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "execution_time_ms": duration_ms,
                "command": command,
                "cwd": target_cwd
            }
        except subprocess.TimeoutExpired as timeout_err:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            result = {
                "status": "TIMEOUT",
                "exit_code": 124,
                "stdout": (timeout_err.stdout or "").strip() if hasattr(timeout_err, "stdout") else "",
                "stderr": f"Command timed out after {exec_timeout} seconds.",
                "execution_time_ms": duration_ms,
                "command": command,
                "cwd": target_cwd
            }
        except Exception as ex:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            result = {
                "status": "ERROR",
                "exit_code": -1,
                "stdout": "",
                "stderr": str(ex),
                "execution_time_ms": duration_ms,
                "command": command,
                "cwd": target_cwd
            }

        self.history.append({
            "command": command,
            "status": result["status"],
            "exit_code": result["exit_code"],
            "timestamp": time.time()
        })
        return result


# Global singleton
terminal_runner = TerminalRunner()
