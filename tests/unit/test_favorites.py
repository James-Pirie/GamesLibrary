import pytest
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Favourite
from games.adapters.memory_repository import MemoryRepository
from games.adapters import repository as repo
from games.favourites import services


def test_get_all_favourites():
    """
    Test the 'get_all_favourites' function.

    - Create a memory repository instance.
    - Add two games, 'game_1' and 'game_2', and a user 'username' to the repository.
    - Add 'game_1' and 'game_2' to the user's favorites.
    - Call 'get_all_favourites' to retrieve the user's favorites.
    - Check if the returned list of favorites matches the expected list of games.

    Expected outcome: The 'get_all_favourites' function should return a list of games containing 'game_1' and 'game_2'.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    game_2 = Game(2, 'game_2')

    repo.repository_instance.add_game(game_2)
    repo.repository_instance.add_game(game_1)
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    services.add_game_to_users_favourites(repo.repository_instance, user, game_1)
    services.add_game_to_users_favourites(repo.repository_instance, user, game_2)

    favourites = services.get_all_favourites(repo.repository_instance, user)
    assert favourites == [Game(1, 'game_1'), Game(2, 'game_2')]

def test_add_game_to_users_favourites():
    """
    Test the 'add_game_to_users_favourites' function.

    - Create a memory repository instance.
    - Add two games, 'game_1' and 'game_2', and a user 'username' to the repository.
    - Add 'game_1' and 'game_2' to the user's favorites.
    - Call 'get_all_favourites' to retrieve the user's favorites.
    - Check if the returned list of favorites matches the expected list of games.
    - Add a new game, 'game_3', to the user's favorites.
    - Call 'get_all_favourites' again and check if it includes 'game_3'.

    Expected outcome: The 'add_game_to_users_favourites' function should add 'game_3' to the user's favorites,
    and 'get_all_favourites' should return a list of games containing 'game_1', 'game_2', and 'game_3'.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    game_2 = Game(2, 'game_2')

    repo.repository_instance.add_game(game_2)
    repo.repository_instance.add_game(game_1)
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    services.add_game_to_users_favourites(repo.repository_instance, user, game_1)
    services.add_game_to_users_favourites(repo.repository_instance, user, game_2)

    favourites = services.get_all_favourites(repo.repository_instance, user)
    assert favourites == [Game(1, 'game_1'), Game(2, 'game_2')]

    game_3 = Game(3, 'game_3')
    repo.repository_instance.add_game(game_3)
    services.add_game_to_users_favourites(repo.repository_instance, user, game_3)
    favourites = services.get_all_favourites(repo.repository_instance, user)
    assert favourites == [Game(1, 'game_1'), Game(2, 'game_2'), Game(3, 'game_3')]

def test_remove_game_from_users_favourites():
    """
    Test the 'remove_game_from_users_favourites' function.

    - Create a memory repository instance.
    - Add two games, 'game_1' and 'game_2', and a user 'username' to the repository.
    - Add 'game_1' and 'game_2' to the user's favorites.
    - Call 'get_all_favourites' to retrieve the user's favorites.
    - Check if the returned list of favorites matches the expected list of games.
    - Remove 'game_1' from the user's favorites using 'remove_game_from_users_favourites'.
    - Call 'get_all_favourites' again and check if it includes only 'game_2'.

    Expected outcome: The 'remove_game_from_users_favourites' function should remove 'game_1' from the user's favorites,
    and 'get_all_favourites' should return a list containing only 'game_2'.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    game_2 = Game(2, 'game_2')

    repo.repository_instance.add_game(game_2)
    repo.repository_instance.add_game(game_1)
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    services.add_game_to_users_favourites(repo.repository_instance, user, game_1)
    services.add_game_to_users_favourites(repo.repository_instance, user, game_2)

    favourites = services.get_all_favourites(repo.repository_instance, user)
    assert favourites == [Game(1, 'game_1'), Game(2, 'game_2')]
    services.remove_game_from_users_favourites(repo.repository_instance, user, game_1)
    favourites = services.get_all_favourites(repo.repository_instance, user)
    assert favourites == [Game(2, 'game_2')]
