var app = angular.module('app', ['ngMessages']);

var equalTo = function () {
    return {
        require: 'ngModel',
        link: function (scope, element, attributes, ngModel) {
            ngModel.$validators.equalTo = function (modelValue) {
                return scope.password === modelValue;
            }

            scope.$watch('password', function () {
                ngModel.$validate();
            })
        }
    }
};

app.directive('equalTo', equalTo);

var signUpAjaxService = function ($http, $httpParamSerializerJQLike) {

    this.signUp = function (signUpParam) {
        var signUpUrl = 'sign_up';

        var param = {
            'username': signUpParam['username'],
            'email': signUpParam['email'],
            'password': signUpParam['password'],
            'confirm_password': signUpParam['confirmPassword']
        };
        return $http({
            method: 'POST',
            url: signUpUrl,
            headers: {'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': signUpParam['csrfToke']},
            data: $httpParamSerializerJQLike(param)
        })
    }

};

app.service('signUpAjaxService', signUpAjaxService);

app.controller('loginController', function ($scope, signUpAjaxService) {
    $scope.submitSignUp = function () {
        var signUpParam = {
            username: $scope.username,
            email: $scope.email,
            password: $scope.password,
            confirmPassword: $scope.confirmPassword,
            csrfToke: $('#csrf_token').val()
        };

        signUpAjaxService.signUp(signUpParam)
            .then(function (data) {
                console.log(data)
            })
            ['catch'](function (data) {
            console.log(data)
        })

    }
});