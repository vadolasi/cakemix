"""Manage database."""

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
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


class PathTable(Base):
    """Table with the boilerplates paths."""

    __tablename__ = 'paths'

    path_id = Column(Integer, primary_key=True)
    boilerplate_name = Column(
        Integer, ForeignKey('boilerplates.name'), nullable=False,
    )
    path = Column(String, nullable=False)
    is_plain_text = Column(Boolean, nullable=False)

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

        engine = create_engine(f'sqlite:///{directory}database.sqlite')
        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        self._session = session()
