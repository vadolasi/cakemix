"""Test the "run" command."""

from click.testing import CliRunner

from cakemix_python.cli import run


def test_add():
    """Test the "run" command."""
    runner = CliRunner()
    output = runner.invoke(run)
    assert output.exit_code == 0
