import os
import pytest

from app import create_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.adapters.orm import metadata, map_model_to_tables
from app.adapters import database_repository

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

TEST_DATABASE_URI_FILE = 'sqlite:///movies-test.db'

@pytest.fixture
def repo():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    repo = database_repository.SqlAlchemyRepository(session_factory)
    database_repository.populate(session_factory, TEST_DATA_PATH)
    yield repo
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(session_factory, TEST_DATA_PATH)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(session_factory, TEST_DATA_PATH)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def client():
    print('test client')
    app = create_app({
        'TESTING': 'True',
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'TEST_DATABASE_URI_FILE': TEST_DATABASE_URI_FILE,
        'WTF_CSRF_CHECK_DEFAULT': False,
        'WTF_CSRF_ENABLED': False
    })
    return app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def register(self, username='jack', password='123456'):
        return self._client.post(
            'auth/register',
            data={'username': username, 'password': password, 'confirm': password},
            follow_redirects=True
        )

    def login(self, username='jack', password='123456'):
        return self._client.post(
            'auth/login',
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/auth/logout',
            follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)