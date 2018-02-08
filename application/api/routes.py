from flask import Blueprint
from . import views

mod = Blueprint('api', __name__)

# Define the URL paths  to view functions
mod.add_url_rule('/version', 'version', views.version)
