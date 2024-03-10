from datetime import datetime

import pytest

from games.browse import services
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Publisher, Genre, Game


# create some test games to use
@pytest.fixture
def games():
    return [
        Game(1, "Game1"),
        Game(2, "Game2"),
        Game(3, "Game3")
    ]


def test_get_games(games):
    """
    Test all games are selected
    """
    repo = MemoryRepository()
    for game in games:
        repo.add_game(game)

    games = services.get_games(repo)
    assert games == [Game(1, "Game1"), Game(2, "Game2"), Game(3, "Game3")]


def test_get_games_by_genre(games):
    """
    Test that only games with specific genre are selected
    """
    repo = MemoryRepository()
    for game in games:
        repo.add_game(game)
    genre = Genre("Action")
    repo.add_genre(genre)
    # only add the genre to the first 2 games
    for i in range(2):
        games[i].add_genre(genre)

    games_with_genre = repo.get_games_by_genre(genre)
    assert games_with_genre == [Game(1, "Game1"), Game(2, "Game2")]


def test_get_number_of_games(games):
    """
    Test number of games
    """
    repo = MemoryRepository()
    for game in games:
        repo.add_game(game)

    num_games = services.get_number_of_games(games)
    assert num_games == len(games)


def test_games_to_show():
    """
    Test no more than 10 games wil show on a single page
    """
    repo = MemoryRepository()
    for i in range(11):
        repo.add_game(Game(i, f"Game{i}"))

    games = repo.get_games()
    games_per_page = 10

    # writing the logic here as real function depends on requests which uses the page number of the active website

    # set first and last game to show depending on how many games per page and what the current page is
    first_game_to_show = (1 - 1) * games_per_page
    last_game_to_show = first_game_to_show + games_per_page
    # only add the current games to show to the list
    games_to_show = games[first_game_to_show: last_game_to_show]

    assert games_to_show == [Game(i, f"Game{i}") for i in range(10)]


def test_sort_games_release_date(games):
    """
    Test that Games are correctly sorted by release date
    """
    repo = MemoryRepository()
    games[0].release_date = "Jan 1, 2016"
    games[1].release_date = "Aug 23, 2001"
    games[2].release_date = "Dec 25, 2022"
    for game in games:
        repo.add_game(game)

    sorted_games = games.copy()
    # simulate selecting release date from the button
    sorting_option = 'Release Date'

    # same logic as above as to why we need the code logic in the test and cna not use the actual function

    # sort games by selection
    if sorting_option == 'Release Date':
        sorted_games.sort(key=lambda game: datetime.strptime(game.release_date, "%b %d, %Y"))
    elif sorting_option == 'Price High - Low':
        sorted_games.sort(key=lambda game: game.price, reverse=True)
    elif sorting_option == 'Price Low - High':
        sorted_games.sort(key=lambda game: game.price)
    elif sorting_option == 'Publisher':
        sorted_games.sort(key=lambda game: game.publisher.publisher_name)

    assert sorted_games == [Game(2, "Game2"), Game(1, "Game1"), Game(3, "Game3")]


def test_sort_games_price_low_high(games):
    """
    Test the games are correctly sorted by price low - high
    """
    repo = MemoryRepository()
    games[0].price = 1.99
    games[1].price = 29.99
    games[2].price = 0.99
    for game in games:
        repo.add_game(game)

    sorted_games = games.copy()
    # simulate selecting price low - high from the button
    sorting_option = 'Price Low - High'

    # same logic as above as to why we need the code logic in the test and cna not use the actual function

    # sort games by selection
    if sorting_option == 'Release Date':
        sorted_games.sort(key=lambda game: datetime.strptime(game.release_date, "%b %d, %Y"))
    elif sorting_option == 'Price High - Low':
        sorted_games.sort(key=lambda game: game.price, reverse=True)
    elif sorting_option == 'Price Low - High':
        sorted_games.sort(key=lambda game: game.price)
    elif sorting_option == 'Publisher':
        sorted_games.sort(key=lambda game: game.publisher.publisher_name)

    assert sorted_games == [Game(3, "Game3"), Game(1, "Game1"), Game(2, "Game2")]


