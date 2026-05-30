# Branching Strategy

## Model: GitHub Flow

A simplified trunk-based workflow suitable for continuous delivery.

## Branches

| Branch | Purpose | Lifetime |
|--------|---------|----------|
| `main` | Production-ready code, always deployable | Permanent |
| `feature/<name>` | New features | Short-lived |
| `fix/<name>` | Bug fixes | Short-lived |
| `docs/<name>` | Documentation changes | Short-lived |
| `chore/<name>` | Maintenance, tooling | Short-lived |

## Branch Naming

Format: `<type>/<short-description>`

- Use kebab-case for the description
- Keep it under 50 characters
- Include issue number when applicable

**Examples:**

```
feature/mcp-semantic-search
fix/empty-kb-crash
docs/add-mcp-setup-guide
chore/upgrade-fastembed
feature/42-add-kiro-adapter
```

## Workflow

```
main ─────────────────────────────────────────────── main
       \                                         /
        └── feature/new-kb ── commits ── PR ────┘
```

1. Create branch from `main`
2. Make focused commits (conventional commits)
3. Push branch and open Pull Request
4. Review, CI passes, approve
5. Squash merge into `main`
6. Delete branch

## Rules

- Never push directly to `main`
- Keep branches short-lived (hours to days, not weeks)
- One concern per branch — don't mix features with fixes
- Rebase on `main` before merging if behind
- Delete branches after merge

## When to Use Feature Branches vs Direct Commits

| Scenario | Approach |
|----------|----------|
| New feature or significant change | Feature branch + PR |
| Bug fix | Fix branch + PR |
| Typo or one-line doc fix | Direct to `main` (if sole maintainer) |
| Experimental/exploratory work | Feature branch (may be discarded) |
