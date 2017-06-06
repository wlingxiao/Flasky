# -*- coding: utf-8 -*-
from flask import request
from . import post
from flasky.auth.models import db, User, Post, Comment
from flask_login import current_user, login_required


@post.route('/create_post', methods=['POST'])
@login_required
def create_post():
    title = request.form['title']
    content = request.form['content']

    post_ = Post()
    post_.user_id = current_user.id
    post_.title = title
    post_.content = content

    db.session.add(post_)
    db.session.commit()
    return '200'


@post.route('/comment_to_post/<post_id>', methods=['POST'])
@login_required
def comment_to_post(post_id):
    comment = Comment()
    comment.content = request.form['content']
    comment.post_id = post_id
    comment.from_user_id = current_user.id

    db.session.add(comment)
    db.session.commit()
    return '200'


@post.route('/comment_to_user/<to_user_id>', methods=['POST'])
@login_required
def comment_to_user(to_user_id):
    post_id = request.form['post_id']
    comment = Comment()
    comment.content = request.form['content']
    comment.post_id = post_id
    comment.from_user_id = current_user.id
    comment.to_user_id = to_user_id

    db.session.add(comment)
    db.session.commit()
    return '200'
