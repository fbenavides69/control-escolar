from flask import Blueprint
from . import views

mod = Blueprint('site', __name__, template_folder='templates')

# Define the URL paths  to view functions
mod.add_url_rule('/', 'index', views.index)
#mod.add_url_rule('/profile/<email>', 'profile', views.profile)
