# Requirements Best Practices

## Dos

### Write Testable Requirements

Every requirement must have a clear pass/fail condition. If you cannot write a test for it, it is not a requirement — it is a wish.

- Use EARS syntax to enforce structure
- Include measurable acceptance criteria
- Specify boundary values and thresholds explicitly

**Good:** "When the user submits a form with an email exceeding 255 characters, the system shall reject the input and display a validation error within 200ms."

**Bad:** "The system should handle long emails gracefully."

### Challenge Every Requirement

Before accepting a requirement, ask:

1. **Why?** — What business value does this deliver?
2. **What if not?** — What happens if we skip this?
3. **How do we know it works?** — What is the acceptance test?
4. **Who benefits?** — Is the stakeholder identified?
5. **Is it atomic?** — Can it be broken down further?

### Separate Concerns

- One requirement = one behavior
- Do not combine functional and non-functional in the same statement
- Keep "what" (requirements) separate from "how" (design)

### Use Consistent Language

| Word | Meaning |
|------|---------|
| **SHALL** | Mandatory requirement (must be implemented) |
| **SHOULD** | Recommended but not mandatory |
| **MAY** | Optional, at implementer's discretion |
| **SHALL NOT** | Explicitly prohibited |

Reference: RFC 2119 / IEEE 830 / EARS pattern.

### Prioritize Ruthlessly

Use MoSCoW and enforce it:

- **Must** — System is unusable without this
- **Should** — Important but workaround exists
- **Could** — Desirable if time/budget allows
- **Won't** — Explicitly out of scope (document why)

Every requirement defaults to "Won't" until justified upward.

### Trace Requirements

Every requirement must link to:
- A business goal or user journey (upstream)
- A test scenario (downstream)
- A design decision (lateral)

Orphan requirements indicate scope creep or missing context.

---

## Don'ts

### Don't Write Implementation as Requirements

- ❌ "The system shall use PostgreSQL 15 with connection pooling"
- ✅ "The system shall persist user data with ACID guarantees and support 500 concurrent connections"

Technology choices belong in design documents, not requirements.

### Don't Use Ambiguous Language

Banned words in requirements:

| Ambiguous | Replace With |
|-----------|-------------|
| "fast" | "within 200ms at p95" |
| "secure" | "encrypted with TLS 1.3, authenticated via OAuth 2.0" |
| "user-friendly" | specific UX criteria (clicks, time-to-task) |
| "scalable" | "handle 10,000 concurrent users with <1% error rate" |
| "reliable" | "99.9% uptime measured monthly" |
| "efficient" | specific resource bounds (CPU, memory, time) |
| "flexible" | specific extension points or configuration options |
| "robust" | specific failure modes and recovery behaviors |

### Don't Gold-Plate

- Don't add requirements "just in case"
- Don't specify features no stakeholder requested
- Don't over-specify non-functional requirements beyond actual needs
- If nobody will test it, nobody needs it

### Don't Skip Negative Requirements

Document what the system shall NOT do:
- "The system shall NOT store plaintext passwords"
- "The system shall NOT expose internal error details to end users"
- "The system shall NOT allow concurrent modification without conflict detection"

### Don't Ignore Dependencies

Every requirement must declare:
- What it depends on (other requirements, external systems)
- What depends on it (downstream requirements)
- Assumptions that must hold true

---

## Robustness

### Define Failure Modes Explicitly

For every external dependency, specify:
1. **What can fail** — network timeout, invalid response, service unavailable
2. **How to detect** — health checks, timeouts, error codes
3. **How to respond** — retry, fallback, degrade, fail fast

### Specify Boundary Conditions

- Maximum input sizes
- Rate limits and throttling behavior
- Timeout values for all operations
- Behavior at capacity limits

### Require Graceful Degradation

- "If the recommendation service is unavailable, the system shall display default content within 500ms"
- "If the database connection pool is exhausted, the system shall queue requests for up to 5 seconds before returning HTTP 503"

### Validate All Inputs

Requirements must specify:
- Accepted input formats and ranges
- Rejection behavior for invalid inputs
- Sanitization rules for untrusted data

---

## Security

### Authentication and Authorization

