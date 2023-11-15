import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
      SECRET_KEY="dev", # Change to something less obvious/randomised in production
      DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
      os.makedirs(app.instance_path)
    except OSError:
      pass
    
    # Register functions related to managing the database
    from . import db
    db.init_app(app)

    # Register blueprint which bundles several auth views
    from . import auth
    app.register_blueprint(auth.bp)

    return app