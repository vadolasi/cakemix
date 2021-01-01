"""Manage database."""

from pathlib import Path
from typing import Any, Callable

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query, relationship, sessionmaker
from sqlalchemy_utils.types.choice import ChoiceType

Base = declarative_base()


class CakemixTable(Base):
    """Table with the information of the boilerplates."""

    __tablename__ = 'cakemixes'

    name = Column(String, primary_key=True)
    description = Column(String)
    author = Column(String)
    structure = Column(String, nullable=False)

    parameters = relationship('ParameterTable', cascade='all, delete')  # noqa: WPS110
    paths = relationship('PathTable', cascade='all, delete')


class ParameterTable(Base):
    """Table with cakemix parameter."""

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

    __tablename__ = 'parameters'

    pk = Column(Integer, primary_key=True)
    cakemix_name = Column(
        Integer, ForeignKey('cakemixes.name'), nullable=False,
    )
    name = Column(String, nullable=False)
    help_message = Column(String)
    ask = Column(String)
    parameter_type = Column(
        ChoiceType(
            parameter_type_choices,
        ), default='argument',
    )
    input_type = Column(ChoiceType(input_type_choices), default='text')
    only = Column(ChoiceType(only_choices))
    default = Column(String)
    abbreviation = Column(String)
    required = Column(Boolean, default=False)

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

    def add_parameter(self, **kwargs):
        """[summary].

        Args:
            kwargs (dict): [description]
        """
        self.parameters.append(
            self._database.add(
                ParameterTable, **kwargs,
            ),
        )

    def add_path(self, **kwargs):
        """[summary].

        Args:
            kwargs (dict): [description]
        """
        self.paths.append(
            self._database.add(
                PathTable, **kwargs,
            ),
        )


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

    def query(self, line_object: Callable) -> Query:
        """[summary].

        Args:
            line_object (Callable): [description]

        Returns:
            Query: [description]
        """
        return self._session.query(line_object)

    def save(self):
        """Save data in database."""
        self._session.commit()
