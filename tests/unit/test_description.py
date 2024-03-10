import pytest
from games.description import services
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game
from games.adapters import repository as repo


# Fixture that provides a testing repository instance for each test function
@pytest.fixture
def testing_repo():
    game_1 = Game(1, 'Game 1')
    game_2 = Game(2, 'Game 2')

    repo.repository_instance = MemoryRepository()

    repo.repository_instance.add_game(game_1)
    repo.repository_instance.add_game(game_2)
    return repo.repository_instance


def test_get_game_from_id_valid_id_string_numeric(testing_repo):
    """
    Test the get_game_from_id function from the services module with a valid numeric ID.

    This test function retrieves a game using a valid numeric ID string and compares
    the result with the expected game attributes.
    """
    repository = testing_repo
    game = services.get_game_from_id(repository, "2")
    assert game.game_id == 2
    assert game.title == "Game 2"


def test_get_game_from_id_valid_id_string_non_numeric(testing_repo):
    """
    Test the get_game_from_id function from the services module with a valid non-numeric ID.

    This test function attempts to retrieve a game using a valid non-numeric ID string and
    ensures that the result is None.
    """
    repository = testing_repo
    game = services.get_game_from_id(repository, "abc")
    assert game is None


def test_get_game_from_id_invalid_id_string(testing_repo):
    """
    Test the get_game_from_id function from the services module with an invalid ID.

    This test function attempts to retrieve a game using an invalid ID string (e.g., empty string)
    and ensures that the result is None.
    """
    repository = testing_repo
    game = services.get_game_from_id(repository, "")
    assert game is None
