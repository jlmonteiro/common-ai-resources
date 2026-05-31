# Security Standards

## Authentication

### Patterns

- Use OAuth 2.0 / OpenID Connect for user authentication
- Use API keys for service-to-service communication (non-user context)
- Use mTLS for internal service mesh communication
- Never implement custom authentication schemes

### Token Handling

- Use short-lived access tokens (15-60 minutes)
- Use refresh tokens for session renewal (stored securely, rotated on use)
- Validate tokens on every request — never trust client-side state
- Validate issuer, audience, expiration, and signature on every JWT

### Session Management

- Invalidate sessions on password change
- Support concurrent session limits when required
- Implement idle timeout and absolute timeout
- Provide logout that revokes tokens server-side

## Authorization

### Model

- Use Role-Based Access Control (RBAC) as the default model
- Use Attribute-Based Access Control (ABAC) for fine-grained rules
- Enforce at the service layer — never rely on UI/client-side checks alone
- Apply principle of least privilege — grant minimum permissions needed

### Rules

- Deny by default — explicitly grant access, never explicitly deny
- Check authorization on every request, not just at login
- Validate resource ownership — user A cannot access user B's data
- Log all authorization failures

## Secrets Management

### Storage

- Never hardcode secrets in source code, config files, or environment variables committed to git
- Use a secrets manager (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- For local development, use `.env` files (always in `.gitignore`)
- For containers, inject via environment variables or mounted secrets at runtime

### Rotation

- All secrets must be rotatable without downtime
- Automate rotation where possible
- Set expiration on all credentials
- Revoke immediately if compromised — don't wait for expiration

### What Counts as a Secret

- Passwords, API keys, tokens
- Database connection strings with credentials
- TLS certificates and private keys
- Encryption keys
- OAuth client secrets
- Webhook signing keys

## Input Validation

### Principles

- Validate all input at the boundary (API layer) — never trust client data
- Use allowlists over denylists — define what's valid, reject everything else
- Validate type, length, format, and range
- Reject early — fail fast on invalid input before processing

### Common Attacks to Prevent

| Attack | Prevention |
|--------|-----------|
| SQL Injection | Parameterized queries — never string concatenation |
| XSS | Output encoding, Content-Security-Policy headers |
| Command Injection | Never pass user input to shell commands |
| Path Traversal | Validate and canonicalize file paths |
| SSRF | Allowlist outbound URLs, block internal ranges |
| Mass Assignment | Explicitly define allowed fields — never bind request to entity directly |

### Validation Rules

- Strings: max length, allowed characters (regex), trim whitespace
- Numbers: min/max range, integer vs decimal
- Emails: format validation + domain verification for critical flows
- URLs: protocol allowlist (https only), domain allowlist
- Files: type validation (magic bytes, not just extension), size limits
- IDs: validate format (UUID, numeric), verify existence and ownership

## Data Protection

### In Transit

- TLS 1.3 minimum for all external communication
- mTLS for internal service-to-service
- Never transmit sensitive data over unencrypted channels
- Use HSTS headers to enforce HTTPS

### At Rest

- Encrypt sensitive data in databases (column-level or full-disk)
- Hash passwords with bcrypt, scrypt, or Argon2 — never MD5/SHA
- Never store plaintext passwords, tokens, or keys
- Encrypt backups

### Data Classification

| Level | Examples | Handling |
|-------|---------|---------|
| Public | Marketing content, docs | No restrictions |
| Internal | Business data, metrics | Access control required |
| Confidential | PII, financial data | Encryption + audit logging |
| Restricted | Passwords, keys, health data | Encryption + strict access + retention limits |

## HTTP Security Headers

Every API and web application must include:

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS |
| `Content-Security-Policy` | Appropriate policy | Prevent XSS |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limit referrer leakage |

## Dependency Security

- Scan dependencies for known vulnerabilities (Dependabot, Snyk, OWASP Dependency-Check)
- Pin dependency versions — never use open ranges
- Update vulnerable dependencies within 7 days (critical) or 30 days (high)
- Audit transitive dependencies — not just direct ones

## Secure Defaults

- All endpoints require authentication unless explicitly public
- All data is encrypted in transit by default
- All logs exclude sensitive data by default
- All inputs are validated by default
- All errors hide internal details by default (use ProblemDetail without stack traces)
