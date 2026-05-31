"""Rich terminal output with ANSI colors and emoji icons."""

from pathlib import Path

# ANSI color codes
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"


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


def print_next_steps(name: str, steps: list[str]) -> None:
    print(f"  {BOLD}{YELLOW}⚠️  What's Next{RESET}\n")
    for step in steps:
        print(f"  {YELLOW}  ▸ {step}{RESET}")
    print(f"\n  {DIM}Edit the prompt to define your agent's persona, expertise, and response style.{RESET}\n")
