from flask_restful import Resource, Api
from . import api_blueprint
from flasky.auth.models import db, User, Post, Comment
from flask_restful import reqparse
from flask_login import current_user, login_required
from flask import request, jsonify


class PostResource(Resource):
    def get(self, post_id):
        current_post = Post.query.filter_by(id=post_id).first()
        if current_post:
            return {'id': current_post.id, 'title': current_post.title, 'content': current_post.content,
                    'create_time': current_post.create_time.timestamp(),
                    'user_id': current_post.user_id, 'message': 'OK'}, 200
        else:
            return {'message': "No content"}, 204


parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help=u'文章名称', required=True)
parser.add_argument('content', type=str, help=u'文章内容', required=True)

post_page_parse = reqparse.RequestParser()
post_page_parse.add_argument('page', type=int, required=False)
post_page_parse.add_argument('page_size', type=int, required=False)


class Posts(Resource):
    def post(self):
        """
        创建文章

        :param post_id: 文章 id
        :return: 创建成功返回 204
        """
        args = parser.parse_args()
        post_ = Post()
        post_.user_id = current_user.id
        post_.title = args['title']
        post_.content = args['content']

        db.session.add(post_)
        db.session.commit()

        return {'message': 'Created'}, 201

    def get(self):
        args = post_page_parse.parse_args()

        page = args['page']
        if page is None:
            page = 1
        page_size = args['page_size']
        if page_size is None or page_size > 20:
            page_size = 10
        size = Post.query.count()
        posts = Post.query.filter_by().order_by(Post.create_time.desc()).limit(page_size).offset((page - 1) * page_size)
        return {'size': size, 'data': [{'id': post.id, 'title': post.title, 'content': post.title} for post in posts]}


comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', type=str, help=u'评论内容', required=True)


@api_blueprint.route('/comments/post/<int:post_id>', methods=['POST'])
@login_required
def comment_to_post(post_id):
    comment = Comment()
    if not request.json:
        raise AttributeError('content should not none')

    comment.content = request.json['content']
    comment.post_id = post_id
    comment.from_user_id = current_user.id

    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Created"}), 204


post_api = Api(api_blueprint)
post_api.add_resource(PostResource, '/posts/<int:post_id>')
post_api.add_resource(Posts, '/posts')
