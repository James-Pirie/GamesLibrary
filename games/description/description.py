from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField
from games.favourites import services as favourites_services
import games.description.services as services
import games.adapters.repository as repo
from flask_wtf.csrf import CSRFProtect
from games.authentication.authentication import login_required
from games.reviews import services as rating_services

description_blueprint = Blueprint("description_bp", __name__)
csrf = CSRFProtect()


@description_blueprint.route('/gameDescription/<game_id>', methods=['GET', 'POST'])
def get_description_specific(game_id):
    """Takes in a game_id and renders a template displaying the details of the associated game"""

    session['game_id'] = game_id

    game = services.get_game_from_id(repo.repository_instance, game_id)
    form = AddFavourite()

    all_reviews = rating_services.get_all_games_reviews(repo.repository_instance, game)
    sum = 0
    for i in range(len(all_reviews)):
        sum += all_reviews[i].rating

    if len(all_reviews) != 0:
        average_rating = f"{sum / len(all_reviews)}/5"
    else:
        average_rating = ' (game not yet rated)'
    message = "Add to Favourites"
    if 'username' in session:
        current_user = favourites_services.get_user_by_username(repo.repository_instance, session['username'])

        if game in favourites_services.get_all_favourites(repo.repository_instance, current_user):
            message = "Remove from Favourites"

    if form.validate_on_submit():
        # Add the selected game to the user's favorites
        return redirect(url_for('description_bp.add_game', game_id=game_id))

    return render_template('gameDescription.html', game=game, form=form, message=message, average_rating=average_rating)


@description_blueprint.route('/gameDescription/<game_id>/addFavourites')
@login_required
def add_game(game_id):
    selected_game = services.get_game_from_id(repo.repository_instance, game_id)
    current_user = favourites_services.get_user_by_username(repo.repository_instance, session['username'])
    # Add the selected game to the user's favorites
    if selected_game in favourites_services.get_all_favourites(repo.repository_instance, current_user):
        favourites_services.remove_game_from_users_favourites(repo.repository_instance, current_user, selected_game)
    else:
        favourites_services.add_game_to_users_favourites(repo.repository_instance, current_user, selected_game)
    return redirect(url_for('description_bp.get_description_specific', game_id=game_id))


class AddFavourite(FlaskForm):
    add_to_favourites_form = SubmitField('AddFavourite')







