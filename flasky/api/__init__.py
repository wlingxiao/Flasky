from flask import Blueprint
from flask_restful import Api
from .User import User

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_blueprint)
api.add_resource(User, '/users/<int:id>')
