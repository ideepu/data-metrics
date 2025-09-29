from typing import Iterator
from unittest.mock import patch

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from src.app import create_app
from src.base import BaseModel
from src.db import db_session_manager

DB_URL = 'sqlite:///:memory:'
engine = create_engine(url=make_url(DB_URL), echo=False)
scoped_session_maker: scoped_session[Session] = scoped_session(sessionmaker(bind=engine))


class BaseTest:
    assert_raises = staticmethod(pytest.raises)
    app: Flask
    client: FlaskClient

    @pytest.fixture
    def testing_app(self) -> Flask:
        application = create_app('testing_app')
        application.config.update({'TESTING': True})
        return application

    @pytest.fixture(autouse=True)
    def setup_application(self, testing_app: Flask) -> None:
        self.app = testing_app
        self.client = testing_app.test_client()

    @pytest.fixture
    def session(self, testing_app: Flask) -> Iterator[Session]:
        with testing_app.app_context():
            with scoped_session_maker() as session_obj:
                with patch.object(db_session_manager, 'session', return_value=session_obj):
                    BaseModel.metadata.create_all(engine)
                    yield session_obj
                    session_obj.close()
                    BaseModel.metadata.drop_all(engine)
