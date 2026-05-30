# Pull Request Conventions

## PR Title

Same format as commit messages (becomes the squash merge commit):

```
<type>[optional scope]: <subject>
```

Max 72 characters, imperative mood, lowercase.

## PR Description Template

```markdown
## Summary

Brief description of what this PR does and why.

## Changes

- Bullet list of specific changes made

## Testing

- How changes were verified (lint, tests, build)

## Notes

- Breaking changes, migration steps, related issues
```

## Rules

- Every PR must have a clear title and description
- CI must pass before merge
- Use squash merge — PR title becomes the commit message
- Delete branch after merge
- Keep PRs focused — one concern per PR
