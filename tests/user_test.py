from flasky import create_app as flasky_create_app
import json
from flasky.auth.models import db, User
from flask_testing import TestCase
from datetime import datetime, timedelta


class UserTest(TestCase):
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
        self.save_user()

    def delete_all_users(self):
        """ Delete all users in test database """

        User.query.delete()

    def save_user(self):
        """ 保存测试 User """

        test_user_1 = User(username='test1', email='test1@test.com', password='111111',
                           sign_up_time=datetime.now(),
                           last_visit_time=datetime.now())
        test_user_2 = User(username='test2', email='test2@test.com', password='111111',
                           sign_up_time=datetime.now(),
                           last_visit_time=datetime.now())
        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.commit()

    def test_load_all_user_without_param(self):
        response = self.client.get('/user/load_all_user')
        self.assertEqual(200, json.loads(response.data)['code'])
        self.assertEqual(2, json.loads(response.data)['size'])

    def test_load_all_user_filter_by_username(self):
        response = self.client.get('/user/load_all_user' + '?username=' + 'test1')
        self.assertEqual(200, json.loads(response.data)['code'])
        self.assertEqual(1, json.loads(response.data)['size'])

    def test_load_all_user_filter_by_email(self):
        response = self.client.get('/user/load_all_user' + '?email=' + 'test1@test.com')
        self.assertEqual(200, json.loads(response.data)['code'])
        self.assertEqual(1, json.loads(response.data)['size'])

    def test_load_all_user_filter_by_sign_up_time_start_and_end(self):
        """ 使用注册时间区间来筛选 User """

        self.delete_all_users()
        today = datetime.now()
        user_sign_up_time_start_and_end = User(username='sign_up_time_start_and_end',
                                               email='sign_up_time_start_and_end@test.com', password='111111',
                                               sign_up_time=today,
                                               last_visit_time=today)
        db.session.add(user_sign_up_time_start_and_end)
        db.session.commit()

        today_str = datetime.strftime(today, '%Y-%m-%d')
        response = self.client.get(
            '/user/load_all_user' + '?sign_up_time_start=' + today_str + '&sign_up_time_end=' + today_str)
        self.assertEqual(200, json.loads(response.data)['code'])
        self.assertEqual(1, json.loads(response.data)['size'])

    def test_load_all_user_filter_by_last_login_time_start_and_end(self):
        """ 使用最后访问时间区间来筛选 User """

        self.delete_all_users()
        today = datetime.now()
        user_last_login_time_start_and_end = User(username='last_login_time_start_and_end',
                                                  email='last_login_time_start_and_end@test.com', password='111111',
                                                  sign_up_time=today,
                                                  last_visit_time=today)
        db.session.add(user_last_login_time_start_and_end)
        db.session.commit()

        today_str = datetime.strftime(today, '%Y-%m-%d')
        response = self.client.get(
            '/user/load_all_user' + '?last_visit_time_start=' + today_str + '&last_visit_time_end=' + today_str)
        self.assertEqual(200, json.loads(response.data)['code'])
        self.assertEqual(1, json.loads(response.data)['size'])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
