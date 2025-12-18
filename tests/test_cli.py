"""
Tests for CLI scripts.
"""

import re
import pytest
from typer.testing import CliRunner
from messenger_utils.cli import app



@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.skip(reason="Control chars for color ruins the test")
def test_cli_version(runner):
    """
    Check if output version is in format "x.y.z"
    """
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert re.match(r"^\d+\.\d+\.\d+$", result.output)


def test_cli_remove_command(runner):
    """
    Check if remove command raises ValueError if command not found
    """
    result = runner.invoke(app, ["remove-command", "--name", "notexistingcommand"])
    assert "not found" in result.output
