# Markdown-UI DSL Reference

> Based on [markdown-ui-dsl](https://github.com/MegaByteMark/markdown-ui-dsl) by MegaByteMark — MIT License.

## Overview

Markdown-UI DSL is a domain-specific language for creating low-fidelity, text-based wireframes using extended Markdown syntax. Wireframes are stored as `.ui.md` files.

## File Convention

- Place wireframes in `wireframes/` or `docs/wireframes/` directory
- Name files descriptively: `login-form.ui.md`, `dashboard-overview.ui.md`
- One screen/view per file

## Layouts

| Syntax | Purpose |
|--------|---------|
| `\|\|\| COLUMN \|\|\|` | Vertical layout container |
| `=== ROW ===` | Horizontal layout container |
| `::: CARD :::` | Card/elevated surface |
| `::: MODAL :::` | Modal/dialog surface |
| `::: HEADER :::` | App bar / top navigation |
| `::: FOOTER :::` | Bottom nav / page footer |
| `::: BUBBLE USER :::` | Chat bubble (user) |
| `::: BUBBLE AGENT :::` | Chat bubble (agent) |
| `--- END ---` | End a layout block |
| `***` | Visual divider (horizontal rule) |

**Agent Directives:** Standard blockquotes (`> text`) act as natural language layout hints applied to the closest container or element (e.g., `> align right`, `> space between`).

## Components

| Syntax | Component |
|--------|-----------|
| `#`, `##`, `**text**` | Text/Headings |
| `[ Button Text ](action)` | Button — e.g., `[ Submit ](#submit)` |
| `\|[ Active Tab ]\| Tab 2 \| Tab 3 \|` | Tabs |
| `[ text: placeholder ]` | Text input — e.g., `[ text: Enter email... ]` |
| `[ ] Label` / `[x] Label` | Checkbox (unchecked/checked) |
| `( ) Label` / `(x) Label` | Radio button |
| `[on] Label` / `[off] Label` | Toggle/switch |
| `[v] Option` | Dropdown — e.g., `[v] Country {US, UK, DE}` |
| `(( Tag Name ))` | Badge/tag — e.g., `(( Admin ))` |
| `[ IMG: Description ]` | Image placeholder |
| Standard Markdown lists | Lists (bulleted/numbered) |
| Standard Markdown tables | Data tables |

## Frontmatter (Optional)

```yaml
---
framework: Next.js + TailwindCSS + Shadcn UI
theme: ./design-system.md
component: src/components/LoginForm.tsx
---
```

- `framework` — target tech stack for code generation
- `theme` — path to design system tokens document
- `component` — path to the linked source code file

## Responsive Directives

Blockquotes prefixed with `@` followed by a breakpoint token scope design tokens to that breakpoint:

```markdown
> @sm columns: 1, gap: 4
> @md columns: 2, gap: 6
> @lg columns: 3, gap: 8
```

Process mobile-first: `@sm` as base, larger breakpoints as overrides.

## Comments vs Hints

| Syntax | Purpose | AI Processing |
|--------|---------|---------------|
| `<!-- comment -->` | Human notes, TODOs | Ignored |
| `> hint text` | Layout/design guidance | Processed as instructions |
| `> @breakpoint ...` | Responsive directive | Processed as responsive rules |

## Spec-Code Synchronization

- `.ui.md` file is the **master** for spec-to-code sync
- Generated code files include a header comment: `// UI Spec: wireframes/login-form.ui.md`
- Code file is the **master** for code-to-spec sync
- On drift detection, ask user for source of truth before overwriting

## Example

```markdown
---
framework: React + TailwindCSS
component: src/components/LoginForm.tsx
---

::: CARD :::

## Login

[ text: Email address ]
[ text: Password ]

> align right
[ Log In ](#login)

***

Don't have an account? [ Sign Up ](#signup)

--- END ---
```
