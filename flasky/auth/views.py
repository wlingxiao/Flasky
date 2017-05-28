from . import auth
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


class LogInForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired('required')])
    email = StringField(u'邮箱', validators=[DataRequired('required'), Email('email')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])
    repeat_password = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password', message=u'密码输入不一致')])


@auth.route('/')
def index():
    return 'home page'


# 登录
@auth.route('/log_in', methods=['GET', 'POST'])
def login_in():
    form = LogInForm()

    if form.validate_on_submit():
        return redirect(url_for('auth.index'))
    return render_template('auth/log_in.html', form=form)


# 注册
@auth.route('/sign_up')
def sign_up():
    pass


# 注销
@auth.route('/sign_out')
def sign_out():
    pass
