---
name: jakarta-repository-connector
description: Query, fetch, and analyze public datasets, government regulations, and municipal documents from Satu Data Jakarta (data.jakarta.go.id) and Repositori SPBE DKI Jakarta. Use when researching Jakarta regional data, APBD budgets, demographic statistics, or municipal regulations.
---

# SKILL: Jakarta Regional Repository & Open Data Connector

> **Origin:** NEXUS Regional Intelligence Suite  
> **Classification:** Public Sector Data & Document Connector  
> **Author:** NEXUS Research & Intelligence Board  
> **Target Owner:** NAYA (Director of Research & Intelligence) | Shared: SEKAR (Finance & Compliance)

---

## 1. PURPOSE & OBJECTIVE
To empower NEXUS AI agents to search, extract, analyze, and synthesize official open datasets, statistical publications, and regulatory documents from Jakarta provincial government repositories, including **Satu Data Jakarta (`data.jakarta.go.id`)**, **Repositori SPBE DKI Jakarta (`repositorispbe.jakarta.go.id`)**, and **BPS DKI Jakarta**.

## 2. SCOPE
- Querying Jakarta Open Data CKAN/REST APIs, parsing CSV/JSON/XLSX public datasets (APBD budget realization, public transport passenger volume, MSME distributions, demographic statistics), ingesting Pergub/Perda regulations from Repositori SPBE, and caching in `knowledge/jakarta-repository/`.

## 3. PRIMARY REPOSITORIES
1. **Satu Data Jakarta (`data.jakarta.go.id`):** Official open data portal of the DKI Jakarta Provincial Government managed by Diskominfotik.
   - Topics: Economy, Transportation, Health, Demographics, Environment, Regional Finance.
2. **Repositori SPBE DKI Jakarta (`repositorispbe.jakarta.go.id`):** Centralized repository for Electronic-Based Government System architectural frameworks, enterprise blueprints, regulations, and IT master plans.
3. **BPS DKI Jakarta (`jakarta.bps.go.id`):** Official statistical agency data on inflation, Regional GDP (PDRB), and economic growth indicators.
4. **Local Repository Cache (`knowledge/jakarta-repository/`):** Pre-ingested regional datasets for instant zero-latency processing.

## 4. STEP-BY-STEP PROCEDURE
1. **Search Query Formulation:**
   - Define exact parameters (e.g. "Data Realisasi Pendapatan APBD DKI Jakarta 2025", "Jumlah Penumpang Transjakarta per Koridor", "Sebaran UMKM Jakarta Selatan").
2. **Endpoint Query / Scrape:**
   - Query `data.jakarta.go.id/api` or fetch relevant dataset resources.
   - Fallback to curated local datasets in `knowledge/jakarta-repository/`.
3. **Data Cleaning & Normalization:**
   - Filter corrupt rows, handle Indonesian currency number formats (Rp, comma vs. period decimal).
   - Normalize time series by month/year.
4. **Synthesis & Strategic Correlation:**
   - NAYA correlates municipal data with market opportunities.
   - SEKAR audits budget numbers and economic inflation indicators.
   - Output clean markdown summaries and data tables.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- Always cite exact Dataset Title, Dinas/OPD Penanggung Jawab, and Date of Publication.
- Differentiate between Realization (Realisasi) vs. Budget Target (Anggaran).

## 6. CONSTRAINTS
- Respect server rate-limits and robot policies of regional portals.
- Explicitly cite official government sources for all municipal indicators.
