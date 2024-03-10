from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre, Game
from flask import request
from datetime import datetime


def get_games(repo: AbstractRepository):
    """
    Get all games from the repository
    """

    all_games = repo.get_games()
    return all_games


def get_games_by_genre(repo: AbstractRepository, genre: Genre):
    """
    Get all games of a certain genre from the repository
    """
    all_games = repo.get_games_by_genre(genre)
    return all_games


def get_number_of_games(games):
    return len(games)


def games_to_show(games):

    page = request.args.get('page', 1, type=int)
    games_per_page = 10
    # set first and last game to show depending on how many games per page and what the current page is
    first_game_to_show = (page - 1) * games_per_page
    last_game_to_show = first_game_to_show + games_per_page
    # only add the current games to show to the list
    games_to_show = games[first_game_to_show: last_game_to_show]

    return games_to_show


def sort_games(games):

    sorting_option = request.args.get('sort', None, type=str)

    sorted_games = games.copy()

    # sort games by selection
    if sorting_option == 'Release Date':
        sorted_games.sort(key=lambda game: datetime.strptime(game.release_date, "%b %d, %Y"))
    elif sorting_option == 'Price High - Low':
        sorted_games.sort(key=lambda game: game.price, reverse=True)
    elif sorting_option == 'Price Low - High':
        sorted_games.sort(key=lambda game: game.price)
    elif sorting_option == 'Publisher':
        sorted_games.sort(key=lambda game: game.publisher.publisher_name)

    return sorted_games


def search_games(repo: AbstractRepository, search_option, search_input):
    """
    Filter games to show by the search
    """

    # search_option = request.args.get('search-filter', None, type=str)
    # search_input = request.args.get('search-input', None, type=str)
    #
    # filtered_games = []
    #
    # if search_option == "Title":
    #     for game in games:
    #         if search_input.lower().strip() in game.title.lower().strip():
    #             filtered_games.append(game)
    # elif search_option == "Publisher":
    #     for game in games:
    #         if search_input.lower().strip() in game.publisher.publisher_name.lower().strip():
    #             filtered_games.append(game)
    # else:
    #     # if the option is neither title or publisher, then it will be none and so return games without searching
    #     return games

    games = repo.search_games(search_option, search_input)

    return games

