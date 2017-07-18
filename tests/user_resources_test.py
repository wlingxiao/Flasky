from flasky import create_app as flasky_create_app
import json
from flasky.auth.models import db, User
from flask_testing import TestCase
from datetime import datetime

URL_PREFIX = '/api/v1'


class UserResourcesTest(TestCase):
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

    def save_user(self, user):
        db.session.add(user)
        db.session.commit()

    def test_validate_email_exist(self):
        test_user = User(username='test', email='test@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        self.save_user(test_user)

        response = self.client.get(URL_PREFIX + '/users/email/' + 'test@test.com')
        self.assertEqual(302, response.status_code)

    def test_validate_username_exist(self):
        test_user = User(username='test', email='test@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        self.save_user(test_user)

        response = self.client.get(URL_PREFIX + '/users/username/' + 'test')
        self.assertEqual(302, response.status_code)

    def test_get_user_by_id(self):
        test_user = User(username='test', email='test@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        self.save_user(test_user)

        response = self.client.get(URL_PREFIX + '/users/' + '1')
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
