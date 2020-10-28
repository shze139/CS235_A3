import os
from flask import Flask
from .adapters import repository as repo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from .adapters import database_repository
from .adapters.orm import metadata, map_model_to_tables

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    data_path = os.path.join(os.path.dirname(__file__), 'adapters', 'data')
    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    database_echo = app.config['SQLALCHEMY_ECHO']

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        database_uri = app.config['TEST_DATABASE_URI_FILE']


    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=database_echo)

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
        print("REPOPULATING DATABASE")
        # For testing, or first-time use of the web application, reinitialise the database.
        clear_mappers()
        metadata.create_all(database_engine)  # Conditionally create database tables.
        for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
            database_engine.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        database_repository.populate(session_factory, data_path)

    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()


    with app.app_context():
        from .home import home
        app.register_blueprint(home.bp)

        from .movie import movie
        app.register_blueprint(movie.bp)

        from .auth import auth
        app.register_blueprint(auth.bp)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app