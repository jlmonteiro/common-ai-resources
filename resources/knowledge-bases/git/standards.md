# Git Standards

## Commit Hygiene

- Each commit must compile/pass tests independently
- Never mix formatting changes with logic changes
- Stage specific files — never use `git add .`
- Never commit secrets, tokens, or credentials

## History Management

- Use squash merge for PRs (clean main history)
- Use rebase to keep feature branches up to date with main
- Never rewrite history on shared branches
- Prefer `git revert` over `git reset --hard` for undoing public commits

## Security

- Never commit `.env` files, API keys, private keys, or certificates
- If a secret is accidentally committed, rotate it immediately — git history is permanent
- Use `.gitignore` to exclude sensitive files from day one

## Collaboration

- Pull before you push
- Use draft PRs for early feedback on direction
- Keep branches short-lived (hours to days, not weeks)
- Delete branches after merge
