from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre, Game, User, Review
from flask import request
from datetime import datetime


def get_reviews(repo: AbstractRepository, user: User):
    """
    get all the user reviews
    """

    reviews = repo.get_users_reviews(user)
    return reviews


def get_favourites(repo: AbstractRepository, user: User):
    """
    get all the user favourite games
    """

    favourites = repo.get_users_favourites(user)
    return favourites


def get_user_by_username(repository: AbstractRepository, username: str):
    """Get a user object by the username"""
    return repository.get_user(username)
