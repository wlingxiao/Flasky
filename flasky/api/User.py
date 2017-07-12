from flask_restful import Resource
from flask import jsonify


class User(Resource):
    def get(self, id):
        return jsonify({'name': 'xiaoming', 'id': 1})
