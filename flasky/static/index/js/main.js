requirejs.config({
    paths: {
        'jquery': 'http://cdn.bootcss.com/jquery/3.2.1/jquery.min',
        'angular': 'http://cdn.bootcss.com/angular.js/1.6.4/angular.min',
        'domReady': 'http://cdn.bootcss.com/require-domReady/2.0.1/domReady.min',
        'bootstrap': 'http://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap'
    },
    shim: {
        'angular': {
            exports: 'angular'
        },
        'bootstrap': {
            exports: 'bootstrap',
            deps: ['jquery']
        }
    },
    deps: ['ng-bootstrap']
});

define('app', ['angular', 'indexController'],
    function (ng, indexController) {
        'use strict'
        var app = ng.module('app', []);
        app.controller('indexController', indexController);
        return app;
    });

/**
 * angular bootstrap
 */
define('ng-bootstrap', ['require', 'angular', 'app'], function (require, angular, app) {
    'use strict'

    require(['domReady!'], function (document) {
        angular.bootstrap(document, ['app'])
    })
});