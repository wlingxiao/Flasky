define('commentToUserDirective', [], function () {
    return function () {
        return {
            replace: true,
            scope: false,
            restrict: 'E',
            templateUrl: '/static/post/comment_to_user.html',
            controller: function ($scope, $http) {
                $scope.commitCommentToUser2 = function (commentId) {
                    $scope.commentToUserContent = $('#commentToUserContent').val();
                    if (!$scope.commentToUserContent) {
                        console.log('no input');
                        return;
                    }
                    var data = {content: $scope.commentToUserContent, 'post_id': 1};
                    $http({
                        method: 'POST',
                        url: '/post/comment_to_user/' + commentId,
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        data: $httpParamSerializerJQLike(data)
                    }).then(function (response) {
                        var data = response['data'];
                        console.log(data)
                    })['catch'](function (response) {
                        var a = response
                    })
                };
            }
        }
    }
});