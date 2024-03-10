from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Game, Review


def get_user_by_username(repository: AbstractRepository, username: str):
    """Get a user object by the username"""
    return repository.get_user(username)


def get_game_from_id(repository: AbstractRepository, id_string: str):
    """Get a game object from it's ID"""
    try:
        if id_string.isnumeric():
            return repository.get_game_by_id(int(id_string))
    except AttributeError:
        pass
    return None


def get_all_users_reviews(repository: AbstractRepository, user: User):
    """Get all user's reviews"""
    return repository.get_users_reviews(user)


def get_all_games_reviews(repository: AbstractRepository, game: Game):
    """Get all reviews of a game"""
    return repository.get_games_reviews(game)


def add_review_to_game(repository: AbstractRepository, game: Game, user: User, review: Review):
    """Add a review to a game"""
    repository.add_review(game, user, review)


def delete_review(repository: AbstractRepository, review: Review, user: User, game: Game):
    """Delete a review from a game"""
    repository.remove_review(game, user, review)


def get_all_games_user_reviewed(repository: AbstractRepository, user: User):
    """Get all games a user reviewed"""
    reviews = repository.get_users_reviews(user)
    return [review.game for review in reviews]
