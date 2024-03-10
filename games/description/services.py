from games.adapters.repository import AbstractRepository


def get_game_from_id(repository: AbstractRepository, id_string: str):
    """Get a game object from it's ID"""
    try:
        if id_string.isnumeric():
            return repository.get_game_by_id(int(id_string))
    except AttributeError:
        pass
    return None

