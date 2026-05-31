"""Rich terminal output with ANSI colors and emoji icons."""

import sys
from pathlib import Path

# ANSI color codes — disabled when not a TTY
_USE_COLOR = sys.stdout.isatty()

BOLD = "\033[1m" if _USE_COLOR else ""
DIM = "\033[2m" if _USE_COLOR else ""
RESET = "\033[0m" if _USE_COLOR else ""
GREEN = "\033[32m" if _USE_COLOR else ""
CYAN = "\033[36m" if _USE_COLOR else ""
YELLOW = "\033[33m" if _USE_COLOR else ""
BLUE = "\033[34m" if _USE_COLOR else ""
MAGENTA = "\033[35m" if _USE_COLOR else ""


def print_header(text: str, level: int = 1) -> None:
    if level == 1:
        print(f"\n{BOLD}{CYAN}{'═' * 60}{RESET}")
        print(f"{BOLD}{CYAN}  {text}{RESET}")
        print(f"{BOLD}{CYAN}{'═' * 60}{RESET}\n")
    else:
        print(f"\n{BOLD}{BLUE}  ▸ {text}{RESET}\n")


def print_file_content(label: str, path: Path | None, content: str | None = None) -> None:
    if content is None and path is not None:
        content = path.read_text()
    print(f"  {MAGENTA}📄 {label}{RESET}")
    print(f"  {DIM}{'─' * 50}{RESET}")
    for line in (content or "").splitlines():
        print(f"  {DIM}│{RESET} {line}")
    print(f"  {DIM}{'─' * 50}{RESET}\n")


def print_tree(target: Path, tree: dict[str, list[str]]) -> None:
    print(f"  {BOLD}{target}/{RESET}")
    dirs = sorted(tree.keys())
    for i, dir_path in enumerate(dirs):
        is_last_dir = i == len(dirs) - 1
        connector = "└── " if is_last_dir else "├── "
        print(f"  {YELLOW}{connector}📁 {dir_path}/{RESET}")
        files = tree[dir_path]
        for j, file_name in enumerate(files):
            is_last_file = j == len(files) - 1
            prefix = "    " if is_last_dir else "│   "
            file_connector = "└── " if is_last_file else "├── "
            print(f"  {prefix}{GREEN}{file_connector}{file_name}{RESET}")
    print()


def print_summary(skills_count: int, kbs_count: int, dry_run: bool) -> None:
    action = "Would install" if dry_run else "✅ Installed"
    parts = []
    if skills_count:
        parts.append(f"{skills_count} skill{'s' if skills_count != 1 else ''}")
    if kbs_count:
        parts.append(f"{kbs_count} knowledge base{'s' if kbs_count != 1 else ''}")
    print(f"  {BOLD}{GREEN}{action}: {', '.join(parts)}{RESET}\n")


def print_next_steps(steps: list[str]) -> None:
    print(f"  {BOLD}{YELLOW}⚠️  What's Next{RESET}\n")
    for step in steps:
        print(f"  {YELLOW}  ▸ {step}{RESET}")
    print(f"\n  {DIM}Edit the prompt to define your agent's persona, expertise, and response style.{RESET}\n")


def build_prompt(name: str, kbs: list, kb_instruction: str) -> str:
    """Build a shared agent prompt template."""
    kb_list = "\n".join(f"- **{kb.name}** — {kb.name} conventions and standards" for kb in kbs)
    return f"""# {name}

## Role

You are a senior developer specializing in [YOUR DOMAIN HERE].
You help the team write clean, tested, production-ready code following established conventions.

## Expertise

- [List your agent's areas of expertise]
- [e.g., Java/Spring Boot development]
- [e.g., REST API design]
- [e.g., Database migrations]

## Knowledge Bases

{kb_instruction}

{kb_list}

## Principles

1. **Convention over configuration** — follow the knowledge bases, don't reinvent
2. **Test-driven** — write tests before or alongside implementation
3. **Security by default** — validate inputs, use parameterized queries, handle errors
4. **Minimal and correct** — solve what was asked, don't over-engineer

## Response Style

- Be direct and concise
- Show complete, working code
- Explain trade-offs when relevant
- Use the project's existing patterns and libraries
"""
