from flask_restful import Resource, reqparse
from flask import jsonify, request
from . import api_blueprint
from flask_restful import Api
from flasky.auth.models import User
from sqlalchemy import and_
import datetime
from flask_login import LoginManager, login_required, login_user, current_user
from .decorators import permission_required


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return {'id': user.id,
                'username': user.username,
                'email': user.email,
                'sign_up_time': user.sign_up_time.timestamp(),
                'last_visit_time': user.last_visit_time.timestamp()}, 200


class UserListResource(Resource):
    def get(self):
        username = request.args.get('username')
        email = request.args.get('email')
        sign_up_time_start = request.args.get('sign_up_time_start')
        sign_up_time_end = request.args.get('sign_up_time_end')
        last_visit_time_start = request.args.get('last_visit_time_start')
        last_visit_time_end = request.args.get('last_visit_time_end')
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)

        if page_size > 20:
            page_size = 10

        query_param = []
        if username:
            query_param.append(User.username == username)

        if email:
            query_param.append(User.email == email)

        datetime_min = datetime.time.min
        datetime_max = datetime.time.max

        if sign_up_time_start:
            sign_up_time_start_datetime = datetime.datetime.strptime(sign_up_time_start, '%Y-%m-%d')
            query_param.append(
                User.sign_up_time >= datetime.datetime.combine(sign_up_time_start_datetime, datetime_min))

        if sign_up_time_end:
            sign_up_time_end_datetime = datetime.datetime.strptime(sign_up_time_end, '%Y-%m-%d')
            query_param.append(User.sign_up_time <= datetime.datetime.combine(sign_up_time_end_datetime, datetime_max))

        if last_visit_time_start:
            last_visit_time_start_datetime = datetime.datetime.strptime(last_visit_time_start, '%Y-%m-%d')
            query_param.append(
                User.sign_up_time >= datetime.datetime.combine(last_visit_time_start_datetime, datetime_min))

        if last_visit_time_end:
            last_visit_time_end_datetime = datetime.datetime.strptime(last_visit_time_end, '%Y-%m-%d')
            query_param.append(
                User.sign_up_time <= datetime.datetime.combine(last_visit_time_end_datetime, datetime_max))

        users = User.query.filter(and_(*query_param)).order_by(User.last_visit_time.desc()).limit(page_size).offset(
            (page - 1) * page_size)

        filter_users_size = User.query.filter(and_(*query_param)).count()

        result = {
            'code': 200,
            'msg': 'OK',
            'size': filter_users_size,
            'data': [
                {'id': per_user.id, 'username': per_user.username, 'email': per_user.email,
                 'sign_up_time': per_user.sign_up_time.strftime('%Y-%m-%d %H:%M'),
                 'last_visit_time': per_user.last_visit_time.strftime('%Y-%m-%d %H:%M')}
                for per_user in users]
        }

        return jsonify(result)

    def post(self):
        pass


def _validate_exist(**kwargs):
    return User.query.filter_by(**kwargs).first()


@api_blueprint.route('/users/email/<string:email>', methods=['GET'])
def validate_email(email):
    if _validate_exist(email=email):
        return jsonify({'msg': '邮箱已注册'}), 302
    return jsonify({'msg': '邮箱已注册'}), 204


@api_blueprint.route('/users/username/<string:username>', methods=['GET'])
def validate_username(username):
    if _validate_exist(username=username):
        return jsonify({'msg': '用户名已注册'}), 302
    return jsonify({'msg': '用户名未注册'}), 204


user_api = Api(api_blueprint)
user_api.add_resource(UserResource, '/users/<int:user_id>')
user_api.add_resource(UserListResource, '/users')
