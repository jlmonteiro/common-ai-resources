---
name: "create-pr"
description: "Create a pull request for the current changes. If on main, moves commits to a new branch first. Use when user says 'create PR', 'open PR', 'create pull request', 'send for review', or 'create merge request'."
---

# Create Pull Request

## Prerequisites

Before executing any step, search the **git/** knowledge bases for applicable guidelines, rules, and templates. Key references:

- **git/pull-requests** — PR title format, description template, review process
- **git/branching** — branch naming conventions, workflow
- **git/commit-messages** — conventional commits for PR title
- **git/best-practices** — history management

## Step 0: Check Current Branch

Determine the current branch. If on `main`, go to Step 1. Otherwise, skip to Step 2.

## Step 1: Move Commits Off Main

If working directly on `main`, create a feature branch and move commits there.

### 1.1 Determine Branch Name

Based on the commits, derive a branch name following the **git/branching** knowledge base:

- Identify the primary commit type (`feat`, `fix`, `docs`, `chore`)
- Extract a short description from the commit subjects
- Format: `<type>/<short-description>`

Ask the user to confirm the branch name.

### 1.2 Create Branch and Reset Main

```bash
# Create new branch at current position
git branch <branch-name>

# Reset main back to origin
git reset --hard origin/main

# Switch to the new branch
git checkout <branch-name>
```

If `origin/main` doesn't exist (no push yet), determine how many commits to move:

```bash
# Count commits not yet pushed
git log --oneline origin/main..HEAD

# Or if no remote, ask user how many commits to move
git branch <branch-name>
git reset --hard HEAD~<n>
git checkout <branch-name>
```

## Step 2: Pre-Push Checks

Run these checks before pushing the new branch:

- **Lint**: Run `inv lint`
- **Tests**: Run `inv test`
- **Changelog**: Verify `CHANGELOG.md` has entries for `feat`/`fix`/`perf` commits
- **Version consistency**: If breaking changes exist, verify version bump in `pyproject.toml`
- **Docker build**: If `src/`, `pyproject.toml`, or Dockerfile changed, run `inv build`

## Step 3: Push Branch

```bash
git push -u origin <branch-name>
```

## Step 4: Create Pull Request

### 4.1 Compose PR Title

Use conventional commits format. Derive from the branch commits:

- Single commit → use that commit message as title
- Multiple commits → summarize the overall change

Refer to the **git/pull-requests** knowledge base for title format.

### 4.2 Compose PR Description

Generate the description using the PR template:

- **Summary** — what and why
- **Changes** — bullet list from commit messages
- **Testing** — what was verified (lint, tests, build)
- **Notes** — breaking changes, migration steps

### 4.3 Open PR

Use the platform CLI to create the PR:

```bash
# GitHub
gh pr create --title "<title>" --body "<description>" --base main

# GitLab
glab mr create --title "<title>" --description "<description>" --target-branch main
```

Ask the user which platform if not obvious from the remote URL.

## Step 5: Post-PR

- Display the PR URL
- Suggest assigning reviewers if applicable
- Remind about CI checks that will run on the PR
