"""Initialize Flask app."""

from flask import Flask
from pathlib import Path
# import games.adapters.repository as repository
# from games.adapters.memory_repository import MemoryRepository
# from games.adapters.memory_repository import populate as local_populate


# sql imports
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


# local imports
import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.adapters.repository_populate import populate
from games.adapters.orm import metadata, map_model_to_tables


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)


    database_uri = 'sqlite:///games.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

    app.config.from_object('config.Config')

    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create a database engine and connect it to the specified database
    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=False)

    # Create the database session factory using session-maker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repository_instance = SqlAlchemyRepository(session_factory)

    if len(inspect(database_engine).get_table_names()) == 0:
        print("REPOPULATING DATABASE...")
        # For testing, or first-time use of the web application, reinitialise the database.
        clear_mappers()
        # Conditionally create database tables.
        metadata.create_all(database_engine)
        # Remove any data from the tables.
        for table in reversed(metadata.sorted_tables):
            with database_engine.connect() as conn:
                conn.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        populate(data_path, repo.repository_instance)
        print("REPOPULATING DATABASE... FINISHED")

    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

    # create the instance of the Memory Repository
    # repository.repository_instance = MemoryRepository()
    # load the games data from the csv file into the repository
    # local_populate(data_path, repository.repository_instance)

    with app.app_context():
        # Register the blueprints
        from .browse import browse
        from .description import description
        from .sidebar import sidebar
        from .authentication import authentication
        from .favourites import favourites
        from .homepage import homepage
        from .userprofile import userprofile
        from .reviews import reviews
        app.register_blueprint(browse.browse_blueprint)
        app.register_blueprint(description.description_blueprint)
        app.register_blueprint(sidebar.sidebar_blueprint)
        app.register_blueprint(authentication.authentication_blueprint)
        app.register_blueprint(favourites.favourites_blueprint)
        app.register_blueprint(homepage.home_bp)
        app.register_blueprint(userprofile.user_profile_blueprint)
        app.register_blueprint(reviews.reviews_blueprint)
    return app

