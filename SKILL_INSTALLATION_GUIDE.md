# NEXUS AI ENTERPRISE — SKILL INSTALLATION & DEPLOYMENT GUIDE

> **System Standard:** Antigravity AI Customization Engine  
> **Target Audience:** Systems Architects, DevOps Engineers, and AI Agents  
> **Document Version:** 2.0.0

---

## 1. ARCHITECTURE & DISCOVERY HIERARCHY

In Google Antigravity, agent skills extend autonomous capabilities using progressive disclosure. Skills are placed in the project root directory under `.agents/skills/`:

```text
NEXUS-AI-ENTERPRISE/
├── .agents/
│   ├── agents/
│   │   ├── arka.md
│   │   ├── naya.md
│   │   ├── raka.md
│   │   ├── sekar.md
│   │   └── dimas.md
│   └── skills/
│       ├── <skill-name>/
│       │   ├── SKILL.md            # Required: Instruction file with YAML frontmatter
│       │   ├── scripts/            # Optional: Validated executable helper scripts
│       │   ├── templates/          # Optional: Reusable artifacts and markdown templates
│       │   └── references/         # Optional: Deep reference materials
```

### How Antigravity Discovers Skills
1. **Discovery Root:** When an agent starts, Antigravity scans `.agents/skills/` (and parent folders up to repository root).
2. **Progressive Disclosure:** Only the `name` and `description` from the YAML frontmatter are initially injected into the agent's prompt budget.
3. **On-Demand Activation:** When an agent encounters a task matching the description, it dynamically reads the full `SKILL.md` content, minimizing context window overhead.

---

## 2. INSTALLATION PROCEDURES

### Method A: Automated Enterprise Repository Setup (Recommended)
All 39 approved skills are pre-installed and verified inside `.agents/skills/`. To deploy in a new workspace:

```bash
# 1. Clone or copy the NEXUS repository
git clone <nexus-enterprise-repo-url> NEXUS-AI-ENTERPRISE
cd NEXUS-AI-ENTERPRISE

# 2. Verify all 39 skills are discovered
python tests/test_skills.py

# 3. Launch the Virtual AI Office
npm install
npm run dev
```

### Method B: Adding an Individual Skill
To install an additional external skill:

1. Create a dedicated directory:
   ```bash
   mkdir -p .agents/skills/<new-skill-name>
   ```
2. Create `SKILL.md` with required frontmatter:
   ```markdown
   ---
   name: <new-skill-name>
   description: >-
     A concise third-person description stating WHAT the skill does and
     WHEN the agent should activate it.
   ---
   # SKILL: <Title>
   ...
   ```
3. Ensure directory name matches `name` in frontmatter exactly.
4. Add the skill identifier to the relevant agent's manifest (`ARKA_SKILL_MANIFEST.md`, etc.) and `config/agents_config.json`.
5. Run the validation test suite to confirm discovery.

---

## 3. QUALITY & FORMATTING RULES
- **No Monolithic Skills:** Keep each skill focused on a single professional domain.
- **Strict Frontmatter:** Must contain `name` (lowercase, hyphenated) and `description` (actionable trigger criteria).
- **Security Vetting:** Never execute scripts from untrusted skills without inspecting source code.
- **Budget Compliance:** Keep `SKILL.md` files under 24 KB. Place bulky references in a `references/` subfolder.

---

## 4. TROUBLESHOOTING

| Symptom | Probable Cause | Remediation |
| :--- | :--- | :--- |
| **Agent does not activate skill** | Vague frontmatter `description` | Rewrite description with explicit triggers e.g., "Use when designing RESTful APIs..." |
| **Discovery Failure** | Directory name does not match `name` | Ensure `.agents/skills/xyz/` contains `name: xyz` in `SKILL.md` |
| **Context Window Overflow** | `SKILL.md` exceeds 24 KB | Move lengthy tables to `references/` subfolder and link relatively |
| **Permission Denied** | Script lacking executable flags | Run `chmod +x .agents/skills/<skill>/scripts/*` |
