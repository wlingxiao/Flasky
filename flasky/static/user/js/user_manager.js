'use strict'
var app = angular.module('app', []);

app.service('userManagerAjaxService', function ($http, $httpParamSerializerJQLike) {
    this.loadAllUsers = function (queryParam) {
        var loadAllUsersUrl = 'load_all_user';
        return $http({
            method: 'GET',
            url: loadAllUsersUrl,
            params: queryParam
        })
    }
});

app.controller('userManagerController', function ($scope, userManagerAjaxService) {
    userManagerAjaxService.loadAllUsers().then(function (response) {
        transformUsers(response)
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
        var queryParm = {
            username: $scope.username,
            email: $scope.email,
            'sign_up_time': $scope.signUpTime,
            'last_visit_time': $scope.lastVisitTime
        };

        userManagerAjaxService.loadAllUsers(queryParm)
            .then(function (response) {
                transformUsers(response)
            })
    };

    $scope.resetSearch = function () {
        $scope.username = null;
        $scope.email = null;
        $scope.signUpTime = null;
        $scope.lastVisitTime = null;

        userManagerAjaxService.loadAllUsers()
            .then(function (response) {
                transformUsers(response)
            })
    };
});