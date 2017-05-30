define('userManagerController', ['datepickerUtil', 'jquery'], function (datepickerUtil, $) {

    return function ($scope, userManagerAjaxService) {

        $scope.totalItems = 64;
        $scope.currentPage = 4;

        $scope.setPage = function (pageNo) {
            $scope.currentPage = pageNo;
        };

        $scope.pageChanged = function () {
            $log.log('Page changed to: ' + $scope.currentPage);
        };

        $scope.maxSize = 5;
        $scope.bigTotalItems = 175;
        $scope.bigCurrentPage = 1;

        userManagerAjaxService.loadAllUsers().then(function (response) {
            transformUsers(response);
        });

        function transformUsers(response) {
            var data = response['data'];
            if (data) {
                if (data['code'] === 200) {
                    var responseUsers = data['data'];
                    var users = [];
                    for (var i = 0; i < responseUsers.length; i++) {
                        var item = responseUsers[i];
                        users.push({
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
            /*var queryParm = {
                username: $scope.username,
                email: $scope.email,
                'sign_up_time_start': $scope.signUpTimeStart,
                'sign_up_time_end': $scope.signUpTimeEnd,
                'last_visit_time_start': $scope.lastVisitTimeStart,
                'last_visit_time_end': $scope.lastVisitTimeEnd
            };*/

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