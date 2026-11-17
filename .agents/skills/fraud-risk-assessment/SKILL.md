---
name: fraud-risk-assessment
description: Detect internal control gaps, conduct Fraud Triangle evaluations, detect anomalous financial transactions, and design anti-fraud controls. Use when auditing internal controls or evaluating fraud vulnerabilities.
---

# SKILL: Enterprise Fraud Risk Assessment & Internal Control Audit

> **Origin:** Original NEXUS Enterprise Skill (Proprietary Workforce Asset)  
> **Classification:** Internal Audit & Risk Governance Standard  
> **Author:** NEXUS Finance & Compliance Board  
> **Target Owner:** SEKAR (Director of Finance, Risk & Compliance)

---

## 1. OBJECTIVE
To identify systemic vulnerabilities in operational and financial processes, evaluate exposure to occupational fraud, misappropriation of assets, and reporting corruption, and design preventative and detective internal controls (COSO framework).

## 2. SCOPE
- The Fraud Triangle analysis (Incentive/Pressure, Opportunity, Rationalization), segregation of duties (SoD) audits, expense reimbursement fraud, automated disbursement tampering, and AI agent execution anomalies.

## 3. EXECUTION METHODOLOGY
- **The Fraud Triangle Forensic Lens:**
  - *Pressure:* Aggressive financial targets, liquidity crunches, or unachievable KPIs.
  - *Opportunity:* Weak access controls, unreviewed managerial overrides, single-signature approvals.
  - *Rationalization:* Cultural tolerance for policy bending, perceived undercompensation.
- **Segregation of Duties (SoD) Matrix:** Ensuring that the agent/person who initiates a transaction cannot approve, execute, and reconcile the same transaction.
- **Benford's Law & Anomaly Screening:** Statistical analysis of transaction digit distributions to detect fabricated invoices or rounded disbursement amounts.

## 4. DECISION RULES & CONTROL CRITERIA
1. Dual-Authorization Mandate: No financial disbursement or contract execution may be approved by a single entity; it requires two distinct authorization signatures (e.g., SEKAR verification + ARKA executive sign-off).
2. Any transaction exceeding the median department spend by > 3 standard deviations must be flagged for manual human inspection.
3. Automated processes must maintain immutable, append-only cryptographic transaction logs.

## 5. QUALITY STANDARDS & REPORTING PROTOCOL
- All identified control deficiencies must be categorized: Material Weakness, Significant Deficiency, or Operational Control Deficiency.
- Remediation plans must assign explicit owners and remediation deadlines (<= 30 days for Material Weaknesses).

## 6. CONSTRAINTS
- Strict confidentiality: Fraud investigations must be handled with appropriate legal discretion.
- Anti-retaliation: Whistleblower protection mechanisms must be verified in corporate SOPs.

## 7. EXPECTED OUTPUT FORMAT
- **Fraud Risk Exposure Register (Process, Threat, Opportunity Rating, Inherent Risk)**
- **Segregation of Duties (SoD) Conflict Matrix**
- **Forensic Anomaly Audit Summary**
- **Corrective Action & Preventive Control Recommendations**

## 8. EXAMPLE USAGE
SEKAR audits the vendor payment pipeline, discovers that a developer could alter recipient bank details in the database without an audit trigger, and mandates dual-key approval and database trigger logging.
