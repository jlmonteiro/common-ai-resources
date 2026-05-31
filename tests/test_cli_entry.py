"""Tests for the Click CLI entry point."""

from click.testing import CliRunner

from common_ai.cli import main


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Common AI Resources" in result.output


def test_install_help():
    runner = CliRunner()
    result = runner.invoke(main, ["install", "--help"])
    assert result.exit_code == 0
    assert "--tool" in result.output
    assert "--name" in result.output
    assert "--target" in result.output
    assert "--dry-run" in result.output


def test_install_missing_required():
    runner = CliRunner()
    result = runner.invoke(main, ["install"])
    assert result.exit_code != 0
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_install_dry_run_kiro(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, [
        "install", "--tool", "kiro", "--name", "test",
        "--target", str(tmp_path / "out"),
        "--skills", "git/commit", "--knowledge-bases", "git",
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert "Dry Run" in result.output
    assert not (tmp_path / "out").exists()


def test_install_dry_run_claude(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, [
        "install", "--tool", "claude", "--name", "test",
        "--target", str(tmp_path / "out"),
        "--skills", "git/commit", "--knowledge-bases", "git",
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert "Claude Code" in result.output


def test_install_dry_run_gemini(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, [
        "install", "--tool", "gemini", "--name", "test",
        "--target", str(tmp_path / "out"),
        "--skills", "git/commit", "--knowledge-bases", "git",
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert "Gemini CLI" in result.output


def test_install_executes_kiro(tmp_path):
    runner = CliRunner()
    target = tmp_path / "out"
    result = runner.invoke(main, [
        "install", "--tool", "kiro", "--name", "myagent",
        "--target", str(target),
        "--skills", "git/commit", "--knowledge-bases", "git",
    ])
    assert result.exit_code == 0
    assert (target / "skills" / "git" / "commit" / "SKILL.md").exists()
    assert (target / "knowledge-bases" / "git" / "commit-messages.md").exists()
    assert (tmp_path / "myagent-agent.json").exists()
