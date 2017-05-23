requirejs.config({
    baseUrl: '../static/js',
    paths: {
        'angular': '/static/node_modules/angular/angular.min',
        'angular-animate': '/static/node_modules/angular-animate/angular-animate.min',
        'angular-route': '/static/node_modules/angular-route/angular-route.min',
        'angular-touch': '/static/node_modules/angular-touch/angular-touch.min',
        'dateformat': '/static/node_modules/dateformat/lib/dateformat',
        'domReady': '/static/node_modules/requirejs-domready/domReady',
        'highcharts': '/static/node_modules/highcharts/highcharts',
        'lodash': '/static/node_modules/lodash/lodash',
        'moment': '/static/node_modules/moment/min/moment.min',
        'rx': '/static/node_modules/rx/dist/rx.min',
        'ui-bootstrap': '/static/node_modules/angular-ui-bootstrap/dist/ui-bootstrap'
    },
    shim: {
        'angular': {
            exports: 'angular',
        },
        'angular-route': {
            deps: ['angular']
        },
        'ui-bootstrap': {
           deps: ['angular'],
           exports: 'ui-bootstrap'
       }
    },

    deps: ['./bootstrap']
});