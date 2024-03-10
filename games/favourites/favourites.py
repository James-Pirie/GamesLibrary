import games.favourites.services as services
import games.adapters.repository as repo
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import SubmitField
from games.authentication.authentication import login_required

favourites_blueprint = Blueprint('favourites_bp', __name__)

csrf = CSRFProtect()


@favourites_blueprint.route('/favourites', methods=['GET', 'POST'])
@login_required
def users_favourites():
    username = session.get('username')
    current_user = services.get_user_by_username(repo.repository_instance, username)
    favourite_games = services.get_all_favourites(repo.repository_instance, current_user)
    form = RemoveFavouriteForm()

    return render_template('usersFavourites.html', username=username, favourite_games=favourite_games, form=form)


@favourites_blueprint.route('/favourites/remove-favourite', methods=['POST'])
@login_required
def process_form():
    game_id = request.form['game_id']
    # Store the game_id in the session or perform other actions as needed
    selected_game = services.get_game_from_id(repo.repository_instance, game_id)
    if 'username' in session:
        current_user = services.get_user_by_username(repo.repository_instance, session['username'])
        services.remove_game_from_users_favourites(repo.repository_instance, current_user, selected_game)
    return redirect(url_for("favourites_bp.users_favourites"))


class RemoveFavouriteForm(FlaskForm):
    remove_from_favourites = SubmitField('AddFavourite')
