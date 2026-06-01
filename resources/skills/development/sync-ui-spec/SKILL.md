---
name: "sync-ui-spec"
description: "Synchronize UI wireframes with code. Handles spec-to-code and code-to-spec two-way binding. Use when user says 'sync ui', 'update wireframe', 'sync spec to code', 'sync code to spec', 'generate code from wireframe', or 'translate ui spec'."
---

# Sync UI Spec

> Uses [markdown-ui-dsl](https://github.com/MegaByteMark/markdown-ui-dsl) by MegaByteMark — MIT License.

## Prerequisites

Search the **ui** knowledge base for DSL syntax and sync conventions.

## Step 1: Determine Direction

Ask the user:

1. **Which direction?**
   - **Spec → Code**: Generate/update component code from a `.ui.md` file
   - **Code → Spec**: Update the `.ui.md` wireframe to match existing code

2. **Which file?** — path to the `.ui.md` or component file

## Step 2: Locate the Paired File

- **Spec → Code**: Read the `component:` key from the `.ui.md` frontmatter
- **Code → Spec**: Look for `// UI Spec: <path>` comment at the top of the code file

If the paired file doesn't exist, offer to create it.

## Step 3: Detect Drift

Compare the wireframe structure against the code structure:

- List components present in spec but missing from code (and vice versa)
- Identify layout differences

If drift is detected, present the differences and ask:
> "The spec and code are out of sync. Which is the source of truth?"

## Step 4: Synchronize

### Spec → Code

1. Parse the `.ui.md` using DSL rules from the **ui** KB
2. Map DSL elements to framework components:
   - ROW → horizontal flex/Row
   - COLUMN → vertical flex/Column
   - CARD → card component
   - Components → framework equivalents
3. Apply responsive directives as breakpoint-specific styles
4. Inject `// UI Spec: <path>` header in generated code
5. Apply theme/design system tokens if `theme:` frontmatter exists

### Code → Spec

1. Read the component structure
2. Reverse-map framework components to DSL syntax
3. Update the `.ui.md` preserving frontmatter
4. Preserve any `<!-- comments -->` from the original spec

## Step 5: Confirm Changes

Before writing, show the user what will change and ask for confirmation.

**Security rule:** Always ask before overwriting unless user explicitly said "force sync" or "autonomous".

## Step 6: Present Summary

```
✓ Synced: wireframes/<name>.ui.md ↔ src/components/<Name>.tsx

Changes applied:
  - [list changes made]

Files modified:
  - [list files]
```
