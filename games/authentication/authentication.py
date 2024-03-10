from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator
from functools import wraps

import games.authentication.services as services
import games.adapters.repository as repo

authentication_blueprint = Blueprint(
    'authentication_bp', __name__)


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_error = None

    if form.validate_on_submit():
        # try to add a new user
        try:
            services.add_user(form.username.data, form.password.data, repo.repository_instance)
            # redirect the user to the login page.
            return redirect(url_for('authentication_bp.login'))
        # if name if not unique, tell user that name is already taken
        except services.NameNotUniqueException:
            username_error = 'Your user name is already taken - please supply another - usernames are case insensitive'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'credentials.html',
        title='Register',
        form=form,
        username_error_message=username_error,
        handler_url=url_for('authentication_bp.register'),
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error = None
    password_error = None

    if form.validate_on_submit():
        # try to login and return to homepage
        try:
            user = services.get_user(form.username.data, repo.repository_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repository_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.homepage'))

        except services.UnknownUserException:
            username_error = 'Invalid Username'

        except services.AuthenticationException:
            password_error = 'Invalid Password'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'credentials.html',
        title='Login',
        username_error_message=username_error,
        password_error_message=password_error,
        form=form,
    )


@authentication_blueprint.route('/logout')
def logout():
    """
    Log the user out and go to home page
    """
    session.clear()
    return redirect(url_for('home_bp.homepage'))


def login_required(view):
    """
    Function that will mark something as login required in order to use this component
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           [DataRequired(message='Username is required'),
                            Length(min=3, message='Username must be at least 3 characters')],
                           render_kw={"placeholder": "Username"})

    password = PasswordField('Password',
                             [DataRequired(message='Password is required'),
                              PasswordValid()],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField('REGISTER')


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', [DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('LOGIN')
