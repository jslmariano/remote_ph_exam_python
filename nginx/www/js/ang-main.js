var app = angular.module('myApp', []);


app.config(function($locationProvider)
{
    $locationProvider.html5Mode(
        {
            enabled: true,
            requireBase: false
        })
        .hashPrefix('!');
});

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

app.controller('MainController', function($scope, $http, $location, $window)
{
    $scope.search_params = {};
    $scope.businesses = [];
    $scope.business_reviews = [];

    //  MANILA!
    $scope.search_params.longtitude = '14.6091';
    $scope.search_params.latitude = '121.0223';

    $scope.search_name = function()
    {
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

                // reset views too
                if (!response.data.business_search.businesses.length)
                {
                    $scope.business_reviews = [];
                }
            }, function error(response)
            {
                console.log(response);
                $scope.businesses = [];
            });
    }

    $scope.fetch_reviews = function($event)
    {
        // Do not fetch if no review
        review_count = $event.currentTarget.dataset.review_count
        if (parseInt(review_count) <= 0)
        {
            $scope.business_reviews = [];
            return false;
        }

        business_datas = {}
        business_datas['alias'] = $event.currentTarget.dataset.alias
        business_datas['business_id'] = $event.currentTarget.dataset.business_id

        // Switch api mode
        default_api = "/api/v1/yelp/business/reviews"
        mode_api = default_api
        url_params = $scope.get_params(window.location.href)
        if (url_params.hasOwnProperty('mode'))
        {
            if (url_params['mode'] == "yelp_xhr")
            {
                mode_api = "/api/v1/yelp/business/scrape_reviews_api"
            }
            else if (url_params['mode'] == "yelp_page")
            {
                mode_api = "/api/v1/yelp/business/scrape_reviews_page"
            }
        }


        $http(
            {
                // http://localhost/api/v1/yelp/business/reviews?alias=spiral-pasay-2
                method: "GET",
                url: mode_api,
                params: business_datas
            })
            .then(function success(response)
            {
                console.log(response);
                $scope.business_reviews = response.data.business_reviews.reviews;
            }, function error(response)
            {
                console.log(response);
                $scope.business_reviews = [];
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
