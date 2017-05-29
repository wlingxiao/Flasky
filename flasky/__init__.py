# -*- coding: utf-8 -*-

from flask import Flask
import os


def create_app(config=None):
    app = Flask(__name__)

    app.config.update(dict(
        SECRET_KEY='s3cr3t',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'flasky.db'),
        WTF_CSRF_ENABLED=True
    ))
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    app.config.update(config or {})

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from flasky.auth.views import csrf
    csrf.init_app(app)

    from flasky.auth import auth
    app.register_blueprint(auth)

    from flasky.user import user
    app.register_blueprint(user)

    from flasky.auth.models import db
    db.init_app(app)

    from flasky.auth.views import login_manager
    login_manager.init_app(app)

    return app
