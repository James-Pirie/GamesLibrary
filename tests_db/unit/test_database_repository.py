from datetime import date, datetime
import pytest
import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Game, Review, Favourite, Publisher, Genre
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    """
    Test that the repository can add a user and retrieve their information correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    test_repo.add_user(User('dave', '12345e6789'))
    test_repo.add_user(User('martin', '12345e6789'))

    user = test_repo.get_user('dave')

    assert user.username == 'dave' and user.password == '12345e6789'


def test_repository_can_retrieve_a_user(session_factory):
    """
    Test that the repository can retrieve a user's information correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    test_repo.add_user(User('fmercury', '8734gfe2058v'))

    user = test_repo.get_user('fmercury')

    assert user.username == 'fmercury' and user.password == '8734gfe2058v'


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    """
    Test that the repository returns None for a non-existent user.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    user = test_repo.get_user('prince')
    assert user is None


def test_get_games(session_factory):
    """
    Test that the repository can add and retrieve a game correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)
    game = Game(1234, 'game')
    game.title = 'game'
    game.price = 12
    game.release_date = 'Oct 21, 2008'
    game.description = 'game'
    game.image_url = 'www.com'
    game.website_url = 'www.co.nz'
    game.publisher = Publisher('publisher')

    test_repo.add_game(game)

    selected_game = test_repo.get_game(1234)
    assert selected_game == game


def test_add_multiple_games(session_factory):
    """
    Test that the repository can add and retrieve multiple games correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    game = Game(1234, 'game')
    game.title = 'game'
    game.price = 12
    game.release_date = 'Oct 21, 2008'
    game.description = 'game'
    game.image_url = 'www.com'
    game.website_url = 'www.co.nz'
    game.publisher = Publisher('publisher')

    game2 = Game(12345, 'game2')
    game2.title = 'game2'
    game2.price = 12
    game2.release_date = 'Oct 21, 2008'
    game2.description = 'game2'
    game2.image_url = 'www.com'
    game2.website_url = 'www.co.nz'
    game2.publisher = Publisher('publisher2')

    test_repo.add_multiple_games([game, game2])

    selected_game = test_repo.get_game(1234)
    selected_game2 = test_repo.get_game(12345)
    assert selected_game == game and selected_game2 == game2


def test_get_reviews(session_factory):
    """
    Test that the repository can add and retrieve reviews for a game and user correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    game2 = Game(12345, 'game2')
    game2.title = 'game2'
    game2.price = 12
    game2.release_date = 'Oct 21, 2008'
    game2.description = 'game2'
    game2.image_url = 'www.com'
    game2.website_url = 'www.co.nz'
    game2.publisher = Publisher('publisher2')

    test_repo.add_game(game2)

    user = User('john', 'password')
    test_repo.add_user(user)

    review = Review(user, game2, 4, 'comment')
    test_repo.add_review(game2, user, review)

    assert test_repo.get_users_reviews(user) == [review]
    assert test_repo.get_games_reviews(game2) == [review]


def test_get_game_by_id(session_factory):
    """
    Test that the repository can retrieve a game by its ID correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    game2 = Game(12345, 'game2')
    game2.title = 'game2'
    game2.price = 12
    game2.release_date = 'Oct 21, 2008'
    game2.description = 'game2'
    game2.image_url = 'www.com'
    game2.website_url = 'www.co.nz'
    game2.publisher = Publisher('publisher2')

    test_repo.add_game(game2)
    assert test_repo.get_game_by_id(12345) == game2


def test_add_to_favourite(session_factory):
    """
    Test that the repository can add a game to favourites, by username and game_id.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    game2 = Game(12345, 'game2')
    game2.title = 'game2'
    game2.price = 12
    game2.release_date = 'Oct 21, 2008'
    game2.description = 'game2'
    game2.image_url = 'www.com'
    game2.website_url = 'www.co.nz'
    game2.publisher = Publisher('publisher2')

    test_repo.add_game(game2)

    user = User('dave', '12345e6789')
    test_repo.add_user(user)

    test_repo.add_game_to_favourite(user, game2)
    user_favourites = test_repo.get_users_favourites(user)
    assert user_favourites == [game2]


def test_remove_from_favourite(session_factory):
    """
    Test that the repository can add and remove a game to favourites, by username and game_id.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    game2 = Game(12345, 'game2')
    game2.title = 'game2'
    game2.price = 12
    game2.release_date = 'Oct 21, 2008'
    game2.description = 'game2'
    game2.image_url = 'www.com'
    game2.website_url = 'www.co.nz'
    game2.publisher = Publisher('publisher2')

    test_repo.add_game(game2)

    user = User('dave', '12345e6789')
    test_repo.add_user(user)

    test_repo.add_game_to_favourite(user, game2)
    user_favourites = test_repo.get_users_favourites(user)

    assert user_favourites == [game2]

    test_repo.remove_game_from_favourites(user, game2)
    user_favourites = test_repo.get_users_favourites(user)
    assert user_favourites == []


def test_delete_reviews(session_factory):
    """
    Test that the repository can delete reviews for a game and user correctly.
    """
    test_repo = SqlAlchemyRepository(session_factory)

    game2 = Game(12345, 'game2')
    game2.title = 'game2'
    game2.price = 12
    game2.release_date = 'Oct 21, 2008'
    game2.description = 'game2'
    game2.image_url = 'www.com'
    game2.website_url = 'www.co.nz'
    game2.publisher = Publisher('publisher2')

    test_repo.add_game(game2)

    user = User('john', 'password')
    test_repo.add_user(user)

    review = Review(user, game2, 4, 'comment')
    test_repo.add_review(game2, user, review)

    assert test_repo.get_users_reviews(user) == [review]
    assert test_repo.get_games_reviews(game2) == [review]

    test_repo.remove_review(game2, user, review)

    assert test_repo.get_users_reviews(user) == []
    assert test_repo.get_games_reviews(game2) == []




