# Pull Requests

## Purpose

Pull requests (PRs) are the primary mechanism for code review, discussion, and quality assurance before changes reach `main`.

## PR Title

Follow the same format as commit messages (Conventional Commits):

```
<type>(<scope>): <subject>
```

- Max 72 characters
- Imperative mood, lowercase
- The title becomes the squash merge commit message

**Examples:**

```
feat(mcp): add list_knowledge_bases tool
fix(docs): correct Gemini CLI config path
docs: add git conventions knowledge base
```

## PR Description

Structure the description with:

```markdown
## Summary

Brief description of what this PR does and why.

## Changes

- Bullet list of specific changes made
- One item per logical change

## Testing

How the changes were verified:
- Unit tests added/updated
- Manual testing performed
- Build verified (`inv lint`, `inv test`)

## Notes

Any context reviewers need:
- Breaking changes
- Migration steps
- Related issues or PRs
```

## Workflow

### Opening a PR

1. Push your branch
2. Open PR against `main`
3. Fill in title and description
4. Assign reviewers if applicable
5. Ensure CI passes

### Review Process

- Reviewers check correctness, style, and completeness
- Use inline comments for specific feedback
- Approve when satisfied or request changes
- Author addresses feedback with new commits (don't force-push during review)

### Merging

- Use **squash merge** — produces a clean single commit on `main`
- The PR title becomes the commit message
- Delete the branch after merge

## Rules

- Every PR must have a clear title and description
- CI must pass before merge
- At least one approval required (for team projects)
- Keep PRs small and focused — one concern per PR
- Don't let PRs sit open for more than a few days

## PR Size Guidelines

| Size | Lines Changed | Review Time |
|------|--------------|-------------|
| Small | < 100 | Minutes |
| Medium | 100-400 | Hours |
| Large | 400+ | Split it up |

## Anti-Patterns

- ❌ PRs with 20+ files touching unrelated concerns
- ❌ "WIP" PRs left open for weeks
- ❌ Empty descriptions ("fixes stuff")
- ❌ Force-pushing during active review
- ❌ Merging without CI passing
