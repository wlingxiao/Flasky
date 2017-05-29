var app = angular.module('app', ['ngMessages']);

var equalTo = function () {
    return {
        require: 'ngModel',
        link: function (scope, element, attributes, ngModel) {
            ngModel.$validators.equalTo = function (modelValue) {
                return scope.password === modelValue;
            };

            scope.$watch('password', function () {
                ngModel.$validate();
            })
        }
    }
};

var validateEmailExist = function ($http, $q) {
    return {
        require: 'ngModel',
        link: function (scope, element, attributes, ngModel) {
            ngModel.$asyncValidators.validateEmailExist = function (modelValue, viewValue) {
                var validateEmailUrl = 'validate_email/';

                return $http({
                    method: 'POST',
                    url: validateEmailUrl + modelValue,
                    headers: {'X-CSRFToken': $('#csrf_token').val()}

                }).then(function (response) {
                    if (response.data['code'] === 200) {
                        return true
                    } else {
                        return $q.reject(response['msg'])
                    }
                })['catch'](function (response) {
                    return $q.reject('请求错误');
                })
            }
        }
    }
};

var validateUsernameExist = function ($http, $q) {
    return {
        require: 'ngModel',
        link: function (scope, element, attributes, ngModel) {
            ngModel.$asyncValidators.validateUsernameExist = function (modleValue, viewValue) {
                var validateUsernameUrl = 'validate_username/';

                return $http({
                    method: 'POST',
                    url: validateUsernameUrl + modleValue,
                    headers: {'X-CSRFToken': $('#csrf_token').val()}
                }).then(function (response) {
                    if (response.data['code'] === 200) {
                        return true;
                    } else {
                        return $q.reject(response['msg']);
                    }
                })['catch'](function (response) {
                    return $q.reject('请求错误')
                });
            }
        }
    }
};

app.directive('validateUsernameExist', validateUsernameExist);
app.directive('validateEmailExist', validateEmailExist);
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