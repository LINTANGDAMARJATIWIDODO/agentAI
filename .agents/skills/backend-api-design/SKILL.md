---
name: backend-api-design
description: Design robust, versioned, idempotent, and secure RESTful and gRPC API contracts. Define OpenAPI schemas, pagination, error models, and rate limits. Use when designing or reviewing backend endpoints and API contracts.
---

# SKILL: Enterprise Backend API Design & Contract Governance

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Backend & API Architecture category.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To architect production-ready, standardized, resilient, and developer-friendly API endpoints adhering to RESTful standards, OpenAPI 3.1 specifications, idempotency principles, and zero-trust authentication protocols.

## 2. SCOPE
- REST API contracts, GraphQL schemas, gRPC protobuf definitions, payload validation, pagination, idempotency keys, error formatting (RFC 7807), and rate-limiting schemes.

## 3. CORE DESIGN PRINCIPLES
1. **Resource-Oriented REST:** Clear plural nouns for resources (`/api/v1/workspaces`, `/api/v1/tasks`).
2. **Deterministic Error Responses (RFC 7807):** Consistent structure `{ "type", "title", "status", "detail", "instance" }`.
3. **Idempotency for Mutating Operations:** Support `Idempotency-Key` header on POST/PUT requests to prevent duplicate transactions.
4. **Strict Schema Validation:** Reject unexpected fields, validate data types, string lengths, and ranges at the gateway level.

## 4. STEP-BY-STEP PROCEDURE
1. **Define API Requirements:** Map user workflows to required endpoints and data contracts.
2. **Draft OpenAPI 3.1 Contract:** Write JSON/YAML specification with request/response schemas.
3. **Implement Serialization & Validation:** Use Pydantic (Python) or Zod (TypeScript) for runtime type safety.
4. **Implement Standard Middleware:**
   - Correlation ID (`X-Request-ID`) propagation.
   - Authentication (JWT / Bearer token) and RBAC evaluation.
   - Rate limiting headers (`RateLimit-Limit`, `RateLimit-Remaining`).
5. **Add Comprehensive Integration Tests:** Test status codes (200, 201, 400, 401, 403, 404, 409, 422, 500).

## 5. STANDARD ERROR FORMAT (RFC 7807 EXAMPLE)
```json
{
  "type": "https://api.nexus-enterprise.ai/errors/validation-failed",
  "title": "Validation Error",
  "status": 422,
  "detail": "Field 'allocated_budget_idr' must be a positive integer.",
  "instance": "/api/v1/tasks/task-402"
}
```

## 6. CONSTRAINTS & SECURITY RULES
- Never expose internal database stack traces or raw SQL queries in error responses.
- Enforce strict CORS policies and prevent open redirect vulnerabilities.
- Mandatory TLS 1.3 encryption across all endpoints.
