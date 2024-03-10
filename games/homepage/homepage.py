from flask import Blueprint
from flask import render_template

# Create the blueprint
home_bp = Blueprint('home_bp', __name__)


# Define routes
@home_bp.route('/')
def homepage():
    return render_template('homepage.html')
