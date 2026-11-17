---
name: source-verification
description: Audit facts, statistical claims, and data provenance. Verify data credibility, detect corporate bias, detect hallucinated statistics, and maintain verifiable bibliographies. Use when validating claims or auditing research integrity.
---

# SKILL: Enterprise Source Verification & Data Provenance Audit

> **Origin:** Original NEXUS Enterprise Skill (Proprietary Workforce Asset)  
> **Classification:** Research Integrity & Anti-Hallucination Standard  
> **Author:** NEXUS Research & Intelligence Board  
> **Target Owner:** NAYA (Director of Research) | Shared: ARKA (CEO / Quality Assurance)

---

## 1. OBJECTIVE
To eradicate artificial intelligence hallucination, misattribution, and biased statistics from enterprise deliverables by enforcing a cryptographic-grade standard of verification, provenance tracking, and credibility grading.

## 2. SCOPE
- Fact-checking numerical assertions, verifying regulatory citations, testing survey methodology robustness, detecting commercial bias, and compiling audit trails.

## 3. EXECUTION METHODOLOGY
- **The CRAAP Test for Enterprise:** Currency, Relevance, Authority, Accuracy, and Purpose.
- **Source Credibility Hierarchy (Tiers 1 to 4):**
  - *Tier 1 (Authoritative):* Government statistics bureaus (BPS, US Census), audited regulatory filings (SEC, OJK), peer-reviewed academic journals, formal technical standards (ISO, IEEE, W3C).
  - *Tier 2 (Reputable Industry Intelligence):* Established global research institutes (Gartner, IDC, McKinsey, Statista, World Bank).
  - *Tier 3 (Commercial / Vendor Whitepapers):* Tech company publications (requires cross-checking for commercial self-interest).
  - *Tier 4 (Unverified / Disqualified):* Anonymous blog posts, unmoderated forums, promotional press releases without raw data.

## 4. DECISION RULES & AUDIT CRITERIA
1. Any data point classified under Tier 3 or 4 cannot be tagged as `[VERIFIED FACT]`; it must be labeled `[ESTIMATION / UNVERIFIED VENDOR CLAIM]`.
2. Every numerical statement must include: the exact sample size (N), geographic boundary, and publication year.
3. If two Tier-1/Tier-2 sources conflict, present both figures with an explanatory note regarding methodological variance.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- 100% of statistical figures in final reports must map to an indexed bibliographic citation.
- No dead or unverifiable links allowed in reference appendices.
- All regulatory citations must specify exact law number, year, and article.

## 6. CONSTRAINTS
- Zero tolerance for AI-generated hypothetical numbers presented as historical data.
- Never use a secondary quote when the original primary research paper is retrievable.

## 7. EXPECTED OUTPUT FORMAT
- **Fact-Verification Ledger:** Claim, Source, Source Tier, Sample Size, Status (Verified/Flagged).
- **Disputed Claims Analysis:** Explanation of conflicting numbers and reconciliation.
- **Audited Bibliography Index:** Formal citations sorted alphabetically.

## 8. EXAMPLE USAGE
NAYA audits an industry report claiming "85% of banks have adopted generative AI," reveals that the sample size was only 20 vendor clients, and downgrades the claim to a qualified vendor survey.
