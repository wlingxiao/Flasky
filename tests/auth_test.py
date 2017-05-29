from unittest import TestCase
from flasky import create_app
import json
import tempfile
from flasky.auth.models import db, User
import os


class AuthTest(TestCase):
    def setUp(self):
        self.test_database_file = os.path.join(os.getcwd(), 'test.db')

        app = create_app(dict(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + self.test_database_file,
            WTF_CSRF_ENABLED=False,
            TESTING=True
        ))

        with app.app_context():
            db.create_all()
            test_user = User(username='test', email='test@test.com', password='111111')
            db.session.add(test_user)
            db.session.commit()

        self.client = app.test_client()

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
        if os.path.exists(self.test_database_file):
            os.remove(self.test_database_file)
