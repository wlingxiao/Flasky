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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