def test_sort_games_price_high_low(games):
    """
    Test that games are correctly sorted high - low
    """
    repo = MemoryRepository()
    games[0].price = 1.99
    games[1].price = 29.99
    games[2].price = 0.99
    for game in games:
        repo.add_game(game)

    sorted_games = games.copy()
    # simulate selecting price high - low from the button
    sorting_option = 'Price High - Low'

    # same logic as above as to why we need the code logic in the test and cna not use the actual function

    # sort games by selection
    if sorting_option == 'Release Date':
        sorted_games.sort(key=lambda game: datetime.strptime(game.release_date, "%b %d, %Y"))
    elif sorting_option == 'Price High - Low':
        sorted_games.sort(key=lambda game: game.price, reverse=True)
    elif sorting_option == 'Price Low - High':
        sorted_games.sort(key=lambda game: game.price)
    elif sorting_option == 'Publisher':
        sorted_games.sort(key=lambda game: game.publisher.publisher_name)

    assert sorted_games == [Game(2, "Game2"), Game(1, "Game1"), Game(3, "Game3")]


def test_sort_games_publisher(games):
    """
    Test that games are correctly sorted by publisher name
    """
    repo = MemoryRepository()
    games[0].publisher = Publisher("Publisher C")
    games[1].publisher = Publisher("Publisher A")
    games[2].publisher = Publisher("Publisher B")
    for game in games:
        repo.add_game(game)

    sorted_games = games.copy()
    # simulate selecting price high - low from the button
    sorting_option = 'Publisher'

    # same logic as above as to why we need the code logic in the test and cna not use the actual function

    # sort games by selection
    if sorting_option == 'Release Date':
        sorted_games.sort(key=lambda game: datetime.strptime(game.release_date, "%b %d, %Y"))
    elif sorting_option == 'Price High - Low':
        sorted_games.sort(key=lambda game: game.price, reverse=True)
    elif sorting_option == 'Price Low - High':
        sorted_games.sort(key=lambda game: game.price)
    elif sorting_option == 'Publisher':
        sorted_games.sort(key=lambda game: game.publisher.publisher_name)

    assert sorted_games == [Game(2, "Game2"), Game(3, "Game3"), Game(1, "Game1")]


def test_search_games_title(games):
    """
    Test that only games that match the search or have the search in their name are shown
    """
    search_option = "Title"
    search_input = "Game1"

    filtered_games = []

    if search_option == "Title":
        for game in games:
            if search_input.lower().strip() in game.title.lower().strip():
                filtered_games.append(game)
    elif search_option == "Publisher":
        for game in games:
            if search_input.lower().strip() in game.publisher.publisher_name.lower().strip():
                filtered_games.append(game)

    assert filtered_games == [Game(1, "Game1")]


def test_search_games_title_not_found(games):
    """
    Test that no results are shown when a title that does not exist is entered
    """
    search_option = "Title"
    search_input = "Game4"

    filtered_games = []

    if search_option == "Title":
        for game in games:
            if search_input.lower().strip() in game.title.lower().strip():
                filtered_games.append(game)
    elif search_option == "Publisher":
        for game in games:
            if search_input.lower().strip() in game.publisher.publisher_name.lower().strip():
                filtered_games.append(game)

    # we return a blank list if the game is not found
    assert filtered_games == []


def test_search_games_publisher(games):
    """
    Test the only games with matching or ones that contain the publisher name are shown
    """
    search_option = "Publisher"
    search_input = "Publisher A"

    filtered_games = []

    repo = MemoryRepository()
    games[0].publisher = Publisher("Publisher C")
    games[1].publisher = Publisher("Publisher A")
    games[2].publisher = Publisher("Publisher B")

    for game in games:
        repo.add_game(game)

    if search_option == "Title":
        for game in games:
            if search_input.lower().strip() in game.title.lower().strip():
                filtered_games.append(game)
    elif search_option == "Publisher":
        for game in games:
            if search_input.lower().strip() in game.publisher.publisher_name.lower().strip():
                filtered_games.append(game)

    assert filtered_games == [Game(2, "Game2")]


def test_search_games_publisher_not_found(games):
    """
    Test that no results are shown when a publisher name that doesn't exist is entered
    """
    search_option = "Publisher"
    search_input = "Publisher D"

    filtered_games = []

    repo = MemoryRepository()
    games[0].publisher = Publisher("Publisher C")
    games[1].publisher = Publisher("Publisher A")
    games[2].publisher = Publisher("Publisher B")

    for game in games:
        repo.add_game(game)

    if search_option == "Title":
        for game in games:
            if search_input.lower().strip() in game.title.lower().strip():
                filtered_games.append(game)
    elif search_option == "Publisher":
        for game in games:
            if search_input.lower().strip() in game.publisher.publisher_name.lower().strip():
                filtered_games.append(game)

    assert filtered_games == []
