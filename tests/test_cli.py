"""
Tests for CLI scripts.
"""

import pytest
import re
from typer.testing import CliRunner
from messenger_utils.cli import app



@pytest.fixture
def runner():
    return CliRunner()


def test_cli_version(runner):
    """
    Check if output version is in format "x.y.z"
    """
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert re.match(r"^\d+\.\d+\.\d+$", result.output)
