---
name: "push"
description: "Push changes and prepare for merge. Runs pre-push checks to ensure the branch is ready for a pull request. Use when user says 'push', 'push changes', 'ready to merge', or 'prepare for PR'."
---

# Push Changes

## Prerequisites

Before executing any step, search the **git/** knowledge bases for applicable guidelines, rules, and templates. Key references:

- **git/branching** — branch naming, workflow rules
- **git/tagging** — version bumping rules
- **git/pull-requests** — PR title, description, review process
- **git/best-practices** — history management, collaboration

## Step 0: Detect Context

- Identify the current branch name
- Identify the remote (default: `origin`)
- Check if a remote tracking branch exists

## Step 1: Pre-Push Checks

### 1.1 Branch is Not Main

Verify the current branch is not `main`. If it is, invoke the **create-pr** skill which will move commits to a new branch before proceeding.

### 1.2 All Changes Committed

Check `git status` for uncommitted changes. If any exist, ask the user whether to commit them first (invoke the **commit** skill) or stash them.

### 1.3 Lint Passes

Run `inv lint`. If it fails, report the issues and ask the user to fix before pushing.

### 1.4 Tests Pass

Run `inv test`. If tests fail, report failures. Warn but allow the user to proceed if they choose.

### 1.5 Changelog Updated

If the branch contains `feat`, `fix`, or `perf` commits, verify `CHANGELOG.md` has corresponding entries under `[Unreleased]`. If not, invoke the **update-changelog** skill.

### 1.6 Version Consistency

If the branch contains breaking changes, verify the version in `pyproject.toml` has been bumped appropriately. Refer to the **git/tagging** knowledge base.

### 1.7 Rebase on Main

Check if the branch is behind `main`:

```bash
git fetch origin main
git log HEAD..origin/main --oneline
```

If behind, suggest rebasing:

```bash
git rebase origin/main
```

Warn about potential conflicts.

### 1.8 Docker Build (if applicable)

If files in `src/`, `pyproject.toml`, or `knowledge-base-mcp.dockerfile` were changed, run `inv build` to verify the Docker image still builds.

## Step 2: Push

Once all checks pass:

```bash
git push -u origin <branch-name>
```

Use `-u` to set up tracking on first push.

## Step 3: Post-Push

Suggest next steps:

- Open a Pull Request (provide the URL or command)
- Remind about PR title format (conventional commits)
- Remind about PR description template

Refer to the **git/pull-requests** knowledge base for PR guidelines.
