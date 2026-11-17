---
name: cybersecurity-hardening
description: Implement enterprise application security, OWASP Top 10 defenses, zero-trust network boundaries, secret lifecycle management, and threat modeling. Use when auditing code security or hardening system configurations.
---

# SKILL: Enterprise Cybersecurity & Zero-Trust Hardening

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Security & AppSec category.  
> **Target Owner:** RAKA (Director of Technology) | Shared: SEKAR (Compliance / Risk)

---

## 1. PURPOSE & OBJECTIVE
To enforce proactive, multi-layered defensive engineering across the enterprise tech stack, systematically defending against the OWASP Top 10 vulnerabilities, unauthorized privilege escalation, data breaches, and insider threats.

## 2. SCOPE
- Authentication/Authorization (OAuth 2.0, OpenID Connect, RBAC/ABAC), cryptographic controls, secret storage, input sanitization, network perimeter protection, and security audit logging.

## 3. CORE SECURITY PRINCIPLES
1. **Never Trust, Always Verify (Zero-Trust):** Every request must be authenticated, authorized, and encrypted, regardless of whether it originates internally or externally.
2. **Principle of Least Privilege (PoLP):** Processes, services, and users are granted only the minimum permissions required to perform their explicit function.
3. **Defense in Depth:** Multiple independent defensive layers (WAF, Gateway, Application Logic, Database Access Controls, Host Hardening).

## 4. OWASP TOP 10 MITIGATION MATRIX
- **Broken Access Control:** Centralized policy enforcement point (PEP); deny-by-default access model.
- **Cryptographic Failures:** AES-256-GCM for storage; TLS 1.3 with strong cipher suites; bcrypt/argon2id for password hashing.
- **Injection (SQL, NoSQL, Command):** Strictly parameterized queries; ORM sanitization; prohibition of shell string concatenation.
- **Insecure Design:** Threat modeling (STRIDE) during architecture phase before writing code.
- **Security Misconfiguration:** Automated container linting; disabling debug endpoints in production.
- **Vulnerable and Outdated Components:** Automated daily dependency scanning (Dependabot / Snyk).
- **Identification & Authentication Failures:** Multi-factor authentication (MFA); brute-force rate limits; secure session cookies (`HttpOnly`, `Secure`, `SameSite=Strict`).
- **Software & Data Integrity Failures:** Signed container images; checksum verification on downloaded packages.
- **Security Logging & Monitoring Failures:** Immutable structured audit logs (`logs/activity_log.json`); alerting on repeated auth failures.
- **Server-Side Request Forgery (SSRF):** Whitelist outbound IP ranges; disallow metadata endpoints (`169.254.169.254`).

## 5. CONSTRAINTS & SECURITY RULES
- Under no circumstances shall an API key, private key, or password be committed to version control.
- Hardcoded test credentials must never be deployed to staging or production.
