# :material-shield-search: Security Audit

Deep security review across 7 areas. Classifies findings by severity and offers TDD-based remediation.

!!! tip "Triggers"
    - "security audit" / "check security" / "is this secure"
    - "vulnerability check" / "pen test review"

!!! success "Expected Outcomes"
    - Findings: 🔴 Critical | 🟡 High | 🟢 Medium | ℹ️ Info
    - Each finding with risk, evidence, and fix
    - Remediation via TDD (failing test → fix → pass)

## Audit Areas

<div class="grid cards" markdown>

- :material-account-key: **Auth & Session**
- :material-account-lock: **Authorization**
- :material-shield-check: **Input Validation**
- :material-key-variant: **Secrets**
- :material-lock: **Data Protection**
- :material-web: **HTTP Headers**
- :material-package-variant: **Dependencies**

</div>

## Example

!!! example "Scenario: Audit finds multiple issues"

    **Step 1:** User: "Full codebase audit"

    **Step 2:** Agent checks all 7 areas:

    **Step 4 — Report:**

    ```
    ## Security Audit Report

    Scope: Full codebase
    Findings: 🔴 2 | 🟡 3 | 🟢 2 | ℹ️ 1

    🔴 SQL Injection in OrderRepository.java:28
       Risk: Attacker can extract/modify database contents
       Evidence: "SELECT * FROM orders WHERE id = '" + id + "'"
       Fix: Use parameterized query

    🔴 Hardcoded API key in application.yml
       Risk: Key exposed in git history
       Evidence: payment.gateway.key: "sk_live_abc123"
       Fix: Move to environment variable, rotate key immediately

    🟡 Missing rate limiting on /api/v1/auth/login
       Risk: Brute force attack on credentials
       Fix: Add rate limiter (5 attempts/minute/IP)

    🟡 CORS allows wildcard origin in production
       Risk: Any site can make authenticated requests
       Fix: Restrict to specific domains

    🟡 No network policy — all pods can communicate
       Risk: Compromised pod can reach any service
       Fix: Add default-deny NetworkPolicy
    ```

    **Step 5 — Remediation:**

    Agent: "Starting with critical issues. Writing test for SQL injection..."

    1. Test: sends `'; DROP TABLE orders; --` as ID → succeeds (vulnerability confirmed) ❌
    2. Fix: parameterized query
    3. Test: same input → returns 400 ✅

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/security/audit/SKILL.md)
