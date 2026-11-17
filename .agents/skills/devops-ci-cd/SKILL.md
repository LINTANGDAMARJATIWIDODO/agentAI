---
name: devops-ci-cd
description: Formulate and maintain automated CI/CD deployment pipelines, containerization standards (Docker), release strategies (Blue-Green/Canary), and environment promotion. Use when building or optimizing build and deployment workflows.
---

# SKILL: DevOps & Automated CI/CD Pipeline Engineering

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) DevOps & Platform category.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To establish automated, deterministic continuous integration and deployment pipelines that build, test, scan, and deploy code changes with zero downtime and fast rollback capabilities.

## 2. SCOPE
- GitHub Actions / GitLab CI pipelines, multi-stage Dockerfiles, Helm charts, automated security scanning (SAST/DAST), artifact registry management, and release tagging.

## 3. CORE PIPELINE PHASES
```
[Commit / PR] -> [Lint & Typecheck] -> [Automated Unit/Integration Tests]
      |
      v
[Security & Vulnerability Scan (Trivy/Sonar)] -> [Container Build (Docker Multi-Stage)]
      |
      v
[Staging Deployment & Smoke Tests] -> [Canary / Blue-Green Production Rollout]
```

## 4. STEP-BY-STEP PROCEDURE
1. **Container Packaging:** Write optimized, multi-stage `Dockerfile` with non-root user execution and minimal base images (`alpine` or `distroless`).
2. **Configure CI Workflow:** Define automated pipeline triggers on pull requests and merges to `main`.
3. **Automate Quality Gates:** Block merge if test coverage drops below 80% or if high-severity CVEs are discovered.
4. **Implement Artifact Signing:** Sign container images using Cosign to prevent supply chain tampering.
5. **Zero-Downtime Deployment Strategy:** Configure Kubernetes rolling updates or Blue/Green router switching with automated health checks.

## 5. DOCKER BEST PRACTICE STANDARD
- Use `.dockerignore` to exclude node_modules, .git, and local secrets.
- Pin base image SHAs or specific versions (no `:latest` in production).
- Run application under dedicated unprivileged system user (`USER appuser`).

## 6. CONSTRAINTS
- Never bake credentials, private keys, or `.env` files into Docker images.
- Deployments must fail-safe: automatically roll back if post-deployment health probes fail.
