// A $( document ).ready() block.
$( document ).ready(function() {

    // Toggle active class in business names
    $(document).on('click', '.business-names-item', function(){
        $('.business-names-item').removeClass('active');
        $(this).addClass('active');
    });

});