from games.adapters.repository import AbstractRepository


def get_genres(repository: AbstractRepository):
    """Get all genres"""
    return repository.get_genres()
