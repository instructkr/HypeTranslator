from contextlib import contextmanager, AbstractContextManager

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class Database:
    def __init__(self, connection_url: str):
        self._engine = create_engine(connection_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self):
        session: AbstractContextManager[Session] = self._session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)
