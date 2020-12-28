"""Test the database."""

from sqlalchemy_utils import assert_non_nullable

from cakemix.database import Database


def test_database():
    """Test database."""
    with Database(in_memory=True) as database:
        boilerplate = database.add(
            Cakemix,
            database,
            name='test',
            structure='',
        )

        database.save()

        assert boilerplate.name == 'test'


def test_database_fields():
    """Tests database fields."""
    with Database(in_memory=True) as database:
        boilerplate = database.add(
            Cakemix,
            database,
            name='test',
            structure='',
        )

        database.save()

        assert_non_nullable(boilerplate, 'name')
        assert_non_nullable(boilerplate, 'structure')
