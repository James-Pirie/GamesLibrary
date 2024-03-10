import pytest
from games.adapters import database_repository
from games.adapters import orm
from games.domainmodel.model import Publisher, Genre, Game, User, Review, Favourite


def insert_user(empty_session, values=None):
    username = "testusername123"
    password = "Password123"

    if values is not None:
        username = values[0]
        password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': username, 'password': password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': username}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_publisher(empty_session, name="Publisher Name"):
    empty_session.execute("INSERT INTO publishers (name) VALUES (:name)", {"name": name})
    row = empty_session.execute("SELECT name FROM publishers WHERE name = :name", {"name": name}).fetchone()
    return row[0]


def insert_game(empty_session):
    game_data = {
        "game_title": "GameA",
        "game_price": 49.99,
        "release_date": "2023-01-01",
        "game_description": "Random game description",
    }

    publisher_name = "PublisherA"
    insert_publisher(empty_session, publisher_name)

    game_data["publisher_name"] = publisher_name
    empty_session.execute(
        "INSERT INTO games (game_title, game_price, release_date, game_description, publisher_name) "
        "VALUES (:game_title, :game_price, :release_date, :game_description, :publisher_name)",
        game_data
    )

    row = empty_session.execute("SELECT game_id FROM games").fetchone()
    return row[0]


def insert_genre(empty_session, genre_name="Action"):
    empty_session.execute("INSERT INTO genres (genre_name) VALUES (:genre_name)", {"genre_name": genre_name})
    row = empty_session.execute("SELECT genre_name FROM genres WHERE genre_name = :genre_name", {"genre_name": genre_name}).fetchone()
    return row[0]


def insert_review(empty_session, username, game_id, rating, comment):
    empty_session.execute(
        "INSERT INTO reviews (username, game_id, rating, comment) "
        "VALUES (:username, :game_id, :rating, :comment)",
        {"username": username, "game_id": game_id, "rating": rating, "comment": comment}
    )


def insert_favourite(empty_session, user, game):
    empty_session.execute(
        "INSERT INTO favourite_games (username, game_id) VALUES (:username, :game_id)",
        {"username": user.username, "game_id": game.game_id}
    )


def make_publisher():
    publisher = Publisher("PublisherA")
    return publisher


def make_genre():
    genre = Genre("Action")
    return genre


def make_game():
    game = Game(1, "GameA")
    return game


def make_user():
    user = User("testusername123", "Password123")
    return user


def make_review():
    user = make_user()
    game = make_game()
    review = Review(user, game, 5, "test comment")
    return review


def make_favourite(user, game):
    favourite = Favourite(user, game)
    return favourite


def test_loading_of_users(empty_session):
    users = list()
    users.append(("testusername123", "Password123"))
    users.append(("testusername234", "Password123"))
    insert_users(empty_session, users)

    expected = [
        User("testusername123", "Password123"),
        User("testusername234", "Password123")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("testusername123", "Password123")]


def test_loading_of_publishers(empty_session):
    publisher_name = insert_publisher(empty_session, "PublisherA")
    expected_publisher = make_publisher()
    fetched_publisher = empty_session.query(Publisher).one()

    assert expected_publisher == fetched_publisher
    assert publisher_name == fetched_publisher.publisher_name


def test_saving_of_games(empty_session):
    game_id = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_id == fetched_game.game_id


def test_loading_of_genres(empty_session):
    genre_name = insert_genre(empty_session, "Action")
    expected_genre = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_genre == fetched_genre
    assert genre_name == fetched_genre.genre_name


def test_saving_of_reviews(empty_session):
    insert_user(empty_session, ("testusername123", "Password123"))
    game_id = insert_game(empty_session)
    insert_review(empty_session, "testusername123", game_id, 5, "test comment")
    review = make_review()
    expected_review = empty_session.query(Review).one()

    assert expected_review == review


def test_saving_of_favorites(empty_session):
    user = make_user()
    game = make_game()
    insert_game(empty_session)
    insert_favourite(empty_session, user, game)
    favourite = make_favourite(user, game)
    expected_favourite = empty_session.query(Favourite).one()

    assert expected_favourite.username == favourite.user.username and expected_favourite.game_id == favourite.game.game_id

