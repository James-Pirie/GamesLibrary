from flask import Blueprint
from flask import request, render_template, redirect, session
from games.authentication.authentication import login_required
from games.domainmodel.model import Genre
import games.adapters.repository as repo
import games.userprofile.services as services


user_profile_blueprint = Blueprint(
    "userprofile_bp", __name__
)


@user_profile_blueprint.route('/userprofile', methods=['GET'])
@login_required
def userprofile():
    username = session.get('username')
    current_user = services.get_user_by_username(repo.repository_instance, username)

    reviews = services.get_reviews(repo.repository_instance, current_user)
    fav_games = services.get_favourites(repo.repository_instance, current_user)

    # only show the latest 5 games
    if len(fav_games) > 5:
        fav_games = fav_games[-5:]

    # only show latest 5 reviews
    if len(reviews) > 5:
        reviews = reviews[-5:]

    return render_template(
        'userProfile.html',
        username=username,
        fav_games=fav_games,
        reviews=reviews,
    )

