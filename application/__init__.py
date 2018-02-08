''' Flask Application Factory

    Blueprint Flask application using the factory pattern,
    with configuration setup and blueprint module registration
'''
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension


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

    # Load default config values
    app.config.from_object('config.default')
    # Load instance config values not stored in repo
    app.config.from_pyfile('config.py')
    # Load environment config values
    app.config.from_envvar('APP_CONFIG_FILE')

    # Initialize bootstrap
    Bootstrap(app)

    # Debug = True to enable the toolbar
    toolbar = DebugToolbarExtension(app)

    # Load blueprint modules
    from application.site.routes import mod as site
    from application.api.routes import mod as api

    # Register blueprint modules for use
    app.register_blueprint(site)
    app.register_blueprint(api, url_prefix='/api')

    return app