#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' Flask Application Factory

    Blueprint Flask application using the factory pattern,
    with configuration setup and blueprint module registration
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_security import Security
from flask_security import SQLAlchemyUserDatastore
from flask_security import utils
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension

from .models import db
from .models import User
from .models import Role
from .admin import admin


def create_app():
    ''' create_app

        input:
            None

        output:
            app -- flask web application instance

        Read configuration values in the following order:
            1) default, values which can be overwritten later
            2) intance, for your eyes only not stored in repo values
            3) environment, selectable values from:
                - development
                - stagging
                - production

        Setup web interface with Bootstrap framework
    '''

    # Initialize app
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False

    # Load default config values
    app.config.from_object('config.default')
    # Load instance config values not stored in repo
    app.config.from_pyfile('config.py')
    # Load environment config values
    app.config.from_envvar('APP_CONFIG_FILE')

    # Create database connection
    db.init_app(app)

    # Instantiate Admin section
    admin.init_app(app)

    # Intialize mail
    Mail(app)

    # Initialize bootstrap
    Bootstrap(app)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Executes before the first request is processed.
    @app.before_first_request
    def before_first_request():

        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "end-user" -- unless they already exist
        user_datastore.find_or_create_role(
            name=app.config['ADMIN_USER'], description='Administrador')

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the
        # password.
        encrypted_password = utils.encrypt_password(
            app.config['ADMIN_PASSWORD'])
        if not user_datastore.get_user(app.config['ADMIN_EMAIL']):
            user_datastore.create_user(
                email=app.config['ADMIN_EMAIL'], password=encrypted_password)

        # Commit any database changes; the User and Roles must exist before
        # we can add a Role to the User
        db.session.commit()

        # "admin" role. (This will have no effect if the Users already have
        # these Roles.) Again, commit any database changes.
        user_datastore.add_role_to_user(
            app.config['ADMIN_EMAIL'], app.config['ADMIN_USER'])

        # Commit the Admin User and Role
        db.session.commit()

    # Debug = True to enable the toolbar
    toolbar = DebugToolbarExtension(app)

    # Load blueprint modules
    from application.site.routes import mod as site
    from application.api.routes import mod as api

    # Register blueprint modules for use
    app.register_blueprint(site)
    app.register_blueprint(api, url_prefix='/api')

    return app
