"""
NEXUS AI ENTERPRISE — Automated Skill Discovery & Integrity Test Suite
Verifies all 39 enterprise skills, frontmatter schemas, directory matches,
manifest references, and security guidelines.
"""

import os
import re
import unittest
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE_DIR, ".agents", "skills")
AGENTS_CONFIG = os.path.join(BASE_DIR, "config", "agents_config.json")


class TestNexusSkills(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(SKILLS_DIR), f"Skills directory not found at: {SKILLS_DIR}")
        self.skill_folders = [f for f in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, f))]

    def test_total_skills_count(self):
        """Verify that at least 41 skills are installed and organized."""
        self.assertGreaterEqual(len(self.skill_folders), 41, f"Expected at least 41 skills, found {len(self.skill_folders)}")

    def test_skill_structure_and_frontmatter(self):
        """Verify each skill has SKILL.md with valid YAML frontmatter matching directory name."""
        frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

        for skill_name in self.skill_folders:
            skill_path = os.path.join(SKILLS_DIR, skill_name)
            skill_md = os.path.join(skill_path, "SKILL.md")

            self.assertTrue(os.path.exists(skill_md), f"SKILL.md missing in {skill_name}")

            # Check file size < 24 KB
            size_bytes = os.path.getsize(skill_md)
            self.assertLess(size_bytes, 24000, f"{skill_name}/SKILL.md exceeds 24KB limit ({size_bytes} bytes)")

            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()

            match = frontmatter_pattern.match(content)
            self.assertIsNotNone(match, f"Invalid or missing YAML frontmatter in {skill_name}/SKILL.md")

            yaml_block = match.group(1)
            name_match = re.search(r"^name:\s*([\w\-]+)", yaml_block, re.MULTILINE)
            self.assertIsNotNone(name_match, f"Missing 'name' field in {skill_name}/SKILL.md frontmatter")
            declared_name = name_match.group(1).strip()

            self.assertEqual(
                declared_name, skill_name,
                f"Frontmatter name '{declared_name}' does not match directory '{skill_name}'"
            )

            desc_match = re.search(r"^description:\s*(.+)", yaml_block, re.MULTILINE)
            self.assertIsNotNone(desc_match, f"Missing 'description' field in {skill_name}/SKILL.md frontmatter")
            desc_text = desc_match.group(1).strip()
            self.assertGreater(len(desc_text), 15, f"Description too short in {skill_name}/SKILL.md")

    def test_security_screening(self):
        """Verify no dangerous shell scripts or plaintext secret keys in skill files."""
        forbidden_patterns = [
            r"rm\s+-rf\s+/",
            r"curl\s+.*?\|\s*bash",
            r"(api[_-]?key|secret[_-]?key|token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]"
        ]

        for skill_name in self.skill_folders:
            skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()

            for pattern in forbidden_patterns:
                self.assertIsNone(
                    re.search(pattern, content, re.IGNORECASE),
                    f"Security violation: matched forbidden pattern in {skill_name}/SKILL.md"
                )

    def test_agent_manifests_integrity(self):
        """Verify each of the 5 manifests references valid installed skills."""
        manifests = [
            "ARKA_SKILL_MANIFEST.md",
            "NAYA_SKILL_MANIFEST.md",
            "RAKA_SKILL_MANIFEST.md",
            "SEKAR_SKILL_MANIFEST.md",
            "DIMAS_SKILL_MANIFEST.md"
        ]

        for m in manifests:
            manifest_path = os.path.join(BASE_DIR, m)
            self.assertTrue(os.path.exists(manifest_path), f"Manifest missing: {m}")
            with open(manifest_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Find all `skill-name` references
            skill_refs = re.findall(r"\.agents/skills/([\w\-]+)", text)
            self.assertGreater(len(skill_refs), 0, f"No skill paths found in {m}")
            for ref in skill_refs:
                self.assertIn(
                    ref, self.skill_folders,
                    f"Manifest {m} references nonexistent skill: {ref}"
                )

    def test_agents_config_skills_alignment(self):
        """Verify that skills listed in config/agents_config.json exist in .agents/skills/."""
        with open(AGENTS_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)

        roster = data.get("enterprise_roster", [])
        self.assertGreaterEqual(len(roster), 5, "Expected at least 5 agents in enterprise_roster")

        for agent in roster:
            agent_skills = agent.get("skills", [])
            self.assertGreater(len(agent_skills), 0, f"Agent {agent['name']} has no assigned skills")
            for skill in agent_skills:
                self.assertIn(
                    skill, self.skill_folders,
                    f"Agent {agent['name']} assigned unknown skill: {skill}"
                )


if __name__ == "__main__":
    unittest.main()
