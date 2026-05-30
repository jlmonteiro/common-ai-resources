from unittest.mock import patch

import pytest


@pytest.fixture
def tmp_kb(tmp_path):
    """Create a temporary knowledge base directory."""
    return tmp_path


@pytest.fixture
def reset_mcp_state():
    """Reset MCP server global state between tests."""
    import common_ai.mcp_server as server
    server._chunks = []
    server._embeddings = None
    server._model = None
    yield
    server._chunks = []
    server._embeddings = None
    server._model = None


@pytest.fixture
def kb_with_docs(tmp_path, reset_mcp_state):
    """Create a KB with sample documents in multiple scopes."""
    import common_ai.mcp_server as server

    # Docker docs
    docker_dir = tmp_path / "docker"
    docker_dir.mkdir()
    (docker_dir / "conventions.md").write_text(
        "# Docker Conventions\n\n"
        "## Dockerfile Best Practices\n\n"
        "Always use multi-stage builds for production images.\n\n"
        "## Image Tagging\n\n"
        "Use semantic versioning for image tags.\n"
    )

    # Java docs
    java_dir = tmp_path / "java"
    java_dir.mkdir()
    (java_dir / "coding.md").write_text(
        "# Java Coding Standards\n\n"
        "## Architecture\n\n"
        "Follow layered architecture: Controller, Service, Repository.\n\n"
        "## Conventions\n\n"
        "Use records for DTOs. Use constructor injection.\n"
    )

    # Git docs
    git_dir = tmp_path / "git"
    git_dir.mkdir()
    (git_dir / "commits.md").write_text(
        "# Commit Conventions\n\n"
        "## Format\n\n"
        "Use conventional commits format.\n\n"
        "## Rules\n\n"
        "Subject line max 72 chars, imperative mood.\n"
    )

    with patch.object(server, "KB_PATH", tmp_path):
        yield tmp_path


@pytest.fixture
def empty_kb(tmp_path, reset_mcp_state):
    """Create an empty KB directory."""
    import common_ai.mcp_server as server
    with patch.object(server, "KB_PATH", tmp_path):
        yield tmp_path
