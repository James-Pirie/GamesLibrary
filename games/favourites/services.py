from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Game


def get_all_favourites(repository: AbstractRepository, user: User):
    """Get a list of favourite games from a user"""
    return repository.get_users_favourites(user)


def get_user_by_username(repository: AbstractRepository, username: str):
    """Get a user object by the username"""
    return repository.get_user(username)


def add_game_to_users_favourites(repository: AbstractRepository, user: User, game: Game):
    """Add a game to a user's list of favourite's"""
    repository.add_game_to_favourite(user, game)


def remove_game_from_users_favourites(repository: AbstractRepository, user: User, game: Game):
    """Remove game from user's list of favourite's"""
    repository.remove_game_from_favourites(user, game)


def get_game_from_id(repository: AbstractRepository, id_string: str):
    """Get a game object from it's ID"""
    try:
        if id_string.isnumeric():
            return repository.get_game_by_id(int(id_string))
    except AttributeError:
        pass
    return None
