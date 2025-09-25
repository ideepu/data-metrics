import contextlib
from typing import Iterator

from sqlalchemy import URL, Engine, create_engine, make_url
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from src.config import config


class DatabaseSessionManager:
    _URL: URL = make_url(config.DB_URL)

    def __init__(self) -> None:
        self.engine: Engine = create_engine(url=self._URL, echo=False)

    def close(self) -> None:
        self.engine.dispose()

    def get_session(self) -> Session:
        scoped_session_maker: scoped_session[Session] = scoped_session(sessionmaker(bind=self.engine))
        return scoped_session_maker()

    @contextlib.contextmanager
    def session(self) -> Iterator[Session]:
        session: Session = self.get_session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


db_session_manager = DatabaseSessionManager()
