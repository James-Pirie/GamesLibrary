from flask import Blueprint
from flask import request, render_template, redirect
from games.domainmodel.model import Genre
import games.adapters.repository as repo
import games.browse.services as services


# Configure browse blueprint
browse_blueprint = Blueprint(
    "games_bp", __name__
)


@browse_blueprint.route('/browse')
def browse_games():
    """
    Render the template of the games browser page, which will contain 10 games per page
    """
    # get the page number
    page = request.args.get('page', 1, type=int)
    games_per_page = 10

    sort_option = request.args.get('sort', None, type=str)
    search_filter = request.args.get('search-filter', None, type=str)
    search_input = request.args.get('search-input', None, type=str)

    # all_games = services.get_games(repo.repository_instance)
    searched_games = services.search_games(repo.repository_instance, search_filter, search_input)
    num_games = services.get_number_of_games(searched_games)
    sorted_games = services.sort_games(searched_games)
    games_to_show = services.games_to_show(sorted_games)

    # check if no games match the criteria
    if num_games == 0:
        page = 0

    total_pages = (num_games + games_per_page - 1) // games_per_page


    return render_template(
        'browse.html',
        title='Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=games_to_show,
        num_games=num_games,
        current_page=page,
        total_pages=total_pages,
        current_sort_option=sort_option,
        current_search_filter=search_filter,
        current_search_input=search_input
    )


@browse_blueprint.route('/browse/<genre_name>')
def browse_games_by_genre(genre_name):
    """
    Render the template of the games browser page, which will contain 10 games per page
    """
    genre = Genre(genre_name)
    # get the page number
    page = request.args.get('page', 1, type=int)
    games_per_page = 10

    sort_option = request.args.get('sort', None, type=str)
    search_filter = request.args.get('search-filter', None, type=str)
    search_input = request.args.get('search-input', None, type=str)

    genre_games = services.get_games_by_genre(repo.repository_instance, genre)
    searched_games = services.search_games(repo.repository_instance, search_filter, search_input)

    search_genre_games = [game for game in genre_games if game in searched_games]

    num_games = services.get_number_of_games(search_genre_games)
    sorted_games = services.sort_games(search_genre_games)
    games_to_show = services.games_to_show(sorted_games)

    if num_games == 0:
        page = 0

    total_pages = (num_games + games_per_page - 1) // games_per_page

    return render_template(
        'browse.html',
        title='Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=games_to_show,
        num_games=num_games,
        current_page=page,
        total_pages=total_pages,
        current_sort_option=sort_option,
        current_search_filter=search_filter,
        current_search_input=search_input
    )


@browse_blueprint.app_context_processor
def get_genre_name():
    # Get the genre_name from the URL parameter
    genre_name = request.view_args.get('genre_name')
    return dict(genre_name=genre_name)

