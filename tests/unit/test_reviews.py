import pytest
from games.domainmodel.model import Publisher, Genre, Game, Review, User
from games.sidebar import services
from games.adapters.memory_repository import MemoryRepository
from games.adapters import repository as repo
from games.reviews import services

from games.domainmodel.model import User, Game, Review


@pytest.fixture()
def testing_repo():
    """
    Fixture for creating a testing repository with sample data.

    - Create a MemoryRepository instance.
    - Add two games, 'game_1' and 'game_2', and a user 'username' to the repository.
    - Add reviews for 'game_1' and 'game_2' by the user.
    - Return the repository instance for testing.

    Returns:
        MemoryRepository: The testing repository instance.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    game_2 = Game(2, 'game_2')
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    repo.repository_instance.add_game(game_1)
    repo.repository_instance.add_game(game_2)
    review_1 = Review(user, game_1, 4, 'comment')
    review_2 = Review(user, game_2, 4, 'comment')
    repo.repository_instance.add_review(game_1, user, review_1)
    repo.repository_instance.add_review(game_2, user, review_2)
    return repo.repository_instance


def test_get_all_users_reviews(testing_repo):
    """
    Test the 'get_all_users_reviews' function.

    - Retrieve the user 'username' from the testing repository.
    - Check if the returned list of user's reviews matches the expected list of reviews for 'game_1' and 'game_2'.

    Expected outcome: The 'get_all_users_reviews' function should return a list of reviews for 'game_1' and 'game_2'.
    """
    repository = testing_repo
    user = services.get_user_by_username(repository, 'username')
    game_1 = Game(1, 'game_1')
    game_2 = Game(2, 'game_2')
    assert services.get_all_users_reviews(repository, user) == [Review(user, game_1, 4, 'comment'), Review(user, game_2, 4, 'comment')]


def test_get_all_games_reviews(testing_repo):
    """
    Test the 'get_all_games_reviews' function.

    - Create a new MemoryRepository instance.
    - Add 'game_1' to the repository.
    - Add a review for 'game_1' by the user.
    - Check if the returned list of reviews for 'game_1' matches the expected list containing that review.

    Expected outcome: The 'get_all_games_reviews' function should return a list containing the review for 'game_1'.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    user = User('username', 'password')
    review_1 = Review(user, game_1, 4, 'comment')
    services.add_review_to_game(repo.repository_instance, game_1, user, review_1)
    assert services.get_all_games_reviews(repo.repository_instance, game_1) == [Review(user, game_1, 4, 'comment')]


def test_add_review_to_game():
    """
    Test the 'add_review_to_game' function.

    - Create a new MemoryRepository instance.
    - Add 'game_1' to the repository.
    - Add a user to the repository.
    - Add a review for 'game_1' by the user using 'add_review_to_game'.
    - Check if the user's reviews now include the added review.

    Expected outcome: The 'add_review_to_game' function should add a review for 'game_1' by the user, and the user's
    reviews should include that review.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    repo.repository_instance.add_game(game_1)
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    review_1 = Review(user, game_1, 4, 'comment')
    services.add_review_to_game(repo.repository_instance, game_1, user, review_1)
    assert services.get_all_users_reviews(repo.repository_instance, user) == [Review(user, game_1, 4, 'comment')]


def test_delete_review():
    """
    Test the 'delete_review' function.

    - Create a new MemoryRepository instance.
    - Add 'game_1' to the repository.
    - Add a user to the repository.
    - Add a review for 'game_1' by the user.
    - Check if the user's reviews include the added review.
    - Delete the review using 'delete_review'.
    - Check if the user's reviews are now empty.

    Expected outcome: The 'delete_review' function should remove the review, and the user's reviews should be empty.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    repo.repository_instance.add_game(game_1)
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    review_1 = Review(user, game_1, 4, 'comment')
    services.add_review_to_game(repo.repository_instance, game_1, user, review_1)
    assert services.get_all_users_reviews(repo.repository_instance, user) == [Review(user, game_1, 4, 'comment')]
    services.delete_review(repo.repository_instance, review_1, user, game_1)
    assert services.get_all_users_reviews(repo.repository_instance, user) == []


def test_get_all_games_user_reviewed():
    """
    Test the 'get_all_games_user_reviewed' function.

    - Create a new MemoryRepository instance.
    - Add 'game_1' and 'game_2' to the repository.
    - Add a user to the repository.
    - Add reviews for 'game_1' and 'game_2' by the user.
    - Check if the user's reviews include both reviews for 'game_1' and 'game_2'.

    Expected outcome: The 'get_all_games_user_reviewed' function should return a list of games that the user has reviewed,
    including 'game_1' and 'game_2'.
    """
    repo.repository_instance = MemoryRepository()
    game_1 = Game(1, 'game_1')
    game_2 = Game(2, 'game_2')
    repo.repository_instance.add_game(game_1)
    repo.repository_instance.add_game(game_2)
    user = User('username', 'password')
    repo.repository_instance.add_user(user)

    review_1 = Review(user, game_1, 4, 'comment')
    review_2 = Review(user, game_2, 4, 'comment')

    services.add_review_to_game(repo.repository_instance, game_1, user, review_1)
    services.add_review_to_game(repo.repository_instance, game_2, user, review_2)

    assert services.get_all_users_reviews(repo.repository_instance, user) == [Review(user, game_1, 4, 'comment'), Review(user, game_2, 4, 'comment')]
