---
name: "list-specifications"
description: "List all specifications with their status. Use when user says 'list specifications', 'show specs', 'what specifications exist', or 'spec status'."
---

# List Specifications

Display persistent requirements/design state and all task files with status.

## Steps

### 1. Check Structure Exists

```bash
[ -d .specs ] || echo "No specifications found. Run 'create requirements' to start."
```

### 2. Summarize Persistent Files

**Requirements:** List topic pages, count requirement IDs from index.

**Design:** List topic pages, count test scenarios.

### 3. List Task Files

For each task file, extract:
- Epic ID (or "Draft" if not yet accepted)
- Status (Draft / In Progress / Done)
- Story count
- Total estimate

### 4. Display Summary

```
Specifications:

Requirements:
  - requirements.md (index: {N} requirements)
  - {topic}.md, ...

Design:
  - design.md (index)
  - {topic}.md, ...
  - test-scenarios.md ({N} scenarios)

Tasks:
  | # | File | Status | Stories | Estimate |
  |---|------|--------|---------|----------|
  | 1 | 1-user-auth.tasks.md | In Progress | 4 | 24h |
  | 2 | 2-payments.tasks.md | Draft | 3 | 16h |

Next steps:
- Draft tasks ready: run 'create tasks'
- Missing design: run 'create design'
```
