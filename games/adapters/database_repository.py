from abc import ABC
from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from games.adapters.repository import AbstractRepository
from games.adapters.utils import search_string
from games.domainmodel.model import Game, Publisher, Genre, User, Review, Favourite


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Game_data
    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def get_number_of_games(self):
        total_games = self._session_cm.session.query(Game).count()
        return total_games

    def get_publishers(self) -> List[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_number_of_publishers(self) -> int:
        pass

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre._Genre__genre_name).all()
        genre_strings = [genre._Genre__genre_name for genre in genres]
        return genre_strings

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    def search_games(self, search_option: str, search_input: str) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        if search_option == "Title":
            games = self._session_cm.session.query(Game).filter(
                Game._Game__game_title.ilike(f"%{search_input.strip().lower()}%")).all()
        elif search_option == "Publisher":
            games = self._session_cm.session.query(Game).filter(
                Publisher._Publisher__publisher_name.ilike(f"%{search_input.strip().lower()}%")).all()

        return games

    def add_game_to_favourite(self, user: User, game: Game):
        favourite = Favourite(user, game)

        with self._session_cm as scm:
            scm.session.merge(favourite)
            scm.commit()

    def add_review(self, game: Game, user: User, review: Review):
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_game_by_id(self, game_id: int):
        game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        return game

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        games = self._session_cm.session.query(Game).filter(Game._Game__genres.contains(genre)).all()
        return games

    def get_games_reviews(self, game: Game):
        reviews = self._session_cm.session.query(Review).filter_by(game_id=game.game_id).all()
        return reviews

    def get_user(self, username: str):
        user = self._session_cm.session.query(User).filter(User._User__username == username).one_or_none()
        return user

    def get_users_favourites(self, user: User):
        favourites = self._session_cm.session.query(Favourite).filter_by(username=user.username).all()
        favourite_games_objects = []
        for item in favourites:
            favourite_games_objects.append(self.get_game_by_id(item.game_id))
        return favourite_games_objects

    def get_users_reviews(self, user: User):
        reviews = self._session_cm.session.query(Review).filter_by(username=user.username).all()
        return reviews

    def remove_game_from_favourites(self, user: User, game: Game):
        with self._session_cm as scm:
            selected_favourite = (
                scm.session.query(Favourite).filter_by(game_id=game.game_id, username=user.username).first()
            )
            scm.session.delete(selected_favourite)
            scm.commit()

    def remove_review(self, game: Game, user: User, review: Review):
        with self._session_cm as scm:
            selected_review = (
                scm.session.query(Review).filter_by(game_id=game.game_id, username=user.username).first()
            )
            scm.session.delete(selected_review)
            scm.commit()
