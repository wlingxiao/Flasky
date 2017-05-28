# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    app.secret_key = 's3cr3t'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'

    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from flasky.auth.views import csrf
    csrf.init_app(app)

    from flasky.auth import auth
    app.register_blueprint(auth)

    return app
