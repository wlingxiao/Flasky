# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    app.secret_key = 's3cr3t'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
    app.config['WTF_CSRF_ENABLED'] = False
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from flasky.auth.views import csrf
    csrf.init_app(app)

    from flasky.auth import auth
    app.register_blueprint(auth)

    from flasky.auth.models import db
    db.init_app(app)

    from flasky.auth.views import login_manager
    login_manager.init_app(app)

    return app
