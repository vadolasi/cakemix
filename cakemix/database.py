"""Manage database."""

from pathlib import Path
from typing import Any, Callable

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils.types.choice import ChoiceType

Base = declarative_base()


class CakemixTable(Base):
    """Table with the information of the boilerplates."""

    __tablename__ = 'cakemixes'

    name = Column(String, primary_key=True)
    structure = Column(String, nullable=False)

    arguments = relationship('ArgumentTable')
    paths = relationship('PathTable')


class Cakemix(CakemixTable):
    """Provides high-level functions to manipulate the cakemixes."""

    def __init__(self, database: 'Database', **args):
        """Create a BoilerplateTable object.

        Args:
            database (Database): [description]
            args (tuple): [description]
        """
        super().__init__(**args)
        self._database = database

    def add_argument(self, **kwargs):
        """[summary].

        Args:
            kwargs (dict): [description]
        """
        self.arguments.append(
            self._database.add(
                self._database.argument_object, **kwargs,
            ),
        )

    def add_path(self, **kwargs):
        """[summary].

        Args:
            kwargs (dict): [description]
        """
        self.paths.append(
            self._database.add(
                self._database.path_object, **kwargs,
            ),
        )


class ArgumentTable(Base):
    """Table with boilerplate arguments."""

    parameter_type_choices = [
        ('argument', 'Argument'),
        ('option', 'Option'),
    ]

    input_type_choices = [
        ('text', 'Text'),
    ]

    only_choices = [
        ('argument', 'Argument'),
        ('question', 'Question'),
    ]

    __tablename__ = 'arguments'

    pk = Column(Integer, primary_key=True)
    cakemix_name = Column(
        Integer, ForeignKey('cakemixes.name'), nullable=False,
    )
    name = Column(String, nullable=False)
    parameter_type = Column(
        ChoiceType(
            parameter_type_choices,
        ), default='argument',
    )
    input_type = Column(ChoiceType(input_type_choices), default='text')
    only = Column(ChoiceType(only_choices))

    cakemix = relationship('Cakemix')


class PathTable(Base):
    """Table with the boilerplates paths."""

    content_type_choices = [
        ('plain_text', 'Plain text'),
        ('not_plain_text', 'Not plain text'),
        ('directory', 'Directory'),
    ]

    __tablename__ = 'paths'

    pk = Column(Integer, primary_key=True)
    cakemix_name = Column(
        Integer, ForeignKey('cakemixes.name'), nullable=False,
    )
    path = Column(String, nullable=False)
    content_type = Column(
        ChoiceType(
            content_type_choices,
        ), default='plain_text',
    )

    cakemix = relationship('Cakemix')


class Database(object):
    """Provides high-level functions to manipulate the database."""

    def __init__(self, in_memory: bool = False):
        """Define the database path.

        Args:
            in_memory (bool, optional): The database path. Defaults to False.
        """
        self.in_memory = in_memory

    def __enter__(self) -> 'Database':
        """Create a SQLAlchemy session.

        Returns:
            Database: [description]
        """
        if self.in_memory:
            database_url = 'sqlite://'
        else:
            database_path = Path.home() / '.cakemix' / 'database.sqlite'
            database_url = f'sqlite:///{database_path}'

        engine = create_engine(database_url, pool_pre_ping=True)

        Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

        self.cakemix_object = Cakemix
        self.argument_object = ArgumentTable
        self.path_object = PathTable

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Close the SQLAlchemy session.

        Args:
            exception_type ([type]): [description]
            exception_value ([type]): [description]
            traceback ([type]): [description]
        """
        self._session.close()

    def add(self, line_object: Callable, *args, **kwargs) -> Any:
        """[summary].

        Args:
            line_object (Callable): [description]
            args (tuple): [description]
            kwargs (dict): [description]

        Returns:
            Any: [description]
        """
        new_object = line_object(*args, **kwargs)
        self._session.add(new_object)

        return new_object

    def save(self):
        """Save data in database."""
        self._session.commit()
