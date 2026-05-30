---
name: "update-changelog"
description: "Update CHANGELOG.md with new entries following Keep a Changelog format. Use when user says 'update changelog', 'add to changelog', 'log this change', or after completing a feature/fix."
---

# Update Changelog

## Step 1: Read Current Changelog

Read `CHANGELOG.md` to understand the current state and existing entries under `[Unreleased]`.

## Step 2: Determine Category

Classify the change into one of these categories:

| Category | Use for |
|----------|---------|
| **Added** | New features, new knowledge bases, new tools |
| **Changed** | Modifications to existing functionality |
| **Deprecated** | Features that will be removed in future versions |
| **Removed** | Features removed in this release |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

## Step 3: Write the Entry

Follow these rules:

- Write from the user's perspective — what changed for them
- Use imperative mood: "Add", "Fix", "Change" — not "Added", "Fixed"
- One entry per logical change — not per commit
- Be concise but specific
- Include context when not obvious

**Good examples:**

```markdown
### Added
- SDD knowledge base with requirements and design best practices
- `inv release` task for version bumping with semver

### Fixed
- MCP server crash when knowledge-bases directory is empty

### Changed
- Chunk size reduced from 1000 to 500 chars for better search precision
```

**Bad examples:**

```markdown
### Added
- stuff
- updated files
- fix bug
```

## Step 4: Insert Under [Unreleased]

Add the entry under the appropriate category heading within the `[Unreleased]` section. If the category doesn't exist yet, create it in this order: Added, Changed, Deprecated, Removed, Fixed, Security.

## Step 5: Verify

- Confirm the entry is under `[Unreleased]`
- Confirm correct category
- Confirm no duplicate entries
- Confirm markdown formatting is valid
