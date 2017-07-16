from flask_restful import Resource, Api
from flask import jsonify
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf import FlaskForm as Form
from . import api_blueprint
from flasky.auth.models import User

from email.utils import parseaddr
from flask_login import LoginManager, login_required, login_user, current_user

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class LoinForm(Form):
    username_or_email = StringField(u'用户名或邮箱', validators=[DataRequired('required')])
    password = PasswordField(u'密码', validators=[DataRequired('required')])


def check_email(input_email):
    """ 判断字符串是否为邮箱 """

    return '@' in parseaddr(input_email)[1]


class SessionResource(Resource):
    def post(self):
        form = LoinForm()

        if form.validate_on_submit():
            username_or_email = form.username_or_email.data
            if check_email(username_or_email):
                request_login_user = User.query.filter_by(email=username_or_email).first()
                if request_login_user:
                    if request_login_user.verify_password(form.password.data):
                        login_user(request_login_user)
                        return {'msg': u'Created'}, 201
                    else:
                        return {'msg': u'密码错误'}, 400
                else:
                    return {'msg': u'该邮箱未注册'}, 404
            else:
                request_login_user = User.query.filter_by(username=username_or_email).first()
                if request_login_user:
                    if request_login_user.verify_password(form.password.data):
                        login_user(request_login_user)
                        return {'msg': u'Created'}, 201
                    else:
                        return {'msg': u'密码错误'}, 400
                else:
                    return {'msg': u'该用户名未注册'}, 404
        return {'msg': 'Bad Request'}, 400

    def delete(self):
        pass


session_api = Api(api_blueprint)
session_api.add_resource(SessionResource, '/sessions')
