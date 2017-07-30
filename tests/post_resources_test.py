from flasky import create_app as flasky_create_app
import json
from flasky.auth.models import db, User, Post
from datetime import datetime
from flask_testing import TestCase

URL_PREFIX = '/api/v1'


class PostTest(TestCase):
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
        self.save_login_user()

    def login(self):
        pass

    def save_login_user(self):
        test_user = User(username='test', email='test@test.com', password='111111', sign_up_time=datetime.now(),
                         last_visit_time=datetime.now())
        db.session.add(test_user)
        db.session.commit()

        p = {'username_or_email': 'test', 'password': '111111'}
        self.client.post(URL_PREFIX + '/sessions', data=p)

    def save_post(self, post):
        db.session.add(post)
        db.session.commit()

    def test_create_post(self):
        p = {'title': 'test_title', 'content': 'test_content'}

        response = self.client.post(URL_PREFIX + '/posts', data=json.dumps(p), content_type="application/json")

        self.assertEqual(201, response.status_code)

    def test_load_post(self):
        post_ = Post()
        post_.id = 1
        post_.user_id = 1
        post_.title = "test"
        post_.content = "test@test.com"
        self.save_post(post_)
        response = self.client.get(URL_PREFIX + '/posts')

        self.assertEqual(200, response.status_code)

    def test_get_post_by_id(self):
        post_ = Post()
        post_.id = 1
        post_.user_id = 1
        post_.title = "test"
        post_.content = "test@test.com"
        self.save_post(post_)

        response = self.client.get(URL_PREFIX + '/posts' + '/1')
        self.assertEqual(200, response.status_code)

    def test_comment_to_post(self):
        """
        测试文章评论
        """

        post_ = Post()
        post_.id = 1
        post_.user_id = 1
        post_.title = "test"
        post_.content = "test@test.com"
        self.save_post(post_)

        response = self.client.post(URL_PREFIX + '/comments/post' + '/1', data=json.dumps({'content': 'test'}),
                                    content_type="application/json")
        self.assertEqual(204, response.status_code)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
