define('postController', function () {
    return function ($scope, $http, $httpParamSerializerJQLike) {

        $http.get('/post/show_post/1').then(function (response) {
            var data = response['data'];
            if (data && data['code'] === 200) {
                var postBody = {};

                postBody['id'] = data['id'];
                postBody['title'] = data['title'];
                postBody['content'] = data['content'];
                postBody['create_time'] = data['create_time'];
                postBody['user_id'] = data['user_id'];

                $scope.postBody = postBody;

                return $http.get('/post/comment/1')
            }
        }).then(function (response) {
            var data = response['data'];
            if (data && data['code'] === 200) {
                var comments = [];
                var commentData = data['data'];
                for (var index = 0; index < commentData.length; index++) {
                    comments.push({
                        'id': commentData[index]['id'],
                        'content': commentData[index]['content'],
                        'createDate': commentData[index]['create_date'],
                        'fromUserId': commentData[index]['from_user_id'],
                        'fromUserName': commentData[index]['from_user_name'],
                        'toUserId': commentData[index]['to_user_id'],
                        'toUserName': commentData[index]['to_user_name'],
                        'toCommentId': commentData[index]['to_comment_id'],
                        'toCommentContent': commentData[index]['to_comment_content'],
                        'toCommentCreateTime': commentData[index]['to_comment_create_time'],
                        'postId': commentData[index]['post_id']
                    })
                }
                $scope.comments = comments;
            }
        });

        $scope.commitComment = function () {
            var data = {content: $scope.commentToUserContent};

            $http({
                method: 'POST',
                url: '/post/comment_to_post/1',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                data: $httpParamSerializerJQLike(data)
            }).then(function (response) {
                var data = response['data'];
                console.log(data);
            })
        };

        $scope.commitCommentToUser = function (commentId) {

            var v = $scope;
        }
    }
});