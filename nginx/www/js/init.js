// Initalize mopdule
var app = angular.module('myApp', []);

/**
 Angular app dierctive for attribute on-error whereas if the src attribute fail
 to load, then attribute src is replcaed by on-error's attribute vakue
*/
app.directive('onError', function()
{
    return {
        restrict: 'A',
        link: function(scope, element, attr)
        {
            element.on('error', function()
            {
                element.attr('src', attr.onError);
            })
        }
    }
})