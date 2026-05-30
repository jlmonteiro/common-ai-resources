---
name: "create-branch"
description: "Create a new branch before starting work. Asks for context to determine proper naming. Use when user says 'create branch', 'start branch', 'new branch', 'start working on', or 'begin feature'."
---

# Create Branch

## Prerequisites

Before executing any step, search the **git/branching** knowledge base for naming conventions and workflow rules.

## Step 1: Gather Context

Ask the user:

1. **What type of change?** — feature, fix, docs, or chore
2. **Brief description** — what will this branch deliver?
3. **Issue number** (optional) — is there a linked issue?

## Step 2: Derive Branch Name

Apply the naming convention from the **git/branching** knowledge base:

Format: `<type>/<short-description>`

Rules:
- Use kebab-case
- Keep under 50 characters
- Include issue number if provided

Examples based on user input:

| User says | Branch name |
|-----------|-------------|
| "adding a new KB for Docker" | `feature/docker-knowledge-base` |
| "fix the MCP crash on empty dir" | `fix/mcp-empty-dir-crash` |
| "update the getting started docs" | `docs/update-getting-started` |
| "upgrade fastembed, issue #12" | `chore/12-upgrade-fastembed` |

Present the suggested name and ask for confirmation.

## Step 3: Ensure Clean State

Before creating the branch:

- Check for uncommitted changes (`git status`)
- If changes exist, ask: stash them or commit first?
- Ensure we're on `main` and it's up to date:

```bash
git checkout main
git pull origin main
```

## Step 4: Create and Switch

```bash
git checkout -b <branch-name>
```

## Step 5: Confirm

Report:
- Branch created and checked out
- Remind the user to commit often and push when ready
