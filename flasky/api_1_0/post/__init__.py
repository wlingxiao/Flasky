# -*- coding: utf-8 -*-
from flasky.api_1_0 import api as post

from flask import request, render_template, jsonify
from flasky.auth.models import db, User, Post, Comment
from flask_login import current_user, login_required


@post.route('/<int:post_id>')
def post_index(post_id):
    return render_template('/post/post.html', post_id=post_id)


@post.route('/show_post/<int:post_id>')
def show_post(post_id):
    current_post = Post.query.filter_by(id=post_id).first()
    if current_post:
        return jsonify({'id': current_post.id, 'title': current_post.title, 'content': current_post.content,
                        'create_time': current_post.create_time.strftime('%Y-%m-%d'), 'user_id': current_post.user_id,
                        'code': 200, 'msg': 'OK'})
    else:
        return jsonify({'code': 200})


@post.route('/load_all_posts')
def load_all_posts():
    posts = Post.query.order_by(Post.create_time.desc()).limit(10).offset(0)

    return jsonify({'code': 200, 'msg': 'OK', 'size': 20,
                    'data': [
                        {'id': per_post.id, 'title': per_post.title,
                         'content': per_post.content, 'create_time': per_post.create_time}
                        for per_post in posts
                        ]})


@post.route('/new_post')
def new_post():
    return render_template('/post/new_post.html')


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
    return jsonify({'code': 201, 'msg': 'Created'})


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


@post.route('/comment/<int:post_id>')
def post_comment(post_id):
    comment_ = Comment.query.filter_by(post_id=post_id).all()
    result = {
        'code': 200,
        'msg': 'OK',
        'size': 10,
        'data': [
            {
                'id': per_comment.id,
                'content': per_comment.content,
                'create_date': per_comment.create_date.strftime('%Y-%m-%d %H:%M'),
                'from_user_id': per_comment.from_user_id,
                'from_user_name': per_comment.from_user_name,
                'to_user_id': per_comment.to_user_id,
                'to_user_name': per_comment.to_user_name,
                'to_comment_id': per_comment.to_comment_id,
                'to_comment_content': per_comment.to_comment_content,
                'to_comment_create_time': per_comment.to_comment_create_time,
                'post_id': per_comment.post_id,
            } for per_comment in comment_
            ]
    }
    return jsonify(result)


@post.route('/comment_to_user/<comment_id>', methods=['POST'])
@login_required
def comment_to_user(comment_id):
    post_id = request.form['post_id']
    comment = Comment()
    comment.content = request.form['content']
    comment.post_id = post_id
    comment.from_user_id = current_user.id
    comment.from_user_name = current_user.username
    comment.to_comment_id = comment_id

    to_comment = Comment.query.filter_by(id=comment_id).first()
    if to_comment:
        comment.to_user_id = to_comment.from_user_id
        comment.to_user_name = to_comment.from_user_name
        comment.to_comment_create_time = to_comment.create_date
        comment.to_comment_content = to_comment.content
    else:
        raise AttributeError

    db.session.add(comment)
    db.session.commit()
    return '200'
