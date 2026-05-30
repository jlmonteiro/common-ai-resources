# Design Document Best Practices

## Dos

### Trace Every Design Decision to Requirements

Every component, interface, and architectural choice must link back to one or more requirements. If a design element cannot be traced to a requirement, it is either:
- Scope creep (remove it)
- A missing requirement (add it first)

### Use C4 Model for Architecture Diagrams

Structure diagrams at four levels of abstraction:

| Level | Shows | Audience |
|-------|-------|----------|
| **Context** | System + external actors | Stakeholders, new team members |
| **Container** | Applications, databases, message brokers | Developers, architects |
| **Component** | Internal modules within a container | Developers working on that container |
| **Code** | Classes/interfaces (only when needed) | Developers implementing the component |

Reference: [C4 Model](https://c4model.com/)

### Design for Failure First

Every component interaction must specify:
1. **Happy path** — normal operation
2. **Failure path** — what happens when the dependency is unavailable
3. **Degraded path** — partial functionality when operating in reduced capacity
4. **Recovery path** — how the system returns to normal after failure

### Apply SOLID Principles at Component Level

- **Single Responsibility** — each component has one reason to change
- **Open/Closed** — extend behavior without modifying existing components
- **Liskov Substitution** — components behind interfaces are interchangeable
- **Interface Segregation** — clients depend only on interfaces they use
- **Dependency Inversion** — depend on abstractions, not concrete implementations

### Document API Contracts Explicitly

For every interface between components:
- Request/response schemas (with examples)
- Error codes and their meaning
- Versioning strategy
- Rate limits and quotas
- Idempotency guarantees
- Backward compatibility rules

### Separate Reads from Writes (CQRS Where Appropriate)

When designing data access:
- Identify read-heavy vs write-heavy paths
- Consider separate read models for complex queries
- Document consistency guarantees between read and write models
- Specify acceptable staleness for read models

### Include Capacity Planning

For each component, document:
- Expected throughput (requests/second)
- Resource requirements (CPU, memory, storage)
- Scaling strategy (horizontal, vertical, auto-scaling triggers)
- Bottleneck analysis and mitigation

---

## Don'ts

### Don't Design Without Constraints

Every design must state its constraints explicitly:
- ❌ "We'll use a microservice architecture"
- ✅ "Given the team size (4 developers), deployment frequency (daily), and independent scaling requirements for the search module, we'll extract search as a separate service"

### Don't Mix Abstraction Levels

Keep each design page at a consistent level of detail:
- ❌ Mixing high-level architecture with database column types in the same section
- ✅ Architecture overview links to data-models page for schema details

### Don't Ignore Cross-Cutting Concerns

Address these in dedicated sections, not scattered across component docs:

| Concern | Must Document |
|---------|--------------|
| Authentication | Where tokens are validated, session management |
| Authorization | Permission model, enforcement points |
| Logging | Format, levels, correlation IDs, what NOT to log |
| Monitoring | Metrics, alerts, dashboards |
| Configuration | How config is loaded, environment-specific overrides |
| Error handling | Error taxonomy, propagation strategy |

### Don't Over-Engineer

- Don't add abstraction layers "for future flexibility" without a concrete requirement
- Don't introduce distributed systems patterns (saga, event sourcing) unless the problem demands it
- Don't design for 10x scale when current requirements are 1x
- YAGNI (You Aren't Gonna Need It) applies to architecture too

### Don't Skip the "Why"

Every design decision must include rationale:
- ❌ "Use PostgreSQL for the database"
- ✅ "Use PostgreSQL because: ACID compliance required (NFR-3), team expertise exists, JSON support needed for flexible metadata (FR-12), and the expected data volume (< 1TB) fits single-node well"

### Don't Design in Isolation

- Reference existing system patterns and conventions
- Show integration points with existing infrastructure
- Document migration path from current state to target state
- Identify breaking changes and their impact

---

## Architectural Decision Records (ADRs)

### When to Write an ADR

- Technology selection (database, framework, language, protocol)
- Architectural pattern choice (monolith vs microservices, sync vs async)
- Integration strategy with external systems
- Security model decisions
- Data storage and consistency model choices
- Any decision that is costly to reverse

### ADR Quality Criteria

- **Technical depth** — Include specific versions, configurations, and constraints
- **Evidence-based** — Reference benchmarks, PoC results, load tests, or compatibility matrices
- **Alternatives exhaustive** — Document at least 2-3 alternatives with honest pros/cons
- **Reproducible** — Another engineer should be able to verify the evidence
- **Time-bound** — Record when the decision was made and what context existed at that time

### Dos

- Quantify claims: "Option A handles 12,000 req/s vs Option B at 8,500 req/s (benchmark link)"
- Document the evaluation criteria used to compare alternatives
- Include constraints that narrowed the options (team expertise, licensing, timeline)
- Link to related ADRs when decisions build on each other
- Record who participated in the decision

### Don'ts

- Don't write ADRs for trivial or easily reversible choices
- Don't use vague rationale: ❌ "it's the industry standard" ✅ "adopted by 3 of our 4 upstream dependencies, reducing integration effort"
- Don't omit rejected alternatives — future readers need to know what was considered
- Don't backfill ADRs without marking them as retrospective

### Lifecycle

- **Proposed** — Under discussion, evidence being gathered
- **Accepted** — Decision made, implementation can proceed
- **Deprecated** — No longer applies but kept for historical context
- **Superseded** — Replaced by a newer ADR (link to successor)

---

## Security Design

### Defense in Depth

Design multiple security layers — never rely on a single control:

1. **Network** — firewalls, network policies, mTLS between services
2. **Application** — input validation, output encoding, parameterized queries
3. **Data** — encryption at rest and in transit, data classification
4. **Identity** — authentication, authorization, least privilege
5. **Monitoring** — audit logs, anomaly detection, alerting

### Zero Trust Architecture

- Never trust network location as a security boundary
- Authenticate and authorize every request
- Encrypt all internal communication (mTLS)
- Validate tokens at every service boundary, not just the gateway

### Secrets Management

- No secrets in code, config files, or environment variables
- Use a secrets manager (Vault, KMS, cloud-native secret stores)
- Rotate secrets automatically
- Document secret lifecycle (creation, rotation, revocation)

### Threat Modeling (STRIDE)

For each component, assess:

| Threat | Question |
|--------|----------|
| **Spoofing** | Can an attacker impersonate a user or service? |
| **Tampering** | Can data be modified in transit or at rest? |
| **Repudiation** | Can actions be denied without evidence? |
| **Information Disclosure** | Can sensitive data leak? |
| **Denial of Service** | Can the service be overwhelmed? |
| **Elevation of Privilege** | Can a user gain unauthorized access? |

Reference: Microsoft STRIDE, OWASP Threat Modeling.

---

## Resilience Patterns

### Circuit Breaker

Document for each external dependency:
- **Closed state** — normal operation, tracking failure rate
- **Open state** — fast-fail, return fallback response
- **Half-open state** — probe with single request to test recovery
- **Thresholds** — failure rate and time window to trip

### Bulkhead

Isolate failures to prevent cascade:
- Separate thread pools per dependency
- Connection pool limits per downstream service
- Queue depth limits with backpressure

### Retry with Backoff

- Maximum retry count (typically 3)
- Exponential backoff with jitter
- Which errors are retryable (5xx, timeout) vs terminal (4xx)
- Idempotency requirements for safe retries

### Timeout Budget

For each request path, define:
- Total timeout budget (end-to-end SLA)
- Per-hop timeout allocation
- Timeout propagation (deadline headers)
- Behavior when budget is exhausted

---

## Data Design

### Schema Evolution Strategy

- Forward and backward compatibility rules
- Migration approach (expand-contract pattern)
- Versioning strategy for APIs and events
- Rollback plan for failed migrations

### Consistency Model

Document explicitly:
- Which operations require strong consistency
- Where eventual consistency is acceptable (and staleness window)
- Conflict resolution strategy for concurrent writes
- Ordering guarantees for events/messages

### Data Lifecycle

- Creation — who creates, validation rules
- Retention — how long data is kept, legal requirements
- Archival — when and where data moves to cold storage
- Deletion — hard delete vs soft delete, cascade rules, GDPR compliance

---

## Observability Design

### Three Pillars

| Pillar | Purpose | Design Consideration |
|--------|---------|---------------------|
| **Logs** | Debug individual requests | Structured JSON, correlation IDs, log levels |
| **Metrics** | Monitor system health | RED method (Rate, Errors, Duration) per service |
| **Traces** | Understand request flow | Distributed tracing across service boundaries |

### Health Check Design

Every service must expose:
- **Liveness** — "is the process running?" (restart if not)
- **Readiness** — "can it serve traffic?" (remove from load balancer if not)
- **Startup** — "has initialization completed?" (wait before checking liveness)

### Alerting Strategy

- Alert on symptoms (high error rate), not causes (CPU usage)
- Define severity levels with response expectations
- Include runbook links in alert definitions
- Avoid alert fatigue — every alert must be actionable

---

## Integration Design

### Synchronous vs Asynchronous

| Use Synchronous When | Use Asynchronous When |
|---------------------|----------------------|
| Response needed immediately | Fire-and-forget acceptable |
| Simple request-response | Long-running operations |
| Strong consistency required | Eventual consistency acceptable |
| Low latency required | Throughput more important than latency |

### Event-Driven Design

When using events:
- Define event schema with versioning
- Specify delivery guarantees (at-least-once, exactly-once)
- Document ordering guarantees
- Design for idempotent consumers
- Plan for dead letter queues and poison messages

### API Versioning

- URL path versioning (`/v1/`, `/v2/`) for breaking changes
- Header versioning for minor variations
- Sunset policy — how long old versions are supported
- Migration guide for consumers

---

## Industry Standards Reference

| Standard | Scope | Use When |
|----------|-------|----------|
| C4 Model | Architecture diagrams | Visualizing system structure |
| ISO 25010 | Quality attributes | Defining non-functional design goals |
| 12-Factor App | Cloud-native design | Designing deployable services |
| TOGAF | Enterprise architecture | Large-scale system design |
| Domain-Driven Design | Bounded contexts | Defining service boundaries |
| STRIDE | Threat modeling | Security design review |
| SRE (Google) | Reliability design | SLOs, error budgets, toil reduction |
| REST Maturity Model (Richardson) | API design | Designing RESTful interfaces |
| CNCF Landscape | Cloud-native tooling | Selecting infrastructure components |

---

## Design Quality Checklist

Before finalizing any design document, verify:

- [ ] **Traceable** — Every component links to requirements it fulfills
- [ ] **Justified** — Every decision includes rationale and alternatives considered
- [ ] **Failure-aware** — Failure modes documented for all external dependencies
- [ ] **Secure** — Threat model completed, defense in depth applied
- [ ] **Observable** — Logging, metrics, tracing, and health checks designed
- [ ] **Scalable** — Capacity planning included with scaling strategy
- [ ] **Testable** — Test scenarios defined that validate the design
- [ ] **Consistent** — Follows existing system patterns and conventions
- [ ] **Bounded** — Scope is clear, no gold-plating
- [ ] **Evolvable** — Migration path and backward compatibility addressed
