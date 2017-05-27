# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    app.secret_key = 'are you ok'

    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    return app
