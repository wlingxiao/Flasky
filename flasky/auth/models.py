from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column('password', db.String(200))

    @property
    def password(self):
        raise AttributeError(u'Cannot not read password')

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def verify_password(self, password):
        assert password
        return check_password_hash(self._password, password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id
