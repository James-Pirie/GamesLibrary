import csv
from typing import List, Optional
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Review
from pathlib import Path
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from bisect import insort_left


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = []
        self.__genres = []
        self.__users = []

    def add_game(self, game: Game):
        if isinstance(game, Game):
            # insort the game and maintain sorted order
            insort_left(self.__games, game)

    def get_game_by_id(self, game_id: int):
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return None

    def get_games(self) -> List[Game]:
        return self.__games

    def add_genre(self, genre: Genre):
        insort_left(self.__genres, genre)

    def get_genres(self) -> List[Genre]:
        unique_genres = []
        for genre in self.__genres:
            if genre not in unique_genres:
                unique_genres.append(genre)
        return unique_genres

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        games_with_genre = []
        for game in self.__games:
            if genre in game.genres:
                games_with_genre.append(game)
        return games_with_genre

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username: str):
        for user in self.__users:
            if user.username == username:
                return user
        return None

    def add_game_to_favourite(self, user: User, game: Game):
        user.add_favourite_game(game)

    def get_users_favourites(self, user: User):
        return user.favourite_games

    def remove_game_from_favourites(self, user: User, game: Game):
        user.remove_favourite_game(game)

    def get_users_reviews(self, user: User):
        return user.reviews

    def get_games_reviews(self, game: Game):
        return game.reviews

    def add_review(self, game: Game, user: User, review: Review):
        user.add_review(review)
        game.add_review(review)

    def remove_review(self, game: Game, user: User, review: Review):
        user.remove_review(review)
        game.remove_review(review)

    def add_multiple_genres(self, genres: List[Genre]):
        """ Add many genres to the repository. """
        pass

    def add_multiple_publishers(self, publisher: List[Publisher]):
        """ Add multiple games to the repository of games. """
        pass

    def add_multiple_games(self, games: List[Game]):
        """ Add multiple games to the repository of games. """
        pass

    def search_games(self, search_option: str, search_input: str):
        """ Filter games by search """


def load_games(data_path: Path, repository: MemoryRepository):
    games_file = str(Path(data_path) / "games.csv")
    reader = GameFileCSVReader(games_file)
    reader.read_csv_file()
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres
    for game in games:
        repository.add_game(game)
    for genre in genres:
        repository.add_genre(genre.genre_name)


def populate(data_path: Path, repository: MemoryRepository):
    load_games(data_path, repository)

