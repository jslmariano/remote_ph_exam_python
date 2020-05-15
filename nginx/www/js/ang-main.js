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

// Initalize Controller
app.controller('MainController', function($scope, $http, $window)
{
    // COMMON
    $scope.search_params = {};
    $scope.businesses = [];
    $scope.business_reviews = [];

    // cooredinates of MANILA!
    $scope.search_params.longtitude = '14.6091';
    $scope.search_params.latitude = '121.0223';

    // Statuses
    $scope.STATUS_LOADING = 1;
    $scope.STATUS_DONE = 0;

    // Statuses contaners
    $scope.statuses = {}
    $scope.statuses.search = 0
    $scope.statuses.search_display = "Search"
    $scope.statuses.reviews = 0

    /**
     * Creates a toast option.
     */
    $scope.create_toast_option = function() {
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": false,
          "progressBar": false,
          "positionClass": "toast-bottom-right",
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "300",
          "hideDuration": "1000",
          "timeOut": "5000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        }
    }

    /**
     * Shows the warning.
     *
     * @param      {<string>}  message  The message
     */
    $scope.show_warning = function(message) {
        toastr["warning"](message, "Mehhh...")
    }

    /**
     * Shows the error.
     *
     * @param      {<string>}  message  The message
     */
    $scope.show_error = function(message) {
        toastr["error"](message, "Oh My!")
    }

    /**
     * Sets the search status.
     *
     * @param      {<int>}  status  The status
     */
    $scope.set_search_status = function(status) {
        if (status == $scope.STATUS_LOADING) {
            $scope.statuses.search = $scope.STATUS_LOADING
            $scope.statuses.search_display = "Searching"
        }
        else {
            $scope.statuses.search = $scope.STATUS_DONE
            $scope.statuses.search_display = "Search"
        }
    }

    /**
     * Sets the reviews status.
     *
     * @param      {<int>}  status  The status
     */
    $scope.set_reviews_status = function(status) {
        if (status == $scope.STATUS_LOADING) {
            $scope.statuses.reviews = $scope.STATUS_LOADING
        }
        else {
            $scope.statuses.reviews = $scope.STATUS_DONE
        }
    }

    /**
     * Search and fetch business names
     */
    $scope.search_name = function()
    {
        $scope.set_search_status(1)
        $http(
            {
                method: "GET",
                url: "/api/v1/yelp/business/search",
                params: $scope.search_params
            })
            .then(function success(response)
            {
                console.log(response);
                $scope.businesses = response.data.business_search.businesses;
                $scope.business_reviews = [];
                $scope.set_search_status(0)
            }, function error(response)
            {
                console.log(response);
                $scope.businesses = [];
                $scope.set_search_status(0)
                $scope.show_error("Something gone wrong can you please try again?")
            });
    }

    /**
     * Fetch business reviews
     */
    $scope.fetch_reviews = function($event)
    {
        // Clear reviews
        $scope.business_reviews = [];

        // Do not proceed while soul searching
        if ($scope.statuses.search == $scope.STATUS_LOADING) {
            return false;
        }

        // Do not fetch if no review
        review_count = $event.currentTarget.dataset.review_count
        if (parseInt(review_count) <= 0)
        {
            return false;
        }

        business_datas = {}
        business_datas['alias'] = $event.currentTarget.dataset.alias
        business_datas['business_id'] = $event.currentTarget.dataset.business_id

        // Switch api mode
        mode_api = "/api/v1/yelp/business/scrape_reviews_page"
        url_params = $scope.get_params(window.location.href)
        if (url_params.hasOwnProperty('mode'))
        {
            if (url_params['mode'] == "yelp_xhr")
            {
                mode_api = "/api/v1/yelp/business/scrape_reviews_api"
            }
            else if (url_params['mode'] == "yelp_api")
            {
                mode_api = "/api/v1/yelp/business/reviews"
            }
        }

        $scope.set_reviews_status(1);
        $http(
            {
                method: "GET",
                url: mode_api,
                params: business_datas
            })
            .then(function success(response)
            {
                console.log(response);
                $scope.business_reviews = response.data.business_reviews.reviews;
                $scope.set_reviews_status(0);
            }, function error(response)
            {
                console.log(response);
                $scope.business_reviews = [];
                $scope.set_reviews_status(0);
                $scope.show_error("Something gone wrong can you please try again?")
            });
    }

    /**
     * Get the URL parameters
     * source: https://css-tricks.com/snippets/javascript/get-url-variables/
     * @param  {String} url The URL
     * @return {Object}     The URL parameters
     */
    $scope.get_params = function(url)
    {
        var params = {};
        var parser = document.createElement('a');
        parser.href = url;
        var query = parser.search.substring(1);
        var vars = query.split('&');
        for (var i = 0; i < vars.length; i++)
        {
            var pair = vars[i].split('=');
            params[pair[0]] = decodeURIComponent(pair[1]);
        }
        return params;
    };

});
