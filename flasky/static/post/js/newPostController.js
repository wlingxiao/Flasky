define('newPostController', function () {
    return function ($scope, $http, $httpParamSerializerJQLike) {
        $scope.submitPost = function () {
            var title = $scope.title;
            var content = $scope.content;

            var data = {title: title, content: content};

            $http({
                method: 'POST',
                url: '/post/create_post',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                data: $httpParamSerializerJQLike(data)
            }).then(function (response) {
                var data = response['data'];
                if (data && data['code'] === 201) {

                }
            })['catch'](function (error) {

            })
        }
    }
});