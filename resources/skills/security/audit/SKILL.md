---
name: "security-audit"
description: "Deep security audit of a codebase or specific area. Checks authentication, authorization, secrets, input validation, dependencies, and data protection. Use when user says 'security audit', 'check security', 'is this secure', 'vulnerability check', or 'pen test review'."
---

# Security Audit

## Prerequisites

Search the following knowledge bases:
- **security** — auth patterns, secrets, input validation, data protection, headers
- **api** — error format (no internal details leaked), status codes (401 vs 403)
- **logging** — sensitive data never logged
- Project's language scope — framework-specific security patterns

## Step 1: Determine Scope

Ask the user:

> "What do you want to audit?
> 1. Full codebase
> 2. Specific area (auth, API, data layer, dependencies)
> 3. Specific files/PR"

## Step 2: Execute Audit

Run each area as a focused check (sub-agent if available, sequential if not):

### 2.1 Authentication & Session

- Token validation on every endpoint (not just login)
- Token expiration and refresh logic
- Session invalidation on password change
- No custom auth schemes (use OAuth 2.0 / OIDC)

### 2.2 Authorization

- Deny by default — explicit grants only
- Resource ownership validated (user A can't access user B's data)
- No authorization logic in controllers (must be in service layer)
- All failures logged

### 2.3 Input Validation

- All inputs validated at API boundary
- Parameterized queries (no string concatenation in SQL)
- No user input passed to shell commands
- File uploads: type validated by magic bytes, size limited
- URLs: protocol and domain allowlisted

### 2.4 Secrets & Configuration

- No hardcoded secrets in source code
- No secrets in environment variables committed to git
- `.env` files in `.gitignore`
- Secrets injected at runtime (not build time)
- No secrets in Docker image layers

### 2.5 Data Protection

- Sensitive data encrypted at rest
- Passwords hashed (bcrypt/scrypt/Argon2 — never MD5/SHA)
- PII handling compliant (no unnecessary storage)
- No sensitive data in logs (check logging statements)
- No internal details in error responses (ProblemDetail without stack traces)

### 2.6 HTTP Security

- HSTS header present
- Content-Security-Policy configured
- X-Frame-Options: DENY
- CORS properly restricted (not wildcard `*` in production)
- Rate limiting on all endpoints

### 2.7 Dependencies

- No known vulnerabilities (check CVE databases)
- All versions pinned
- No unused dependencies (attack surface)
- Transitive dependencies audited

## Step 3: Classify Findings

| Severity | Criteria |
|----------|----------|
| 🔴 Critical | Exploitable vulnerability, data exposure, auth bypass |
| 🟡 High | Missing protection that could be exploited with effort |
| 🟢 Medium | Best practice violation, defense-in-depth gap |
| ℹ️ Info | Hardening suggestion, not currently exploitable |

## Step 4: Present Report

```
## Security Audit Report

**Scope:** {what was audited}
**Findings:** 🔴 {N} | 🟡 {N} | 🟢 {N} | ℹ️ {N}

### 🔴 Critical

#### SQL Injection in OrderRepository.java:28
**Risk:** Attacker can extract/modify database contents
**Evidence:** String concatenation in query: `"SELECT * FROM orders WHERE id = '" + id + "'"`
**Fix:** Use parameterized query or JPA named parameter

### 🟡 High

#### Missing rate limiting on /api/v1/auth/login
**Risk:** Brute force attack on credentials
**Fix:** Add rate limiter (e.g., 5 attempts per minute per IP)

...
```

## Step 5: Offer Remediation

Ask: "Would you like me to fix these findings? I'll address critical issues first."

For each fix:
1. Write a failing test that demonstrates the vulnerability
2. Apply the fix
3. Verify the test passes
