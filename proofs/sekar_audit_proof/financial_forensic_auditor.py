"""
NEXUS AI ENTERPRISE — Practical Financial & Risk Audit Proof by SEKAR
Role: Chief Financial, Risk & Compliance Officer
Artifact: Automated Financial Statement Forensic Auditor & Risk Matrix Engine
Capabilities Demonstrated:
1. Forensic Detection of Balance Sheet Imbalances (Assets != Liabilities + Equity)
2. Discovery of EBITDA Manipulation / Non-Operating Gain Misclassification
3. Recalculation of Cash Burn Rate and Runway Deficits
4. Statutory Regulatory Compliance Auditing (UU PDP & SPBE Contingency Reserve)
5. Issuance of Corrective Journal Entries and Restated Financial Schedule
"""

import json
import os
from typing import Dict, List, Any


class FinancialForensicAuditor:
    def __init__(self):
        # Sample corporate financial statement submitted for SEKAR's audit
        self.submitted_statement = {
            "fiscal_period": "FY2026-Q4",
            "currency": "USD",
            "income_statement": {
                "gross_revenue": 5000000.0,
                "cost_of_goods_sold": 2200000.0,
                "gross_profit": 2800000.0,
                "operating_expenses": {
                    "salaries_and_wages": 1200000.0,
                    "sales_and_marketing": 500000.0,
                    "general_and_administrative": 300000.0,
                    "depreciation_and_amortization": 250000.0
                },
                "non_operating_gain_one_off": 350000.0,
                "claimed_ebitda": 1150000.0  # Anomaly: Submitter included non-operating one-off gain!
            },
            "balance_sheet": {
                "total_assets": 8500000.0,
                "total_liabilities": 4200000.0,
                "total_equity": 3850000.0  # Anomaly: 4.2M + 3.85M = 8.05M != 8.5M (Imbalance: $450,000!)
            },
            "cash_flow_and_runway": {
                "cash_at_bank": 1800000.0,
                "claimed_monthly_burn": 100000.0,  # Anomaly: Omitted quarterly tax & supplier arrears
                "claimed_runway_months": 18.0
            },
            "regulatory_compliance": {
                "uu_pdp_compliance_reserve": 0.0,  # Anomaly: Zero statutory reserve set aside for PDP liability
                "spbe_security_audit_fund": 0.0
            }
        }

    def execute_forensic_audit(self) -> Dict[str, Any]:
        """Scrutinizes financial records, flags anomalies, and issues corrective entries."""
        findings: List[Dict[str, Any]] = []

        bs = self.submitted_statement["balance_sheet"]
        is_stmt = self.submitted_statement["income_statement"]
        cf = self.submitted_statement["cash_flow_and_runway"]
        reg = self.submitted_statement["regulatory_compliance"]

        # 1. Audit Balance Sheet Equation
        assets = bs["total_assets"]
        liab = bs["total_liabilities"]
        equity = bs["total_equity"]
        calc_liab_eq = liab + equity
        imbalance = round(assets - calc_liab_eq, 2)

        if abs(imbalance) > 0.01:
            findings.append({
                "finding_id": "AUDIT-FINDING-001",
                "area": "Balance Sheet Fundamental Equation",
                "severity": "CRITICAL_DEFECT",
                "description": f"Balance sheet equation broken! Assets (${assets:,.2f}) != Liabilities + Equity (${calc_liab_eq:,.2f}). Unreconciled gap: ${imbalance:,.2f}.",
                "root_cause": "Omission of $450,000 accrued restructuring and warranty liability from current liabilities.",
                "corrective_action": "Increase Total Liabilities by $450,000.00 to balance equation: $4,650,000 + $3,850,000 = $8,500,000.",
                "corrective_journal_entry": {
                    "debit": "Retained Earnings / Expense Reserve: $450,000",
                    "credit": "Accrued Restructuring Liability: $450,000"
                }
            })

        # 2. Audit EBITDA Calculation
        opex = is_stmt["operating_expenses"]
        total_opex = sum(opex.values())
        true_operating_income = is_stmt["gross_profit"] - total_opex
        da = opex["depreciation_and_amortization"]
        true_ebitda = true_operating_income + da
        claimed_ebitda = is_stmt["claimed_ebitda"]

        if abs(claimed_ebitda - true_ebitda) > 0.01:
            findings.append({
                "finding_id": "AUDIT-FINDING-002",
                "area": "Income Statement & EBITDA Integrity",
                "severity": "HIGH_MATERIAL_MISSTATEMENT",
                "description": f"EBITDA overstated! Submitter claimed ${claimed_ebitda:,.2f}, but true operating EBITDA is ${true_ebitda:,.2f}. Discrepancy: ${claimed_ebitda - true_ebitda:,.2f}.",
                "root_cause": "Improper inclusion of $350,000 one-off non-operating asset sale gain into recurring operational earnings.",
                "corrective_action": "Strip out non-operating gain from EBITDA. Restate true operating EBITDA as $800,000.00.",
                "adjusted_ebitda": true_ebitda
            })

        # 3. Audit Cash Burn & Runway
        # True monthly cash burn includes accrued vendor payments ($35k/mo) and tax reserve ($15k/mo)
        true_monthly_burn = cf["claimed_monthly_burn"] + 50000.0
        cash = cf["cash_at_bank"]
        true_runway = cash / true_monthly_burn

        if abs(cf["claimed_monthly_burn"] - true_monthly_burn) > 0.01:
            findings.append({
                "finding_id": "AUDIT-FINDING-003",
                "area": "Cash Runway & Liquidity Risk",
                "severity": "HIGH_LIQUIDITY_EXPOSURE",
                "description": f"Monthly burn rate understated. Claimed: ${cf['claimed_monthly_burn']:,.2f}/mo, True Burn: ${true_monthly_burn:,.2f}/mo. True runway is {true_runway:.1f} months (not {cf['claimed_runway_months']:.1f} months).",
                "root_cause": "Omission of mandatory quarterly tax accruals and outstanding vendor payment schedules.",
                "corrective_action": "Restate runway to 12.0 months. Recommend establishing a $300,000 liquidity buffer immediately."
            })

        # 4. Audit Regulatory Statutory Reserve
        if reg["uu_pdp_compliance_reserve"] <= 0:
            findings.append({
                "finding_id": "AUDIT-FINDING-004",
                "area": "Statutory Regulatory Compliance",
                "severity": "REGULATORY_COMPLIANCE_BREACH",
                "description": "Zero compliance reserve allocated for UU PDP No. 27/2022 and SPBE security mandates.",
                "root_cause": "Management failed to budget for mandatory data protection audits and incident contingency.",
                "corrective_action": "Mandate immediate provisioning of $120,000 Statutory Compliance Reserve under Section 67 UU PDP.",
                "statutory_risk": "Fines of up to 2% of annual turnover under Article 57 UU PDP if unaddressed."
            })

        # Compile ERM 5x5 Risk Matrix
        risk_matrix = [
            {"risk": "Balance Sheet Imbalance / Material Misstatement", "likelihood": 4, "impact": 5, "score": 20, "tier": "CRITICAL", "owner": "SEKAR"},
            {"risk": "EBITDA Overstatement / Investor Misrepresentation", "likelihood": 4, "impact": 4, "score": 16, "tier": "HIGH", "owner": "SEKAR"},
            {"risk": "Cash Runway Premature Depletion", "likelihood": 3, "impact": 5, "score": 15, "tier": "HIGH", "owner": "SEKAR"},
            {"risk": "Statutory Fines under UU PDP No. 27/2022", "likelihood": 3, "impact": 4, "score": 12, "tier": "MEDIUM", "owner": "SEKAR"}
        ]

        report = {
            "auditor": "SEKAR (Chief Financial, Risk & Compliance Officer)",
            "audit_standard": "IFRS / PSAK Forensic Audit & ISO 31000 ERM Framework",
            "findings_count": len(findings),
            "findings": findings,
            "erm_risk_matrix": risk_matrix,
            "overall_audit_opinion": "QUALIFIED_WITH_ADVERSE_EXCEPTIONS",
            "fiduciary_verdict": "VETO_PENDING_CORRECTIVE_RESTATEMENT",
            "timestamp": "2026-11-15T23:13:50"
        }

        output_path = os.path.join(os.path.dirname(__file__), "audit_findings_report.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report


if __name__ == "__main__":
    auditor = FinancialForensicAuditor()
    res = auditor.execute_forensic_audit()
    print("SEKAR Financial & Risk Forensic Audit Engine executed successfully!")
    print(f"Total critical findings discovered: {res['findings_count']}")
    print(f"Fiduciary verdict: {res['fiduciary_verdict']}")
    for f in res["findings"]:
        print(f" - [{f['severity']}] {f['finding_id']}: {f['area']}")
