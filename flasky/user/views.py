from . import user
from flasky.auth.models import User, db
from flask import jsonify, render_template, request
from sqlalchemy import and_
from datetime import datetime


@user.route('/load_all_user', methods=['GET'])
def load_all_user():
    username = request.args.get('username')
    email = request.args.get('email')
    sign_up_time = request.args.get('sign_up_time')
    last_visit_time = request.args.get('last_visit_time')

    query_param = []
    if username:
        query_param.append(User.username == username)

    if email:
        query_param.append(User.email == email)

    users = User.query.filter(and_(*query_param)).limit(20).all()

    filter_users_size = User.query.filter(and_(*query_param)).count()

    result = {
        'code': 200,
        'msg': 'OK',
        'size': filter_users_size,
        'data': [
            {'username': user.username, 'email': user.email, 'sign_up_time': user.sign_up_time.strftime('%Y-%m-%d'),
             'last_visit_time': user.last_visit_time.strftime('%Y-%m-%d')} for
            user in users]
    }

    return jsonify(result)


@user.route('/user_manager', methods=['GET'])
def user_manager():
    return render_template('user/user_manager.html')
