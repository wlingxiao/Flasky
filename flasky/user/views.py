from . import user
from flasky.auth.models import User, db
from flask import jsonify, render_template, request
from sqlalchemy import and_
import datetime


@user.route('/load_all_user', methods=['GET'])
def load_all_user():
    username = request.args.get('username')
    email = request.args.get('email')
    sign_up_time_start = request.args.get('sign_up_time_start')
    sign_up_time_end = request.args.get('sign_up_time_end')
    last_visit_time_start = request.args.get('last_visit_time_start')
    last_visit_time_end = request.args.get('last_visit_time_end')

    query_param = []
    if username:
        query_param.append(User.username == username)

    if email:
        query_param.append(User.email == email)

    datetime_min = datetime.time.min
    datetime_max = datetime.time.max

    if sign_up_time_start:
        sign_up_time_start_datetime = datetime.datetime.strptime(sign_up_time_start, '%Y-%m-%d')
        query_param.append(User.sign_up_time >= datetime.datetime.combine(sign_up_time_start_datetime, datetime_min))

    if sign_up_time_end:
        sign_up_time_end_datetime = datetime.datetime.strptime(sign_up_time_end, '%Y-%m-%d')
        query_param.append(User.sign_up_time <= datetime.datetime.combine(sign_up_time_end_datetime, datetime_max))

    if last_visit_time_start:
        last_visit_time_start_datetime = datetime.datetime.strptime(last_visit_time_start, '%Y-%m-%d')
        query_param.append(User.sign_up_time >= datetime.datetime.combine(last_visit_time_start_datetime, datetime_min))

    if last_visit_time_end:
        last_visit_time_end_datetime = datetime.datetime.strptime(last_visit_time_end, '%Y-%m-%d')
        query_param.append(User.sign_up_time <= datetime.datetime.combine(last_visit_time_end_datetime, datetime_max))

    users = User.query.filter(and_(*query_param)).order_by(User.last_visit_time.desc()).limit(20).all()

    filter_users_size = User.query.filter(and_(*query_param)).count()

    result = {
        'code': 200,
        'msg': 'OK',
        'size': filter_users_size,
        'data': [
            {'username': per_user.username, 'email': per_user.email,
             'sign_up_time': per_user.sign_up_time.strftime('%Y-%m-%d'),
             'last_visit_time': per_user.last_visit_time.strftime('%Y-%m-%d')}
            for per_user in users]
    }

    return jsonify(result)


@user.route('/user_manager', methods=['GET'])
def user_manager():
    return render_template('user/user_manager.html')
