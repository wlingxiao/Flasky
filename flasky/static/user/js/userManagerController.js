define('userManagerController', ['datepickerUtil', 'jquery'], function (datepickerUtil, $) {

    return function ($scope, userManagerAjaxService) {
        $scope.pageChanged = function () {
            var queryParm = {
                username: $scope.username,
                email: $scope.email,
                'sign_up_time_start': $('#sign-up-time-start').val(),
                'sign_up_time_end': $('#sign-up-time-end').val(),
                'last_visit_time_start': $('#last-login-time-start').val(),
                'last_visit_time_end': $('#last-login-time-end').val(),
                'page': $scope.currentPage,
                'page_size': 10
            };

            userManagerAjaxService.loadAllUsers(queryParm)
                .then(function (response) {
                    transformUsers(response)
                })
        };

        userManagerAjaxService.loadAllUsers().then(function (response) {
            transformUsers(response);
        });

        function transformUsers(response) {
            var data = response['data'];
            if (data) {
                if (data['code'] === 200) {
                    $scope.totalItems = data['size'];
                    var responseUsers = data['data'];
                    $scope.totalPage = parseInt($scope.totalItems / 10) + 1;
                    var users = [];
                    for (var i = 0; i < responseUsers.length; i++) {
                        var item = responseUsers[i];
                        users.push({
                            id: item['id'],
                            username: item['username'],
                            email: item['email'],
                            signUpTime: item['sign_up_time'],
                            lastVisitTime: item['last_visit_time']
                        })
                    }

                    $scope.users = users;
                }
            }
        }

        $scope.searchUser = function () {
            $scope.currentPage = 1;
            var queryParm = {
                username: $scope.username,
                email: $scope.email,
                'sign_up_time_start': $('#sign-up-time-start').val(),
                'sign_up_time_end': $('#sign-up-time-end').val(),
                'last_visit_time_start': $('#last-login-time-start').val(),
                'last_visit_time_end': $('#last-login-time-end').val()
            };

            userManagerAjaxService.loadAllUsers(queryParm)
                .then(function (response) {
                    transformUsers(response)
                })
        };

        $scope.resetSearch = function () {
            $scope.currentPage = 1;
            $scope.username = '';
            $scope.email = '';
            datepickerUtil.clearDateRanger();
            userManagerAjaxService.loadAllUsers()
                .then(function (response) {
                    transformUsers(response)
                })
        };
    }
});