- Specify authentication mechanism (OAuth 2.0, OIDC, mTLS)
- Define authorization model (RBAC, ABAC, policy-based)
- Require principle of least privilege
- Specify session management (timeout, revocation, concurrent sessions)

### Data Protection

- Classify data sensitivity (public, internal, confidential, restricted)
- Specify encryption requirements (at rest: AES-256, in transit: TLS 1.3)
- Define data retention and deletion policies
- Require PII handling compliance (GDPR, CCPA as applicable)

### Secure Defaults

Requirements must specify secure-by-default behavior:
- "The system shall deny access unless explicitly granted"
- "The system shall log all authentication failures"
- "The system shall reject requests without valid authentication tokens"
- "The system shall enforce HTTPS for all endpoints"

### Attack Surface

Address in requirements:
- Input validation against injection (SQL, XSS, command injection)
- Rate limiting against brute force and DDoS
- CSRF protection for state-changing operations
- Secrets management (no hardcoded credentials, externalized secret storage)

### Audit and Compliance

- "The system shall log all access to sensitive data with user identity, timestamp, and action"
- "The system shall retain audit logs for minimum 90 days"
- "The system shall support compliance reporting for [standard]"

---

## Resilience

### Define SLOs Before Implementation

Every service must have:
- **Availability target** — e.g., 99.9% (8.76h downtime/year)
- **Latency target** — e.g., p50 < 100ms, p99 < 500ms
- **Error budget** — acceptable failure rate before action is required

### Circuit Breaker Requirements

Specify the behavior, not the implementation. Examples (adapt thresholds to your context):

- "When error rate exceeds {threshold}% over {window}, the system shall stop sending requests to the failing dependency"
- "While the dependency is unavailable, the system shall return cached/default responses"
- "The system shall periodically probe the dependency and resume normal operation upon recovery"

### Retry and Backoff

- Specify maximum retry count
- Require the system to avoid retry storms (design chooses the mechanism)
- Define idempotency requirements for retried operations
- Specify which errors are retryable vs terminal

### Data Consistency

- Specify consistency model (strong, eventual, causal)
- Define conflict resolution strategy
- Require idempotent operations for at-least-once delivery
- Specify acceptable staleness window for eventually consistent reads

### Recovery Requirements

- **RTO (Recovery Time Objective)** — maximum acceptable downtime
- **RPO (Recovery Point Objective)** — maximum acceptable data loss
- Specify backup frequency and retention
- Require documented and tested recovery procedures

### Observability

- "The system shall emit structured logs for all business-critical operations"
- "The system shall expose health check endpoints returning status within 100ms"
- "The system shall publish metrics for latency, error rate, and throughput"
- "The system shall support distributed tracing across service boundaries"

---

## Industry Standards Reference

| Standard | Scope | Use When |
|----------|-------|----------|
| IEEE 830 (SRS) | Software requirements specification structure | Formal documentation |
| EARS | Requirements syntax patterns | Writing acceptance criteria |
| RFC 2119 | Requirement keywords (SHALL, SHOULD, MAY) | Consistent language |
| ISO 25010 | Software quality characteristics | Non-functional requirements |
| OWASP ASVS | Application security verification | Security requirements |
| NIST 800-53 | Security and privacy controls | Compliance requirements |
| ISO 27001 | Information security management | Security governance |
| SRE (Google) | Reliability engineering practices | SLOs, error budgets, resilience |

---

## Requirements Quality Checklist

Before finalizing any requirement, verify:

- [ ] **Atomic** — Describes exactly one behavior
- [ ] **Testable** — Has clear pass/fail criteria
- [ ] **Traceable** — Links to business goal and test scenario
- [ ] **Unambiguous** — No banned words, uses EARS syntax
- [ ] **Prioritized** — Has MoSCoW classification with justification
- [ ] **Bounded** — Specifies limits, timeouts, and edge cases
- [ ] **Secure** — Addresses relevant attack vectors
- [ ] **Resilient** — Defines failure behavior, not just happy path
- [ ] **Independent** — Can be implemented and verified in isolation
- [ ] **Necessary** — Stakeholder confirmed, not gold-plated
