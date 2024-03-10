import abc
from games.domainmodel.model import Game, Genre, Publisher, User, Review
from typing import List, Optional

# the instance of the repository
repository_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):
        """
        Adds a game to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, game_id: int) -> Optional[Game]:
        """
        Returns a game with the specified game id.

        If there is no game with the specified id, then returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """
        Returns all games in the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """
        Adds a game to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """
        Returns all games in the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """
        Return all games of a certain genre
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str):
        """
        Return user with the given username, or none if it does not exist
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """
        Add a new user
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game_to_favourite(self, user: User, game: Game):
        """
        Add a new game to user's favourites
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_users_favourites(self, user: User):
        """
        Add a new game to user's favourites
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_game_from_favourites(self, user: User, game: Game):
        """
        Remove a game from user's favourites
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_users_reviews(self, user: User):
        """
        Get all of a user's reviews
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_reviews(self, game: Game):
        """
        Get all of the reviews on a game
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, game: Game, user: User, review: Review):
        """Add a review to a game and a user"""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_review(self, game: Game, user: User, review: Review):
        """Remove a review from a user and game"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_genres(self, genres: List[Genre]):
        """ Add many genres to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_publishers(self, publisher: List[Publisher]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_games(self, games: List[Game]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_games(self, search_option: str, search_input: str):
        """
        Search for game by title or publisher
        """
        raise NotImplementedError



