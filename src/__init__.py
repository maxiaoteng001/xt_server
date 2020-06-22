import os
from flask import Flask
from src.utils.logger_helper import logger_config


def create_app(test_config=None):
    # create and configure the app
    logger_config(log_name='xt_server', always=True)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import tools
    from . import api
    app.register_blueprint(tools.tools_bp)
    app.register_blueprint(api.api_bp)
    print(app.url_map)
    return app