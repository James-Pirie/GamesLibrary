import pytest
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import User, Game, Review, Genre
from games.userprofile.services import (
    get_reviews,
    get_favourites,
    get_user_by_username,
)


@pytest.fixture
def repo():
    """
    setup the repo with some temp games and users
    """
    repo = MemoryRepository()
    user1 = User("user1", "password1")
    user2 = User("user2", "password2")
    game1 = Game(1, "Game 1")
    game2 = Game(2, "Game 2")
    genre1 = Genre("Action")
    genre2 = Genre("Adventure")

    review1 = Review(user1, game1, 4, "this is a test review")

    repo.add_user(user1)
    repo.add_user(user2)
    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_genre(genre1)
    repo.add_genre(genre2)

    repo.add_review(game1, user1, review1)

    yield repo


def test_get_reviews(repo):
    """
    test that we get the reviews to show in the profile page
    """
    user1 = repo.get_user("user1")
    reviews = get_reviews(repo, user1)
    assert len(reviews) == 1


def test_get_favourites(repo):
    """
    test that we correctly get the favourites to show
    """
    user1 = repo.get_user("user1")
    favourites = get_favourites(repo, user1)
    assert len(favourites) == 0  # No favorites added yet


def test_get_user_by_username(repo):
    """
    test getting the correct user with the user name provided
    """
    user = get_user_by_username(repo, "user1")
    assert user.username == "user1"
