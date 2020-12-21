"""Test the "remove" command."""

from click.testing import CliRunner

from cakemix_python.cli import remove


def test_add():
    """Test the "remove" command."""
    runner = CliRunner()
    output = runner.invoke(remove)
    assert output.exit_code == 0
