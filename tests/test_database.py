"""Test the database."""

from sqlalchemy_utils import assert_non_nullable

from cakemix.database import Cakemix, Database


def test_database():
    """Test database."""
    with Database(in_memory=True) as database:
        cakemix = database.add(
            Cakemix,
            database,
            name='test',
            name_slug='test',
            structure='',
        )

        database.save()

        assert cakemix.name == 'test'


def test_database_fields():
    """Tests database fields."""
    with Database(in_memory=True) as database:
        cakemix = database.add(
            Cakemix,
            database,
            name='test',
            name_slug='test',
            structure='',
        )

        database.save()

        assert_non_nullable(cakemix, 'name')
        assert_non_nullable(cakemix, 'structure')
