import pytest
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Genre, Game
from games.adapters import repository as repo


# Fixture that provides a testing repository instance for each test function
@pytest.fixture()
def testing_repo():
    repo.repository_instance = MemoryRepository()
    return repo.repository_instance


def test_add_game(testing_repo):
    """
    Test the add_game method of the repository.

    This test function creates two games, adds them to the repository,
    and then checks if they are retrievable using the get_games method.
    """
    repository = testing_repo

    new_game_1 = Game(1, 'game_1')
    repository.add_game(new_game_1)
    assert repository.get_games() == [new_game_1]

    new_game_2 = Game(2, 'game_2')
    repository.add_game(new_game_2)
    assert repository.get_games() == [new_game_1, new_game_2]
    assert repository.get_games()[0].title == 'game_1'


def test_get_game_by_id(testing_repo):
    """
    Test the get_game_by_id method of the repository.

    This test function adds three games to the repository and then retrieves
    one of the games by its ID to check if the retrieved game matches the expected game.
    """
    repository = testing_repo
    new_game_1 = Game(1, 'game_1')
    new_game_2 = Game(2, 'game_2')
    new_game_3 = Game(3, 'game_3')

    repository.add_game(new_game_1)
    repository.add_game(new_game_2)
    repository.add_game(new_game_3)
    selected_game = repository.get_game_by_id(2)
    assert selected_game == new_game_2
    assert selected_game.game_id == 2
    assert selected_game.title == 'game_2'


def test_get_games(testing_repo):
    """
    Test the get_games method of the repository.

    This test function adds three games to the repository and then retrieves
    all the games to check if the retrieved games match the expected games.
    """
    repository = testing_repo
    new_game_1 = Game(1, 'game_1')
    new_game_2 = Game(2, 'game_2')
    new_game_3 = Game(3, 'game_3')

    repository.add_game(new_game_1)
    repository.add_game(new_game_2)
    repository.add_game(new_game_3)
    selected_games = repository.get_games()
    assert selected_games == [new_game_1, new_game_2, new_game_3]


def test_add_genre(testing_repo):
    """
    Test the add_genre method of the repository.

    This test function adds three genres to the repository and then checks
    if they are retrievable using the get_genres method.
    """
    repository = testing_repo
    genre_1 = Genre('genre_1')
    genre_2 = Genre('genre_2')
    genre_3 = Genre('genre_3')

    repository.add_genre(genre_1)
    assert repository.get_genres() == [genre_1]

    repository.add_genre(genre_2)
    assert repository.get_genres() == [genre_1, genre_2]

    repository.add_genre(genre_3)
    assert repository.get_genres() == [genre_1, genre_2, genre_3]


def test_get_genre(testing_repo):
    """
    Test the get_genres method of the repository.

    This test function adds three genres to the repository and then retrieves
    all the genres to check if the retrieved genres match the expected genres.
    """
    repository = testing_repo
    genre_1 = Genre('genre_1')
    genre_2 = Genre('genre_2')
    genre_3 = Genre('genre_3')
    repository.add_genre(genre_1)
    repository.add_genre(genre_3)
    repository.add_genre(genre_2)
    assert repository.get_genres() == [genre_1, genre_2, genre_3]


def test_get_games_by_genre(testing_repo):
    """
    Test the get_games_by_genre method of the repository.

    This test function adds three genres and three games with corresponding genres
    to the repository. It then retrieves games by each genre and checks if the
    retrieved games match the expected games for each genre.
    """
    repository = testing_repo
    genre_1 = Genre('genre_1')
    genre_2 = Genre('genre_2')
    genre_3 = Genre('genre_3')

    new_game_1 = Game(1, 'game_1')
    new_game_2 = Game(2, 'game_2')
    new_game_3 = Game(3, 'game_3')

    new_game_1.add_genre(genre_1)
    new_game_2.add_genre(genre_1)
    new_game_3.add_genre(genre_1)

    new_game_2.add_genre(genre_2)
    new_game_3.add_genre(genre_2)

    new_game_3.add_genre(genre_3)

    repository.add_game(new_game_1)
    repository.add_game(new_game_2)
    repository.add_game(new_game_3)

    assert repository.get_games_by_genre(genre_1) == [new_game_1, new_game_2, new_game_3]
    assert repository.get_games_by_genre(genre_2) == [new_game_2, new_game_3]
    assert repository.get_games_by_genre(genre_3) == [new_game_3]
