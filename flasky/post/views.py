# -*- coding: utf-8 -*-
from flask import request, render_template, jsonify
from . import post
from flasky.auth.models import db, User, Post, Comment
from flask_login import current_user, login_required


@post.route('/')
def post_index():
    return render_template('/post/post.html')


@post.route('/show_post/<post_id>')
def show_post(post_id):
    current_post = Post.query.filter_by(id=post_id).first()
    return jsonify({'id': current_post.id, 'title': current_post.title, 'content': current_post.content,
                    'create_time': current_post.create_time.strftime('%Y-%m-%d'), 'user_id': current_post.user_id,
                    'code': 200, 'msg': 'OK'})


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


@post.route('/comment/<post_id>')
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
                'to_user_id': per_comment.to_user_id,
                'post_id': per_comment.post_id
            } for per_comment in comment_
        ]
    }
    return jsonify(result)


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
