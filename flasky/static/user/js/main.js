/**
 * requirejs config init
 */
requirejs.config({
    paths: {
        'jquery': 'http://cdn.bootcss.com/jquery/3.2.1/jquery.min',
        'angular': 'http://cdn.bootcss.com/angular.js/1.6.4/angular.min',
        'domReady': 'http://cdn.bootcss.com/require-domReady/2.0.1/domReady.min',
        'datepicker': 'http://cdn.bootcss.com/bootstrap-datepicker/1.7.0-RC3/js/bootstrap-datepicker',
        'datepickerzhCN': 'http://cdn.bootcss.com/bootstrap-datepicker/1.7.0-RC3/locales/bootstrap-datepicker.zh-CN.min',
        'moment': 'http://cdn.bootcss.com/moment.js/2.18.1/moment.min',
        'uiBootstrap': 'http://cdn.bootcss.com/angular-ui-bootstrap/2.5.0/ui-bootstrap.min',
        'uiBootstrapTpls': 'http://cdn.bootcss.com/angular-ui-bootstrap/2.5.0/ui-bootstrap-tpls.min',
        'bootstrap': 'http://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap'
    },
    shim: {
        'angular': {
            exports: 'angular'
        },
        'datepickerzhCN': {
            exports: 'datepickerzhCN',
            deps: ['jquery', 'datepicker']
        },
        'datepicker': {
            exports: 'datepicker',
            deps: ['jquery', 'moment', 'bootstrap']
        },
        'uiBootstrap': {
            exports: 'uiBootstrap',
            deps: ['angular']
        },
        'uiBootstrapTpls': {
            exports: 'uiBootstrapTpls',
            deps: ['uiBootstrap']
        }
    },
    deps: ['ng-bootstrap']
});

/**
 * angular module init
 */
define('app', ['angular', 'userManagerController', 'userManagerAjaxService', 'uiBootstrap', 'uiBootstrapTpls'], function (ng, userManagerController, userManagerAjaxService) {
    'use strict'
    var app = ng.module('app', ['ui.bootstrap']);
    app.controller('userManagerController', userManagerController);
    app.service('userManagerAjaxService', userManagerAjaxService);
    return app;
});

/**
 * angular bootstrap
 */
define('ng-bootstrap', ['require', 'angular', 'app', 'datepickerUtil'], function (require, angular, app, datepickerUtil) {
    'use strict'

    require(['domReady!'], function (document) {
        datepickerUtil.initDatePicker()
        angular.bootstrap(document, ['app'])
    })
});
