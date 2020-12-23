"""Test the CLI."""

from click.testing import CliRunner

from cakemix_python import cli


def test_add():
    """Test the "add" command."""
    runner = CliRunner()
    output = runner.invoke(cli.add, ['./fake_projects/fake_project/', 'test'])
    assert output.exit_code == 1


def test_remove():
    """Test the "remove" command."""
    runner = CliRunner()
    output = runner.invoke(cli.remove)
    assert output.exit_code == 0


def test_run():
    """Test the "run" command."""
    runner = CliRunner()
    output = runner.invoke(cli.run)
    assert output.exit_code == 0
