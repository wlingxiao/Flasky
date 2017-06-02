define('viewUserDirective', [], function () {
    return function () {
        return {
            replace: true,
            restrict: 'E',
            templateUrl: '/static/user/view_user.html'
        }
    }
});
