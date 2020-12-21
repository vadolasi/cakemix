"""Test the "add" command."""

from click.testing import CliRunner

from cakemix_python.cli import add


def test_add():
    """Test the "add" command."""
    runner = CliRunner()
    output = runner.invoke(add)
    assert output.exit_code == 0
