---
name: performance-engineering
description: Profile system bottlenecks, optimize algorithmic complexity, tune database query execution plans, configure caching strategies, and conduct load stress testing. Use when tuning latency, throughput, or resource consumption.
---

# SKILL: Performance Engineering & System Optimization

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Systems & SRE category.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To maximize computational throughput, minimize end-to-end response latency (p95/p99), and reduce cloud resource consumption through rigorous empirical profiling, indexing, caching, and algorithmic optimization.

## 2. SCOPE
- CPU/Memory profiling (py-spy, clinic.js, pprof), database execution plan analysis (`EXPLAIN ANALYZE`), Redis caching topologies, asynchronous I/O optimization, and load/stress testing (k6, Locust).

## 3. CORE OPTIMIZATION METHODOLOGY
1. **Never Optimize Without Measurement:** Always capture baseline benchmarks before attempting code or infrastructure changes.
2. **Amdahl's Law Focus:** Target the largest latency contributor (typically I/O, database round-trips, or network calls) first.
3. **Multi-Tiered Caching:** In-memory L1 cache (LRU) -> Distributed L2 cache (Redis) -> Edge CDN cache (Cloudflare).

## 4. STEP-BY-STEP PROCEDURE
1. **Benchmark Baseline:** Measure latency distribution (p50, p95, p99) under simulated concurrent load.
2. **Profile Hotspots:** Run flamegraphs and query analyzers to isolate the root bottleneck.
3. **Database Indexing & Query Tuning:**
   - Eliminate sequential scans on tables > 10,000 rows.
   - Replace N+1 queries with single batched queries (`JOIN` or `IN`).
4. **Connection Pooling & Asynchronous I/O:** Tune connection pool limits to prevent database connection exhaustion.
5. **Re-Test & Verify:** Run identical load benchmark to mathematically prove performance delta.

## 5. PERFORMANCE ACCEPTANCE TARGETS
- API p99 latency < 200 ms under standard peak load.
- Database CPU utilization < 65% during peak traffic bursts.
- Memory leak free (flat memory utilization profile over sustained 24-hour run).

## 6. CONSTRAINTS
- Do not sacrifice code correctness, security, or maintainability for premature micro-optimizations.
- Do not cache sensitive user data without explicit TTL and cache-invalidation hooks.
