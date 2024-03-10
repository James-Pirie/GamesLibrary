from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, Review, User, Favourite

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    # We only want to maintain those attributes that are in our domain model
    # For publisher, we only have name.
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

game_genres_table = Table(
    'game_genres_table', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, autoincrement=True),
    Column('username', String(255), primary_key=True),
    Column('password', String(255), nullable=False),
)

favourite_games_table = Table(
    'favourite_games', metadata,
    Column('username', ForeignKey('users.username'), nullable=False),
    Column('game_id', ForeignKey('games.game_id'), nullable=False),
    PrimaryKeyConstraint('username', 'game_id')
)

reviews_table = Table(
    'reviews', metadata,
    Column('username', ForeignKey('users.username'), nullable=False),
    Column('game_id', ForeignKey('games.game_id'), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('comment', String(255)),
    PrimaryKeyConstraint('username', 'game_id')
)


def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table)
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review),
        '_User__favourite_games': relationship(Game, secondary=favourite_games_table),
    })

    mapper(Review, reviews_table, properties={
        '_Review__rating': reviews_table.c.rating,
        '_Review__comment': reviews_table.c.comment,
        '_Review__user': relationship(User),
        '_Review__game': relationship(Game),
    })

    mapper(Favourite, favourite_games_table, properties={
        '_Favourite__user': relationship(User),
        '_Favourite__game': relationship(Game),
    })

