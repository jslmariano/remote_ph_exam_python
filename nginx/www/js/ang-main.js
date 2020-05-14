var app = angular.module('myApp', []);

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

app.controller('MainController', function($scope, $http)
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
                if (!response.data.business_search.businesses.length) {
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
        if (parseInt(review_count) <= 0) {
            $scope.business_reviews = [];
            return false;
        }

        business_alias = $event.currentTarget.dataset.alias
        $http(
            {
                // http://localhost/api/v1/yelp/business/reviews?alias=spiral-pasay-2
                method: "GET",
                url: "/api/v1/yelp/business/reviews",
                params: {'alias': business_alias}
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

    $scope.fetch_emotions = function($event)
    {
        business_alias = $event.currentTarget.dataset.alias
        $http(
            {
                // http://localhost/api/v1/yelp/business/reviews?alias=spiral-pasay-2
                method: "GET",
                url: "/api/v1/yelp/business/reviews",
                params: {'alias': business_alias}
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

});
