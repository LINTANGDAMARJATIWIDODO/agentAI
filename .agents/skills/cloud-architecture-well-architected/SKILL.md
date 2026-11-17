---
name: cloud-architecture-well-architected
description: Evaluate and design multi-cloud infrastructures using the Well-Architected Framework (Operational Excellence, Security, Reliability, Performance, Cost Optimization, Sustainability). Use when designing or auditing cloud infrastructure.
---

# SKILL: Cloud Architecture & Well-Architected Framework

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Cloud & Systems category.  
> **Target Owner:** RAKA (Director of Technology) | Shared: SEKAR (Finance / Cost Audit)

---

## 1. PURPOSE & OBJECTIVE
To architect, evaluate, and operate high-reliability enterprise cloud topologies on AWS, Google Cloud, or Azure that balance resilience, data security, operational overhead, and fiscal efficiency.

## 2. THE 6 PILLARS OF WELL-ARCHITECTED DESIGN
1. **Operational Excellence:** Infrastructure as Code (Terraform), automated canary deployments, centralized telemetry (OpenTelemetry, Prometheus, Grafana).
2. **Security:** Zero-Trust perimeter, encryption at rest (AES-256) and in transit (TLS 1.3), least privilege IAM policies, automated secret rotation.
3. **Reliability:** Multi-Availability-Zone (Multi-AZ) redundancy, stateless worker scaling, automated database failover, RPO <= 1h, RTO <= 4h.
4. **Performance Efficiency:** Appropriate compute tier selection, distributed caching (Redis), CDN edge acceleration, asynchronous decoupling with message queues.
5. **Cost Optimization:** Rightsizing compute nodes, auto-scaling to zero for non-production environments, reserved/spot instance blending.
6. **Sustainability:** Efficient resource utilization and carbon footprint minimization.

## 3. STEP-BY-STEP PROCEDURE
1. **Workload Profiling:** Determine compute type (stateless web vs. stateful worker), peak traffic, and latency targets.
2. **Network Topology Design:** Configure VPCs, private subnets for databases/internal workers, public subnets for ingress load balancers, and NAT gateways.
3. **Data Tier Selection:** Pair relational OLTP workloads with managed PostgreSQL and caching with Redis.
4. **Draft Infrastructure as Code (IaC):** Formulate declarative Terraform / OpenTofu configurations.
5. **Generate Cloud Bill of Materials (BOM):** Compute precise monthly hosting projections for SEKAR's review.

## 4. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- Zero single points of failure (SPOF) on production critical paths.
- All database instances must reside in private subnets with no public IP exposure.
- Infrastructure costs must be audited against revenue projections.

## 5. CONSTRAINTS
- Prohibit manual click-ops changes in production cloud environments.
- Prohibit wildcard IAM permissions (`"Action": "*"`, `"Resource": "*"`).
