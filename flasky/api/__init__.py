from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

import flasky.api.UserApi
import flasky.api.SessionApi
