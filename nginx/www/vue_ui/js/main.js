/**
 * Javascript Object exntendable
 */

/**
 * Order object for view
 */
OrderModel = {};
OrderModel.el = '#app';
OrderModel.data = function() {
    return {
        orders: [],
        api_orders: '/api/v1/customer/orders',
        order_pagination_instance: null,
        total_amount: 198.23,
        pagination: {
            totalPages: 1,
            startPage: 1,
            initiateStartPageClick: false,
            onPageClick: this.on_page,
        },
        datepicker_from: {
            format: 'yyyy-mm-dd',
        },
        datepicker_to: {
            format: 'yyyy-mm-dd',
        },
        els: {
            order_start_date: null
        },
        params: {
            page: 1,
            limit: 5,
            start_date: null,
            end_date: null,
            term: null,
            total_items: 0
        }
    };
}

/**
 * Methods declaratons
 */
OrderModel.methods = {}

OrderModel.methods.get_orders = function () {
    _params = this.get_url_params();
    axios.get(this.api_orders, {params: _params})
        .then(({data}) => {
            this.orders = data.items;
            this.total_amount = data.total_amount;
            this.pagination.startPage = parseInt(this.params.page);
            this.pagination.totalPages = Math.ceil(
                parseInt(data.total_count) / parseInt(this.params.limit)
            );
            this.params.total_items = data.total_count;
            this.update_pagination();
        })
        .catch((err) => {
            throw err;
            this.params.total_items = 0;
        })
}

OrderModel.methods.on_page = function(event, page) {
    this.params.page = page;
    this.get_orders();
}

OrderModel.methods.on_goto = function(event, page) {
    if (page > this.pagination.totalPages) {
        page = this.pagination.totalPages;
    }
    this.params.page = page;
    this.on_page(event, page);
}

OrderModel.methods.get_url_params = function() {
    _params = {}
    for (var key of Object.keys(this.params)) {
        _q = this.params[key];
        if (this.is_none(_q)) {}
        _params[key] = encodeURIComponent(_q)
    }
    return _params
}

OrderModel.methods.init_pagination = function() {
    this.$pagination_el = jQuery('.order-pagination');


    totalPages = this.pagination.totalPages;
    if (!totalPages) {
        this.pagination.totalPages = 1;
    }

    this.order_pagination_instance = this.$pagination_el.twbsPagination(
        this.pagination
    );
}

OrderModel.methods.update_pagination = function() {
    if (!this.$pagination_el) {
        this.init_pagination();
    }

    console.log(this.pagination.totalPages);
    totalPages = this.pagination.totalPages;
    if (!totalPages) {
        this.pagination.totalPages = 1;
    }

    this.$pagination_el.twbsPagination('destroy');
    this.$pagination_el.twbsPagination(jQuery.extend({}, this.pagination));
}

OrderModel.methods.init_datepicker = function() {

    let self = this;

    this.$dt_from_input = jQuery('.order-date-from');
    this.from_input = this.$dt_from_input.pickadate(this.datepicker_from)
    this.from_picker = this.from_input.pickadate('picker')

    this.$dt_to_input = jQuery('.order-date-to');
    this.to_input = this.$dt_to_input.pickadate(this.datepicker_to)
    this.to_picker = this.to_input.pickadate('picker')


    // Check if there’s a “from” or “to” date to start with and if so, set their
    // appropriate properties.
    if (this.from_picker.get('value')) {
        this.to_picker.set('min', this.from_picker.get('select'))
    }
    if (this.to_picker.get('value')) {
        this.from_picker.set('max', this.to_picker.get('select'))
    }

    // Apply event listeners in case of setting new “from” / “to” limits to have
    // them update on the other end. If ‘clear’ button is pressed, reset the
    // value.
    this.from_picker.on('set', function (event) {
        if (event.select) {
            self.to_picker.set('min', self.from_picker.get('select'))
            self.params.start_date = self.get_date_format(
                this.component.item.highlight.obj, self.datepicker_from.format
            )

        } else if ('clear' in event) {
            self.to_picker.set('min', false)
            self.params.start_date = null;
        }
        self.on_page(event, 1);
    })
    this.to_picker.on('set', function (event) {
        if (event.select) {
            self.from_picker.set('max', self.to_picker.get('select'))

            self.params.end_date = self.get_date_format(
                this.component.item.highlight.obj, self.datepicker_to.format
            )
        } else if ('clear' in event) {
            self.from_picker.set('max', false)
            self.params.end_date = null;
        }
        self.on_page(event, 1);
    })
}

OrderModel.methods.get_date_format = function(dateobj, format) {
    var year = dateobj.getFullYear();
    var month= ("0" + (dateobj.getMonth()+1)).slice(-2);
    var date = ("0" + dateobj.getDate()).slice(-2);
    var hours = ("0" + dateobj.getHours()).slice(-2);
    var minutes = ("0" + dateobj.getMinutes()).slice(-2);
    var seconds = ("0" + dateobj.getSeconds()).slice(-2);
    var day = dateobj.getDay();
    var months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];
    var dates = ["SUN","MON","TUE","WED","THU","FRI","SAT"];
    var converted_date = "";

    switch(format) {
        case "yyyy-mm-dd":
            converted_date = year + "-" + month + "-" + date;
            break;
        case "yyyy-mmm-dd ddd":
            converted_date = year + "-" + months[parseInt(month)-1] + "-" + date + " " + dates[parseInt(day)];
            break;
    }

    return converted_date;
}

OrderModel.methods.is_none = function(data) {
    if (data === null) return true;
    if (data === false) return true;

    if (typeof(data) == 'string') {
        if(data.trim() == '') return true;
    }

    if (typeof(data) == 'number') {
        if(!data) return true;
    }

    for(var key in data) {
        if(data.hasOwnProperty(key))
            return false;
    }
    return true;
}

/**
 * Mounted like onLoad()
 */
OrderModel.mounted = function() {
      this.get_orders();
      this.init_datepicker();
}

/**
 * Load Vue components
 */
for (const component in mdbvue) {
   Vue.component(component, mdbvue[component]);
}

/**
 * Initialize VUE
 * OBJECTS is defined above for proper organization
 */
var app = new Vue(OrderModel);

/**
 * Initialize Datatable
 */
jQuery(document).ready(function(){

});
