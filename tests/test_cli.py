"""Test the CLI."""

from click.testing import CliRunner

from cakemix.cli import cli


def test_add():
    """Test the "add" command."""
    runner = CliRunner()
    output = runner.invoke(cli, ['add', 'fake_projects/fake_project'])
    assert output.exit_code == 1


def test_list():
    """Test the "remove" command."""
    runner = CliRunner()
    output = runner.invoke(cli, ['list'])
    assert output.exit_code == 0


def test_add_with_empty_project():
    """Test the "add" command with empty project."""
    runner = CliRunner()
    output = runner.invoke(cli, ['add', 'fake_projects/empty_fake_project'])
    assert output.exit_code == 1


def test_remove():
    """Test the "remove" command."""
    runner = CliRunner()
    output = runner.invoke(cli, ['remove'])
    assert output.exit_code == 2


def test_run():
    """Test the "run" command."""
    runner = CliRunner()
    output = runner.invoke(cli, ['run'])
    assert output.exit_code == 0
