from . import auth
from flask import render_template, jsonify
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.csrf import CSRFProtect
from .models import db, User

from email.utils import parseaddr
from flask_login import LoginManager

login_manager = LoginManager()

csrf = CSRFProtect()


class LoinForm(Form):
    username_or_email = StringField(u'用户名或邮箱', validators=DataRequired('required'))
    password = PasswordField(u'密码', validators=DataRequired('required'))


class SignUpForm(Form):
    username = StringField(u'用户名', validators=[DataRequired('required')])
    email = StringField(u'邮箱', validators=[DataRequired('required'), Email('email')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])
    confirm_password = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password', message=u'密码输入不一致')])


@auth.route('/')
def index():
    return 'home page'


def check_email(input_email):
    return '@' in parseaddr(input_email)[1]


# 登录
@auth.route('/log_in', methods=['GET', 'POST'])
def login_in():
    form = LoinForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        if check_email(username_or_email):
            if User.query.filter_by(email=username_or_email):
                return jsonify({'code': 200, 'msg': 'OK'})
            else:
                return jsonify({'code': 404, 'msg': '该邮箱未注册'})
        else:
            if User.query.filter_by(username=username_or_email):
                return jsonify({'code': 200, 'msg': 'OK'})
            else:
                return jsonify({'code': 404, 'msg': '该用户名未注册'})

    return render_template('auth/log_in.html', form=form)


@auth.route('/validate_username/<username>')
def validate_username(username):
    if _validate_email(username):
        return jsonify({'code': 400, 'msg': '用户名已注册'})
    return jsonify({'code': 200, 'msg': 'OK'})


def _validate_username(username):
    return User.query.filter_by(username=username)


@auth.route('/validate_email/<email>')
def validate_email(email):
    if _validate_email(email):
        return jsonify({'code': 400, 'msg': '邮箱已注册'})
    return jsonify({'code': 200, 'msg': 'OK'})


def _validate_email(email):
    return User.query.filter_by(email=email)


# 注册
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    pass


# 注销
@auth.route('/sign_out')
def sign_out():
    pass
