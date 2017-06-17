define('indexController', function () {
    return function ($scope, $http) {
        $http.get('/post/load_all_posts').then(function (response) {
            var data = response['data'];
            if (data && data['code'] === 200) {
                var posts = []
                var postsData = data['data']
                for (var i = 0; i < postsData.length; i++) {
                    posts.push({
                        id: postsData[i]['id'],
                        title: postsData[i]['title'],
                        content: postsData[i]['content'],
                        createTime: postsData[i]['create_time']
                    })
                }
                $scope.posts = posts;
            }

        })['catch'](function (error) {

        })
    }
});