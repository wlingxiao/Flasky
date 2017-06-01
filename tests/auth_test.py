from flasky import create_app as flasky_create_app
import json
from flasky.auth.models import db, User
from flask_testing import TestCase
from datetime import datetime


class AuthTest(TestCase):
    def create_app(self):
        self.app = flasky_create_app(dict(
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False,
            TESTING=True,
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        ))
        return self.app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        AuthTest.save_user()
    
    def delete_all_users(self):
        """ Delete all users in test database """

        User.query.delete()
    
    @staticmethod
    def save_user():
        test_user = User(username='test', email='test@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(test_user)
        db.session.commit()

    def test_validate_email_exist(self):
        response = self.client.post('/auth/validate_email/' + 'test@test.com')
        self.assertEqual(400, json.loads(response.data)['code'])

    def test_validate_email_not_exist(self):
        response = self.client.post('/auth/validate_email/' + 'not_exist@test.com')
        self.assertEqual(200, json.loads(response.data)['code'])

    def test_validate_username_exist(self):
        response = self.client.post('/auth/validate_username/' + 'test')
        self.assertEqual(400, json.loads(response.data)['code'])

    def test_validate_username_not_exist(self):
        response = self.client.post('/auth/validate_username/' + 'not_exist')
        self.assertEqual(200, json.loads(response.data)['code'])
    
    def test_sign_up_but_usename_exist(self):
        """ 注册用户时用户名已存在 """
        
        self.delete_all_users()
        
        user = User(username='sign_up_but_usename_exist', email='sign_up_but_usename_exist@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/sign_up', data=dict(
            username='sign_up_but_usename_exist',
            email='sign_up_but_usename_exist@test.com',
            password='111111',
            confirm_password='111111'
        ))
        
        self.assertEqual(400, json.loads(response.data)['code'])
        
    def test_sign_up_but_email_exist(self):
        """ 注册用户时邮箱已存在 """
        
        self.delete_all_users()
        
        user = User(username='sign_up_but_email_exist', email='sign_up_but_email_exist@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/sign_up', data=dict(
            username='sign_up_but_email_exist',
            email='sign_up_but_email_exist@test.com',
            password='111111',
            confirm_password='111111'
        ))
        
        self.assertEqual(400, json.loads(response.data)['code'])
       
    def test_sign_up_success(self):
        """ 注册用户成功 """
        
        self.delete_all_users()
        
        response = self.client.post('/auth/sign_up', data=dict(
            username='sign_up_success',
            email='sign_up_success@test.com',
            password='111111',
            confirm_password='111111'
        ))
        
        self.assertEqual(201, json.loads(response.data)['code'])
        
        saved_user = User.query.filter(User.username == 'sign_up_success').first()
        self.assertIsNotNone(saved_user)
    
    def test_login_emial_wrong_password(self):
        """ 使用邮箱登录，密码错误 """
        
        self.delete_all_users()
        user = User(username='login_emial_wrong_password', email='login_emial_wrong_password@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data=dict(
            username_or_email='login_emial_wrong_password@test.com',
            password='111112'
        ))
        
        self.assertEqual(400, json.loads(response.data)['code'])
        
    def test_login_username_wrong_password(self):
        """ 使用用户名登录，密码错误 """
        
        self.delete_all_users()
        user = User(username='login_emial_wrong_password', email='login_emial_wrong_password@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data=dict(
            username_or_email='login_emial_wrong_password',
            password='111112'
        ))
        
        self.assertEqual(400, json.loads(response.data)['code'])
    
    def test_login_emial_not_exist(self):
        """ 使用邮箱登录，邮箱未注册 """
        
        self.delete_all_users()
        user = User(username='login_emial_wrong_password', email='login_emial_wrong_password@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data=dict(
            username_or_email='login_emial_wrong_password_1@test.com',
            password='111111'
        ))
        
        self.assertEqual(404, json.loads(response.data)['code'])
        
        
    def test_login_usename_not_exist(self):
        """ 使用用户名登录，用户名未注册 """
        
        self.delete_all_users()
        user = User(username='login_emial_wrong_password', email='login_emial_wrong_password@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data=dict(
            username_or_email='login_emial_wrong_password_1',
            password='111112'
        ))
        
        self.assertEqual(404, json.loads(response.data)['code'])
    
    def test_login_email_success(self):
        """ 使用邮箱登录成功 """
        
        self.delete_all_users()
        user = User(username='login_emial_right_password', email='login_emial_right_password@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data=dict(
            username_or_email='login_emial_right_password@test.com',
            password='111111'
        ))
        
        self.assertEqual(200, json.loads(response.data)['code'])
        
    def test_login_usename_success(self):
        """ 使用用户名登录成功 """
        
        self.delete_all_users()
        user = User(username='login_usename_right_password', email='login_usename_right_password_1@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data=dict(
            username_or_email='login_usename_right_password',
            password='111111'
        ))
        
        self.assertEqual(200, json.loads(response.data)['code'])
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
