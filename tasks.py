from invoke import task

IMAGE_NAME = "ghcr.io/jlmonteiro/common-knowledge-base-mcp"
IMAGE_TAG = "latest"


@task
def build(c):
    """Build the MCP knowledge base Docker image."""
    c.run(f"docker build -f knowledge-base-mcp.dockerfile -t {IMAGE_NAME}:{IMAGE_TAG} .")


@task
def run(c):
    """Run the MCP server (STDIO)."""
    c.run(f"docker run -i {IMAGE_NAME}:{IMAGE_TAG}")


@task
def run_dev(c):
    """Run MCP server with live-mounted knowledge bases."""
    c.run(f"docker run -i -v ./resources/knowledge-bases:/data {IMAGE_NAME}:{IMAGE_TAG}")


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
    """Run tests."""
    c.run("pytest")
