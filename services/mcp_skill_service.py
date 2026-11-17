"""
NEXUS AI ENTERPRISE — Skills and Model Context Protocol (MCP) Service
Engineered by RAKA (CTO), BIMA (CISO), and TARA (CDO)
Manages MCP servers, custom agent skills, GitHub skills, and security clearance.
"""

import os
import json
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SKILLS_REGISTRY_FILE = os.path.join(CONFIG_DIR, "skills_registry.json")


def load_json(filepath: str, default_val: Any = None) -> Any:
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_val
    return default_val


class MCPSkillService:
    def __init__(self):
        self.skills_data = load_json(SKILLS_REGISTRY_FILE, None)
        if not self.skills_data:
            self.skills_data = self._init_default_registry()
            self._save()

    def _init_default_registry(self) -> Dict[str, Any]:
        return {
            "mcp_version": "1.0.0",
            "protocol": "Model Context Protocol (MCP)",
            "servers": [
                {
                    "name": "nexus-filesystem-mcp",
                    "status": "CONNECTED",
                    "transport": "stdio",
                    "capabilities": ["resources", "tools", "prompts"],
                    "tools": ["read_file", "write_file", "list_directory", "get_file_info"],
                    "security_policy": "SANDBOX_RESTRICTED"
                },
                {
                    "name": "nexus-gdrive-mcp",
                    "status": "CONNECTED",
                    "transport": "stdio",
                    "capabilities": ["resources", "tools"],
                    "tools": ["gdrive_search", "gdrive_read_doc", "gdrive_read_sheet", "gdrive_audit"],
                    "security_policy": "STRICT_READ_ONLY_AUDIT"
                },
                {
                    "name": "nexus-document-mcp",
                    "status": "CONNECTED",
                    "transport": "stdio",
                    "capabilities": ["tools"],
                    "tools": ["generate_docx", "generate_xlsx", "generate_zip", "generate_pdf"],
                    "security_policy": "OUTPUT_RESTRICTED"
                },
                {
                    "name": "nexus-playwright-mcp",
                    "status": "CONNECTED",
                    "transport": "stdio",
                    "capabilities": ["tools"],
                    "tools": ["browser_navigate", "browser_screenshot", "browser_evaluate", "browser_assert"],
                    "security_policy": "HEADLESS_RESTRICTED"
                },
                {
                    "name": "nexus-postgres-mcp",
                    "status": "STANDBY",
                    "transport": "stdio",
                    "capabilities": ["resources", "tools"],
                    "tools": ["query_readonly", "get_schema", "explain_plan"],
                    "security_policy": "READ_ONLY_QUERY"
                }
            ],
            "skills": [
                {
                    "id": "skill-fullstack-dev",
                    "name": "Fullstack Application Synthesizer",
                    "owner": "RAKA",
                    "version": "2.4.0",
                    "description": "Synthesizes responsive single page web applications with Tailwind, modern typography, reactive cart, and sound.",
                    "security_clearance": "APPROVED_BY_BIMA"
                },
                {
                    "id": "skill-document-generator",
                    "name": "Enterprise Document & Spreadsheet Publisher",
                    "owner": "SEKAR & TARA",
                    "version": "2.1.0",
                    "description": "Builds multi-sheet styled Excel workbooks, Word docs, and project ZIP bundles.",
                    "security_clearance": "APPROVED_BY_BIMA"
                },
                {
                    "id": "skill-security-sast",
                    "name": "OWASP SAST & Input Sanitization Shield",
                    "owner": "BIMA",
                    "version": "3.0.0",
                    "description": "Scans forms for XSS vulnerabilities and neutralizes malicious script payloads.",
                    "security_clearance": "APPROVED_BY_BIMA"
                },
                {
                    "id": "skill-automated-testing",
                    "name": "End-to-End Regression & Assertion Suite",
                    "owner": "FARREL",
                    "version": "2.0.0",
                    "description": "Executes 8 automated test cases on UI, DOM, mathematics, and viewport stability.",
                    "security_clearance": "APPROVED_BY_BIMA"
                },
                {
                    "id": "skill-spbe-audit",
                    "name": "SPBE DKI Jakarta 3C Forensic Auditor",
                    "owner": "ARKA & NAYA",
                    "version": "3.2.0",
                    "description": "Audits 22 Perangkat Daerah, 42 columns, RAB L1-L7, Sasaran RPJMD, and Gap Analysis.",
                    "security_clearance": "APPROVED_BY_BIMA"
                }
            ]
        }

    def _save(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(SKILLS_REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.skills_data, f, indent=2, ensure_ascii=False)

    def get_all(self) -> Dict[str, Any]:
        return self.skills_data

    def get_servers(self) -> List[Dict[str, Any]]:
        return self.skills_data.get("servers", [])

    def get_skills(self) -> List[Dict[str, Any]]:
        return self.skills_data.get("skills", [])


mcp_skill_service = MCPSkillService()
