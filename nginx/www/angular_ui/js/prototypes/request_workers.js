/**
 * SHOULD BE LOADED AFTER INIT.JS
 */


/**
 * Request Workers
 *
 * REFERRENCES for angulat $q and $http:
 * https://code.angularjs.org/1.4.2/docs/api/ng/service/$http#general-usage
 * https://code.angularjs.org/1.4.2/docs/api/ng/service/$q#the-promise-api
 *
 * In case of infamiliarity with javascritp prototype, just google it :)
 *
 * @class      RequestWorkers (name)
 * @param      {HTTP ANGULAR}    http    The http
 * @param      {HTTP Q PROMISE}  q       The quarter
 */
function RequestWorkers(http, q)
{
    this.http = http;
    this.q = q;
    this.workers = {};
    this.id = 0;
}

RequestWorkers.prototype.get_http = function()
{
    return this.http;
};

RequestWorkers.prototype.get_q = function()
{
    return this.q;
};

RequestWorkers.prototype.get_requests = function(request_name)
{
    if (!request_name)
    {
        return this.workers;
    }
    return this.workers[request_name];
};

RequestWorkers.prototype.create_request = function(request_name, url, params)
{
    if (this.workers.hasOwnProperty(request_name))
    {
        this.cancel_request(request_name);
        delete this.workers[request_name];
    }

    this.workers[request_name] = this.init_request(url, params);
    console.log("Request worker created for ", request_name);
    return this.workers[request_name];
};

RequestWorkers.prototype.cancel_request = function(request_name) {

    if (this.workers.hasOwnProperty(request_name))
    {
        console.log("Request worker cancelled for ", request_name, this.workers);
        this.workers[request_name].cancel('Cancel requested');
        delete this.workers[request_name];
    }
    return this;
};

RequestWorkers.prototype.init_request = function(url, params)
{
    var canceller = this.get_q()
        .defer();
    var is_cancelled = 0;
    var id = (this.id++);

    var cancel = function(reason)
    {
        canceller.resolve(reason);
        is_cancelled = 1;
    };

    var promise =
        this.get_http()
        .get(url,
        {
            timeout: canceller.promise,
            params: params
        })
        .then(function(response)
        {
            return response;
        });

    return {
        promise: promise,
        cancel: cancel,
        url: url,
        is_cancelled: is_cancelled
    };

};

/* Register Factory */
app.factory('request_workers', function($http, $q)
{
    x = new RequestWorkers($http, $q);
    return x;
});
