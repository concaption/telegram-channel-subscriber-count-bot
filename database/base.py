"""
- This module is responsible for handling the database related works
"""
import logging
from contextlib import contextmanager
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from .client import DbClient


log = logging.getLogger(__name__)
Base = declarative_base()


class DbHelper:
    """
    DbHelper class to manage some initialization tasks
    """
    _sess: Union[sessionmaker[Session], None] = None
    _is_initialized: bool = False
    db_client = DbClient

    @classmethod
    def initialize(cls, db_path: str):
        """
        Initializes the database
        :param db_path: Path
        :return:
        """
        log.info("initializing database engine with path: %s", db_path)
        if cls._is_initialized:
            err_msg = "database is already initialized"
            log.warning(err_msg)
            raise ValueError(err_msg)

        engine = create_engine(
            url=db_path,
            echo=False,
        )
        log.info("initializing session maker")
        sess = sessionmaker(bind=engine)
        log.info("creating the database tables")
        Base.metadata.create_all(engine)
        cls._is_initialized = True
        cls._sess = sess

    @classmethod
    @contextmanager
    def session_manager(cls) -> Session:
        """
        Provide a session to perform works and close it afterward
        :yield: Session
        """
        if cls._sess is None:
            err_msg = "tried to create session before database is initialized"
            log.error(err_msg)
            raise ValueError(err_msg)

        session = cls._sess()
        try:
            log.info("yielding session")
            yield session

        except Exception as e:
            log.exception("error occurred while working with session %s", e)
            session.rollback()
            raise

        else:
            # committing the changes
            session.commit()

        finally:
            session.close()
