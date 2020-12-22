"""Manage database."""

import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class BoilerplateTable(Base):
    """Table with the information of the boilerplates."""

    __tablename__ = 'boilerplates'

    name = Column(String, primary_key=True)
    docopt_string = Column(String, nullable=False)
    questions = Column(String, nullable=False)
    structure = Column(String, nullable=False)

    paths = relationship('PathTable')


class PathContentType(enum.Enum):
    """PathTable.content_type choices."""

    plain_text = 1
    not_plain_text = 2
    directory = 3


class PathTable(Base):
    """Table with the boilerplates paths."""

    __tablename__ = 'paths'

    pk = Column(Integer, primary_key=True)
    boilerplate_name = Column(
        Integer, ForeignKey('boilerplates.name'), nullable=False,
    )
    path = Column(String, nullable=False)
    content_type = Column(Enum(PathContentType), default=1)

    boilerplate = relationship('BoilerplateTable')


class Database(object):
    """Provides high-level functions to manipulate the database."""

    def __init__(self, directory: str = ''):
        """Init the database.

        Args:
            directory (str, optional): The database directory. Defaults to ''.
        """
        if directory:
            directory = f'{directory}/'

        self._directory = f'sqlite:///{directory}database.sqlite'

    def __enter__(self):
        """Create a SQLAlchemy session."""  # noqa: DAR201
        engine = create_engine(self._directory)
        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        self._session = session()

        return self

    def __exit__(self, *args):
        """Close the SQLAlchemy session."""  # noqa: DAR101
        self._session.close()
