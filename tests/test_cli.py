"""Tests for logsight.cli."""

from __future__ import annotations

from click.testing import CliRunner

from logsight.cli import main


class TestHealthCommand:
    def test_health_exits_zero(self):
        runner = CliRunner()
        result = runner.invoke(main, ["health"])
        assert result.exit_code == 0

    def test_health_output_contains_healthy(self):
        runner = CliRunner()
        result = runner.invoke(main, ["health"])
        assert "healthy" in result.output.lower()

    def test_health_output_contains_version(self):
        runner = CliRunner()
        result = runner.invoke(main, ["health"])
        assert "version" in result.output.lower()
