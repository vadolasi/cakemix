"""Test the database."""

from cakemix_python.database import Database


def test_database():
    """Test database."""
    with Database() as database:
        assert database._directory == 'sqlite:///database.sqlite'
