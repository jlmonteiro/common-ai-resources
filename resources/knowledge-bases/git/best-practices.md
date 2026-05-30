# Git Best Practices

## Commit Hygiene

- Commit early, commit often — but keep commits logical
- Each commit should compile/pass tests independently
- Don't mix formatting changes with logic changes
- Stage specific files (`git add file`) over `git add .`

## History Management

- Prefer squash merge for PRs (clean main history)
- Use rebase to keep feature branches up to date with main
- Never rewrite history on shared branches
- Use `--no-ff` merge only when preserving branch history matters

## Security

- Never commit secrets, tokens, or credentials
- Use `.gitignore` to exclude sensitive files
- If a secret is accidentally committed, rotate it immediately (history is permanent)
- Use environment variables or secret managers for sensitive values

## .gitignore

Maintain a comprehensive `.gitignore` from day one:

- Build artifacts
- IDE files
- OS files (.DS_Store, Thumbs.db)
- Environment files (.env)
- Dependencies (node_modules, .venv)

## Collaboration

- Pull before you push — avoid unnecessary merge conflicts
- Communicate when working on the same files
- Use draft PRs for early feedback on direction
- Write meaningful commit messages — your future self will thank you

## Recovery

- Use `git stash` for temporary work-in-progress
- Use `git reflog` to recover lost commits
- Prefer `git revert` over `git reset --hard` for undoing public commits
- Create a backup branch before risky operations

## Repository Hygiene

- Keep the repository focused — one project per repo
- Archive unused branches periodically
- Use tags for releases, not branches
- Keep `.gitattributes` for consistent line endings across platforms
