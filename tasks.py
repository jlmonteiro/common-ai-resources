import re
from pathlib import Path

from invoke import task

IMAGE_NAME = "ghcr.io/jlmonteiro/common-knowledge-base-mcp"


def _get_version():
    text = Path("pyproject.toml").read_text()
    match = re.search(r'^version\s*=\s*"(.+?)"', text, re.MULTILINE)
    return match.group(1) if match else "latest"


@task
def build(c):
    """Build the MCP knowledge base Docker image."""
    version = _get_version()
    c.run(f"docker build -f knowledge-base-mcp.dockerfile -t {IMAGE_NAME}:{version} -t {IMAGE_NAME}:latest .")


@task
def run(c):
    """Run the MCP server (STDIO)."""
    c.run(f"docker run -i {IMAGE_NAME}:latest")


@task
def run_dev(c):
    """Run MCP server with live-mounted knowledge bases."""
    c.run(f"docker run -i -v ./resources/knowledge-bases:/data {IMAGE_NAME}:latest")


@task
def docs(c):
    """Serve MkDocs documentation locally."""
    c.run("mkdocs serve")


@task
def lint(c):
    """Run ruff linter."""
    c.run("ruff check src/")


@task
def test(c):
    """Run tests with coverage and HTML reports."""
    c.run("pytest --junitxml=reports/test-results.xml --html=reports/test-report.html --self-contained-html --cov=common_ai --cov-report=html:reports/coverage --cov-report=term-missing")


@task
def version(c):
    """Show current project version."""
    print(_get_version())


@task
def release(c, part="patch"):
    """Bump version, commit, and tag. Usage: inv release --part=minor"""
    current = _get_version()
    major, minor, patch = [int(x) for x in current.split(".")]

    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        major, minor, patch = major, minor + 1, 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()
    content = content.replace(f'version = "{current}"', f'version = "{new_version}"')
    pyproject.write_text(content)

    c.run('git add pyproject.toml')
    c.run(f'git commit -m "release: v{new_version}"')
    c.run(f'git tag v{new_version}')
    print(f"Released v{new_version}")
