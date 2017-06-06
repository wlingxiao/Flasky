from . import auth
from flask import render_template, jsonify, url_for, redirect
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.csrf import CSRFProtect
from .models import db, User
from datetime import datetime

from email.utils import parseaddr
from flask_login import LoginManager, login_required, login_user, current_user

login_manager = LoginManager()

csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class LoinForm(Form):
    username_or_email = StringField(u'用户名或邮箱', validators=[DataRequired('required')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])


class SignUpForm(Form):
    username = StringField(u'用户名', validators=[DataRequired('required')])
    email = StringField(u'邮箱', validators=[DataRequired('required'), Email('email')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])
    confirm_password = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password', message=u'密码输入不一致')])


@auth.route('/')
def index():
    return 'home page'


def check_email(input_email):
    """ 判断字符串是否为邮箱 """

    return '@' in parseaddr(input_email)[1]


@auth.route('/login', methods=['GET', 'POST'])
def login_in():
    """ 登录 """

    form = LoinForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        request_login_user = None
        if check_email(username_or_email):
            request_login_user = User.query.filter_by(email=username_or_email).first()
            if request_login_user:
                if request_login_user.verify_password(form.password.data):
                    login_user(request_login_user)
                    return jsonify({'code': 200, 'msg': 'OK'})
                else:
                    return jsonify({'code': 400, 'msg': u'密码错误'})
            else:
                return jsonify({'code': 404, 'msg': u'该邮箱未注册'})
        else:
            request_login_user = User.query.filter_by(username=username_or_email).first()
            if request_login_user:
                if request_login_user.verify_password(form.password.data):
                    login_user(request_login_user)
                    return jsonify({'code': 200, 'msg': 'OK'})
                else:
                    return jsonify({'code': 400, 'msg': u'密码错误'})
            else:
                return jsonify({'code': 404, 'msg': u'该用户名未注册'})

    return render_template('auth/login.html', form=form)


@auth.route('/validate_username/<username>', methods=['POST'])
def validate_username(username):
    if _validate_exist(username=username):
        return jsonify({'code': 400, 'msg': '用户名已注册'})
    return jsonify({'code': 200, 'msg': 'OK'})


@auth.route('/validate_email/<email>', methods=['POST'])
def validate_email(email):
    if _validate_exist(email=email):
        return jsonify({'code': 400, 'msg': '邮箱已注册'})
    return jsonify({'code': 200, 'msg': 'OK'})


def _validate_exist(**kwargs):
    return User.query.filter_by(**kwargs).first()


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """ 用户注册 """

    form = SignUpForm()

    if form.validate_on_submit():
        old_user_filter_by_username = User.query.filter_by(username=form.username.data).first()
        if old_user_filter_by_username:
            return jsonify({'code': 400, 'msg': u'用户名已注册'})

        old_user_filter_by_email = User.query.filter_by(email=form.email.data).first()
        if old_user_filter_by_email:
            return jsonify({'code': 400, 'msg': u'邮箱已注册'})
        now = datetime.now()
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    sign_up_time=now, last_visit_time=now)
        db.session.add(user)
        db.session.commit()
        return jsonify({'code': 201, 'msg': 'Created'})

    return render_template('auth/sign_up.html', form=form)


# 注销
@auth.route('/sign_out')
@login_required
def sign_out():
    return 'sign out'
