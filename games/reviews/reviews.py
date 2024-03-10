import games.reviews.services as services
import games.adapters.repository as repo
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from games.authentication.authentication import login_required
from wtforms import StringField, PasswordField, SubmitField, URLField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from games.domainmodel.model import User, Review, Game
import json


reviews_blueprint = Blueprint('reviews_bp', __name__)

csrf = CSRFProtect()


@reviews_blueprint.route('/gamesReviews', methods=['GET'])
def game_reviews():
    game = services.get_game_from_id(repo.repository_instance, session['game_id'])
    reviews = services.get_all_games_reviews(repo.repository_instance, game)

    return render_template('gameReviews.html', reviews=reviews, game=game)


@reviews_blueprint.route('/userReviews', methods=['GET', 'POST'])
@login_required
def user_reviews():
    user = services.get_user_by_username(repo.repository_instance, session['username'])
    reviews = services.get_all_users_reviews(repo.repository_instance, user)
    form = DeleteReviewForm()
    return render_template('userReviews.html', reviews=reviews, user=user, form=form)


@reviews_blueprint.route('/addReview', methods=['GET', 'POST'])
@login_required
def new_review():
    form = NewReviewForm()
    game = services.get_game_from_id(repo.repository_instance, session['game_id'])

    current_user = services.get_user_by_username(repo.repository_instance, session['username'])

    already_reviewed = game in services.get_all_games_user_reviewed(repo.repository_instance, current_user)

    if form.validate_on_submit():
        content = form.content.data
        rating = form.rating.data

        user = services.get_user_by_username(repo.repository_instance, session['username'])
        review = Review(user, game, rating, content)

        services.add_review_to_game(repo.repository_instance, game, user, review)

        flash('Review submitted successfully!', 'success')
        return redirect(url_for('reviews_bp.game_reviews'))  # Redirect to another page after successful submission

    return render_template('addreview.html', form=form, already_reviewed=already_reviewed)


@reviews_blueprint.route('/deleteReview', methods=['GET', 'POST'])
@login_required
def delete_review():
    game_id = request.form['game_id']
    game = services.get_game_from_id(repo.repository_instance, game_id)
    user = services.get_user_by_username(repo.repository_instance, session['username'])
    users_reviews = services.get_all_users_reviews(repo.repository_instance, user)
    for review in users_reviews:
        if review.game == game:
            services.delete_review(repo.repository_instance, review, user, game)
    return redirect(url_for("reviews_bp.user_reviews"))


class DeleteReviewForm(FlaskForm):
    submit = SubmitField('Submit')


class NewReviewForm(FlaskForm):
    content = StringField('Content', [DataRequired()], render_kw={"placeholder": "Content"})
    submit = SubmitField('Submit')
    rating = SelectField('Rating', choices=[('1', '1/5'), ('2', '2/5'), ('3', '3/5'), ('4', '4/5'), ('5', '5/5')],
                          validators=[InputRequired()], coerce=int)


