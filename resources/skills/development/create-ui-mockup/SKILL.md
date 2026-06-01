---
name: "create-ui-mockup"
description: "Create low-fidelity wireframes using Markdown-UI DSL. Generates .ui.md files with text-based UI specs. Use when user says 'create mockup', 'create wireframe', 'design UI', 'create ui spec', 'add screen', or 'wireframe this'."
---

# Create UI Mockup

> Uses [markdown-ui-dsl](https://github.com/MegaByteMark/markdown-ui-dsl) by MegaByteMark — MIT License.

## Prerequisites

Search the **ui** knowledge base for the Markdown-UI DSL syntax reference.

## Step 1: Gather Context

Ask the user:

1. **What screen/view?** — e.g., login page, dashboard, settings panel, chat interface
2. **Target framework?** (optional) — e.g., React + Tailwind, Flutter, Next.js + Shadcn
3. **Component path?** (optional) — where the generated code will live
4. **Key elements?** — what must appear on the screen (forms, tables, navigation, etc.)

## Step 2: Generate the Wireframe

Using **only** the Markdown-UI DSL syntax from the **ui** knowledge base:

1. Add YAML frontmatter if framework/component was specified
2. Structure the layout using appropriate containers (ROW, COLUMN, CARD, HEADER, FOOTER)
3. Place components using strict DSL syntax
4. Add layout hints via blockquotes where alignment/spacing matters
5. Add responsive directives if the user mentioned breakpoints

**Rules:**
- Output ONLY Markdown-UI DSL — no HTML, no framework code
- Use `--- END ---` to close every layout block
- Use `***` for visual dividers (never `---`)
- One screen per file

## Step 3: Propose File Location

Suggest placement following conventions:
- `wireframes/<screen-name>.ui.md` (default)
- Or `docs/wireframes/<screen-name>.ui.md`

Ask user to confirm path.

## Step 4: Write the File

Save the `.ui.md` file to the confirmed path.

## Step 5: Present Summary

```
✓ Wireframe created: wireframes/<name>.ui.md

Components used:
  - [list key components]

Next steps:
  - Review and refine the wireframe
  - Run 'sync-ui-spec' to generate code from this spec
  - Add responsive directives for mobile/tablet breakpoints
```
