# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class LoinForm(Form):
    username_or_email = StringField(u'用户名或邮箱', validators=[DataRequired('required')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])


class SignUpForm(Form):
    username = StringField(u'用户名', validators=[DataRequired('required')])
    email = StringField(u'邮箱', validators=[DataRequired('required'), Email('email')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])
    confirm_password = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password', message=u'密码输入不一致')])
