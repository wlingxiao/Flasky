define('userManagerAjaxService', [], function () {
    return function ($http) {
        this.loadAllUsers = function (queryParam) {
            var loadAllUsersUrl = 'load_all_user';
            return $http({
                method: 'GET',
                url: loadAllUsersUrl,
                params: queryParam
            })
        }
    }
});