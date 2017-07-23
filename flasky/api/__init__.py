from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

import flasky.api.user_resources
import flasky.api.session_resources
import flasky.api.post_resources
