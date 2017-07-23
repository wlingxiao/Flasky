from flask_restful import Resource, Api
from . import api_blueprint
from flasky.auth.models import db, User, Post, Comment
from flask_restful import reqparse
from flask_login import current_user, login_required


class PostResource(Resource):
    @login_required
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


class Posts(Resource):
    @login_required
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


comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', type=str, help=u'评论内容', required=True)


class CommentPostResource(Resource):
    @login_required
    def post(self, post_id):
        args = comment_parser.parse_args()

        comment = Comment()
        comment.content = args['content']
        comment.post_id = post_id
        comment.from_user_id = current_user.id

        db.session.add(comment)
        db.session.commit()

        return {'message': 'Created'}, 204


session_api = Api(api_blueprint)
session_api.add_resource(PostResource, '/posts/<int:post_id>')
session_api.add_resource(Posts, '/posts')
session_api.add_resource(CommentPostResource, '/comments/post/<int:post_id>')
