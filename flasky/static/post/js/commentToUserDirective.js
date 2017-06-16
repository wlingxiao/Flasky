define('commentToUserDirective', [], function () {
    return function () {
        return {
            replace: true,
            scope: false,
            restrict: 'E',
            templateUrl: '/static/post/comment_to_user.html',
            controller: function ($scope, $http) {

            }
        }
    }
});