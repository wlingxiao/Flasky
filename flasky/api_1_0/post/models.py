# -*- coding: utf-8 -*-
from datetime import datetime
from flasky.api_1_0.db import db


class Post(db.Model):
    """ Post """

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    content = db.Column(db.String(1000))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', back_populates='post')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user')


class Comment(db.Model):
    """ Comment """

    __tablename__ = 'comment'

    id = db.Column(db.INT, primary_key=True)
    content = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.now)
    # 该评论用户 ID
    from_user_id = db.Column(db.Integer)
    from_user_name = db.Column(db.String(80))
    # 评论目标用户 ID若没有则为空
    to_user_id = db.Column(db.Integer)
    to_user_name = db.Column(db.String(80))
    # 评论的评论ID，若没有则以下三列为空
    to_comment_id = db.Column(db.Integer)
    to_comment_content = db.Column(db.Text)
    to_comment_create_time = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')
