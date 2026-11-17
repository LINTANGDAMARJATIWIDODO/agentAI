---
name: data-engineering-pipelines
description: Architect and operate scalable ETL/ELT data pipelines, streaming architectures (Kafka/Redis Streams), lakehouse storage, and data quality frameworks. Use when engineering data ingestion, transformation, or analytical storage.
---

# SKILL: Enterprise Data Engineering & Ingestion Pipelines

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Data Engineering & Platform category.  
> **Target Owner:** RAKA (Director of Technology) | Shared: NAYA (Intelligence & Analytics)

---

## 1. PURPOSE & OBJECTIVE
To construct robust, fault-tolerant, high-throughput batch and streaming data pipelines that ingest, clean, normalize, and load diverse business data into analytical data warehouses and vector stores for intelligence synthesis.

## 2. SCOPE
- Ingestion connectors, stream processing (Kafka, Redis Streams), batch transformation (dbt, Apache Spark, DuckDB), schema evolution, data quality assertions (Great Expectations), and vector embeddings pipeline.

## 3. PIPELINE ARCHITECTURE (MEDALLION PATTERN)
```
[Raw Sources / APIs] 
       |
       v
[Bronze Layer]: Raw, immutable append-only ingestion storage.
       |
       v
[Silver Layer]: Cleaned, filtered, enriched, deduplicated data with schema validation.
       |
       v
[Gold Layer]: Aggregated, business-ready star-schema / data marts for NAYA & SEKAR.
```

## 4. STEP-BY-STEP PROCEDURE
1. **Source Contract Definition:** Establish schema definitions and SLA with upstream producers.
2. **Implement Ingestion Worker:** Formulate idempotent consumer workers handling backpressure and retries.
3. **Data Quality Gate:** Run automated checks: null-value limits, uniqueness, referential integrity, and value distribution bounds.
4. **Transform & Model:** Build clean star schemas or analytical views.
5. **Monitoring & Dead-Letter Queue (DLQ):** Route corrupted records to a DLQ for offline inspection rather than halting the pipeline.

## 5. QUALITY STANDARDS & METRICS
- Zero data loss guarantee on streaming ingestion (at-least-once with idempotent downstream deduplication).
- Pipeline latency SLAs explicitly monitored and reported.

## 6. CONSTRAINTS
- Never execute unmonitored mass-mutations directly against production OLTP databases.
- Isolate heavy analytical queries from transactional customer-facing databases using read-replicas or data warehouses.
