from flask import Blueprint
import games.sidebar.services as services
import games.adapters.repository as repo

sidebar_blueprint = Blueprint("sidebar_bp", __name__)
genres = services.get_genres(repo.repository_instance)


@sidebar_blueprint.app_context_processor
def sidebar_data():
    """Gets all genres for the sidebar to display."""
    genre_data = services.get_genres(repo.repository_instance)
    return {'genre_data': genre_data}
