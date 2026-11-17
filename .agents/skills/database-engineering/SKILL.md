---
name: database-engineering
description: Model enterprise relational and NoSQL database schemas, write idempotent migrations, design B-Tree/GIN indexes, manage transactions, and handle partitioning. Use when designing, migrating, or optimizing database schemas.
---

# SKILL: Enterprise Database Engineering & Schema Modeling

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Backend & Data category.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To engineer robust, normalized, highly performant relational and document database architectures capable of supporting heavy transactional (OLTP) and analytical (OLAP) enterprise workloads with strict ACID guarantees.

## 2. SCOPE
- PostgreSQL, MySQL, Redis, schema normalization (3NF) vs. purposeful denormalization, zero-downtime database migrations, composite/partial indexing, connection pooling, and read-replica routing.

## 3. CORE DESIGN PROTOCOLS
1. **Third Normal Form (3NF) Baseline:** Eliminate data redundancy and update anomalies before considering denormalization for specific high-read performance paths.
2. **Explicit Foreign Key Constraints:** Enforce referential integrity at the database engine level with appropriate `ON DELETE` cascading rules.
3. **Idempotent, Reversible Migrations:** Every schema migration script must have an exact, tested `down` migration rollback script.
4. **Targeted Indexing:** Index all foreign keys, query filter predicates (`WHERE`), and sorting columns (`ORDER BY`).

## 4. STEP-BY-STEP PROCEDURE
1. **Entity-Relationship Modeling:** Map business entities, relationships (1:1, 1:N, N:M), and cardinality constraints.
2. **Draft Schema DDL:** Define tables, primary keys (`UUIDv7` or `BIGSERIAL`), column types, and constraints (`NOT NULL`, `CHECK`).
3. **Create Migration Scripts:** Use Alembic (Python) or Prisma/Flyway with automated schema verification.
4. **Optimize Execution Plans:** Run `EXPLAIN (ANALYZE, BUFFERS)` to verify index usage and eliminate sequential scans.
5. **Partitioning & Archiving:** Plan range partitioning (e.g. by month/year) for append-heavy audit log tables.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- No table without an explicit primary key and `created_at`/`updated_at` audit timestamps.
- Zero table lockouts during production migrations (use `CREATE INDEX CONCURRENTLY`).

## 6. CONSTRAINTS
- Never execute destructive `DROP TABLE` or `ALTER COLUMN DROP` operations without a prior verified backup and multi-step release cadence.
- Prohibit storing unencrypted credentials, PII, or raw credit card data in database columns.
