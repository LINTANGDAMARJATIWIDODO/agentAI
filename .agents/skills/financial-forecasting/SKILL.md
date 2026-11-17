---
name: financial-forecasting
description: Build multi-scenario 3-statement financial forecasts (Income Statement, Balance Sheet, Cash Flow), run Monte Carlo simulations, stress-test working capital, and project cash runway. Use when forecasting corporate financials.
---

# SKILL: Enterprise Financial Forecasting & Multi-Scenario Modeling

> **Origin:** Original NEXUS Enterprise Skill (Proprietary Workforce Asset)  
> **Classification:** Corporate Finance & Treasury Standard  
> **Author:** NEXUS Finance & Compliance Board  
> **Target Owner:** SEKAR (Director of Finance, Risk & Compliance)

---

## 1. OBJECTIVE
To construct mathematically linked, dynamically variable, 36-to-60-month three-statement financial models that accurately forecast corporate revenues, cash runways, capital expenditure depreciation, and working capital needs across multiple economic scenarios.

## 2. SCOPE
- Integrated Income Statement, Balance Sheet, and Cash Flow Statement; Scenario Modeling (Base, Bull, Bear); Monte Carlo risk distribution; Burn Rate and Runway analysis; Working Capital cycle management.

## 3. EXECUTION METHODOLOGY
- **Three-Statement Dynamic Linking:** Net Income flows into Retained Earnings (Balance Sheet) and Operating Cash Flow (Cash Flow Statement); CAPEX increases Gross PP&E and flows into Cash Flow from Investing.
- **Driver-Based Forecasting:** Modeling revenue bottom-up through operational drivers (New Deals x Average Contract Value x Retention Rate) rather than arbitrary percentage growth.
- **Scenario & Stress-Testing:**
  - *Base Case:* Most probable operational forecast based on confirmed pipelines.
  - *Bull Case (Upside):* 25% faster sales velocity, 15% higher contract value.
  - *Bear Case (Downside):* 40% reduction in new enterprise acquisition, 30% increase in cloud inference costs.

## 4. DECISION RULES & CRITERIA
1. Cash is King: Solvency must be evaluated based on Free Cash Flow to the Firm (FCFF), not merely accrual accounting EBITDA.
2. The Cash Runway in the Bear Case scenario must never drop below 6 months of operational burn without triggering an immediate capital preservation alert.
3. Debt and financing interest must be explicitly modeled if debt instruments are utilized.

## 5. QUALITY STANDARDS & INTEGRITY RULES
- The Balance Sheet MUST balance (`Total Assets == Total Liabilities + Shareholder Equity`) across all forecasted periods.
- Every formula must be documented with explicit growth rates, depreciation schedules, and tax assumptions.
- Projections must account for seasonal corporate buying patterns (e.g., enterprise budget flushing in Q4).

## 6. CONSTRAINTS
- DILARANG: Projecting "hockey stick" revenue growth without modeling corresponding increases in headcount, infrastructure OPEX, and support costs.
- DILARANG: Assuming 100% on-time accounts receivable collections; bad debt allowance must be modeled.

## 7. EXPECTED OUTPUT FORMAT
- **Executive Financial Projections Summary (Base vs. Bull vs. Bear)**
- **Integrated Three-Statement Model Table (Monthly Year 1, Quarterly Years 2-3)**
- **Cash Runway & Monthly Net Burn Trajectory Chart Data**
- **Sensitivity Matrix (Gross Margin vs. Sales Cycle Length)**
- **CFO Recommendations on Capital Allocation**

## 8. EXAMPLE USAGE
SEKAR stress-tests a proposed $2M expansion plan against a 6-month delay in enterprise client procurement, calculating the exact buffer capital needed to avoid insolvency.
