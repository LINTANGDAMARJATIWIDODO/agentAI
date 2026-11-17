# NEXUS AI ENTERPRISE — SKILL SOURCE & LICENSE REGISTRY

> **Document Classification:** Enterprise Open-Source Compliance & Governance  
> **System Architecture:** NEXUS Multi-Agent Workforce  
> **Compliance Officer:** SEKAR (Director of Finance, Risk & Compliance)  
> **Approved By:** ARKA (Chief Executive & Strategy Officer)  
> **Date of Audit:** 2026-11-15  
> **Audit Version:** 2.0.0-PROD

---

## 1. REPOSITORY AUDIT & ATTRIBUTION MATRIX

| Repository Identifier | Author / Custodian | Upstream Repository URL | License Type | Pinned Version / Commit Ref | Skills Acquired | Security & Safety Clearance |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **`obra/superpowers`** | Jesse Vincent (`obra`) | `https://github.com/obra/superpowers` | **MIT License** | `main` (`commit-pinned-2026.11`) | 5 Skills: `subagent-driven-development`, `test-driven-development`, `systematic-debugging`, `requesting-code-review`, `writing-plans` | **APPROVED** (Zero malicious code, zero arbitrary shell injection) |
| **`j4flmao/agent-skills`** | `j4flmao` | `https://github.com/j4flmao/agent-skills` | **MIT License** | `main` (`release-v1.4.2`) | 9 Skills: `backend-api-design`, `cloud-architecture-well-architected`, `devops-ci-cd`, `cybersecurity-hardening`, `data-engineering-pipelines`, `performance-engineering`, `mlops-pipeline`, `frontend-engineering-patterns`, `database-engineering` | **APPROVED** (Clean schemas, fully typed, isolated references) |
| **`anthropics/skills`** | Anthropic (`anthropics`) | `https://github.com/anthropics/skills` | **Apache-2.0 License** | `main` (`commit-pinned-2026.11`) | 2 Skills: `brand-guidelines`, `mcp-builder` | **APPROVED** (Official enterprise AI standard templates) |
| **`bughunt8/skills`** | `bughunt8` | `https://github.com/bughunt8/skills` | **MIT License** | `main` (`commit-pinned-2026.11`) | 2 Skills: `deep-research`, `agile-scrum-operations` | **APPROVED** (Verified multi-hop research & agile frameworks) |
| **`awesome-antigravity`** | `LichAmnesia` | `https://github.com/LichAmnesia/awesome-antigravity-skills` | **CC0 1.0 Universal** | `main` (`v2026.11`) | 1 Skill: `antigravity-git-workflow` | **APPROVED** (Public Domain standard git templates) |
| **`ind4x/ai-agent-skills`** | `ind4x` | `https://github.com/ind4x/ai-agent-skills` | **MIT License** | `main` (`v2026.11`) | 106 Curated Skills: Testing & QA (`automated-qa-testing`), UI/UX, Multi-Agent Coordination, Integration | **APPROVED** (Curated high-assurance primitives) |
| **`nextlevelbuilder/ui-ux-pro-max-skill`** | `nextlevelbuilder` | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` | **MIT License** | `main` (`v2026.11`) | Dedicated UI/UX Pro Max: Design Systems (`product-design-system`), Typography, Layout, Component Contracts | **APPROVED** (WCAG 2.1 AA compliant design tokens) |
| **`vercel-labs/agent-skills`** | Vercel Labs | `https://github.com/vercel-labs/agent-skills` | **Apache-2.0 License** | `main` (`v2026.11`) | Frontend Engineering, Web Design Guidelines, Component Composition, App Performance | **APPROVED** (Industry standard enterprise web patterns) |
| **`SeaXen/agentskills`** | `SeaXen` | `https://github.com/SeaXen/agentskills` | **MIT License** | `main` (`v2026.11`) | 594 Skills & 20 Multi-Agent Specialists: Data Architecture (`data-engineering-etl`), Growth Marketing (`growth-marketing-seo`) | **APPROVED** (Specialized autonomous agent playbooks) |
| **`nexus-internal-core`** | NEXUS AI Enterprise Corp. | *Internal Proprietary Development* | **NEXUS Enterprise Commercial License** | `v2.0.0` | 20 Skills: 12 Foundational + 8 Specialized Original (`decision-intelligence`, `competitive-intelligence`, `source-verification`, `financial-forecasting`, `procurement-analysis`, `fraud-risk-assessment`, `strategic-marketing-seo`, `corporate-communication`) | **APPROVED** (Authored to strict enterprise governance) |

---

## 2. LEGAL & LICENSE COMPLIANCE STATEMENT
1. **Permissive Open-Source Compatibility:** All external repositories utilized (`obra/superpowers`, `j4flmao/agent-skills`, `anthropics/skills`, `bughunt8/skills`, `LichAmnesia/awesome-antigravity-skills`) are governed by OSI-approved permissive open-source licenses (MIT, Apache 2.0) or public domain dedication (CC0-1.0).
2. **Attribution & Notice Preservation:** In accordance with Section 4(a) of the Apache 2.0 License and the MIT License conditions, all imported skills preserve original author attributions, source URLs, and copyright notices in their respective `SKILL.md` header comments.
3. **Patent & Indemnity Protection:** Neither the MIT nor Apache 2.0 components introduce restrictive copyleft provisions (such as GPL/AGPL). The integrated codebase remains unencumbered for proprietary enterprise deployment.

---

## 3. SECURITY & UNTRUSTED CODE SCREENING PROTOCOL
All external skills imported into `.agents/skills/` underwent strict pre-integration screening:
- **No Remote Code Execution (RCE):** No scripts containing `curl | bash`, unquoted `eval`, or unsanitized subprocess executions were imported.
- **No Credential Exfiltration:** No hardcoded tokens, telemetry endpoints, or external network webhooks exist in any skill instructions.
- **Progressive Disclosure Adherence:** Skills conform strictly to Antigravity's progressive disclosure standard, saving model context while maintaining deep procedural guidance.
