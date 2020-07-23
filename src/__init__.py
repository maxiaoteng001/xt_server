import os
from flask import Flask, render_template, url_for
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

    from . import tools
    from . import api
    from . import data
    app.register_blueprint(tools.tools_bp)
    app.register_blueprint(api.api_bp)
    app.register_blueprint(data.data_bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    @app.route('/index.html')
    def index():
        return render_template('index.html')

    # @app.route("/all-links")
    # def all_links():
    #     return render_template("all_links.html", links=links)

    # links = []
    # print(app.url_map.iter_rules())
    # for rule in app.url_map.iter_rules():
    #     print(rule.defaults, rule.arguments)
    #     if len(rule.defaults) >= len(rule.arguments):
    #         url = url_for(rule.endpoint, **(rule.defaults or {}))
    #         links.append((url, rule.endpoint))
    # print(links)

    return app