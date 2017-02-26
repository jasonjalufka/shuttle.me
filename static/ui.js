/**
 * Created by Jason on 2/22/17.
 */
$( document ).ready(function() {
    console.log('ready!');

    $(document).ready(function(){
        $('.stop-select').show();
        $('.distance-select').hide();
        $('.alert-select').hide();
    });

    $('.btn-left').click(function () {
        $('.stop-select').show();
        $('.distance-select').hide();
        $('.alert-select').hide();
    });

    $('.btn-mid').click(function () {
        $('.stop-select').hide();
        $('.distance-select').show();
        $('.alert-select').hide();
    });

    $('.btn-right').click(function () {
        $('.stop-select').hide();
        $('.distance-select').hide();
        $('.alert-select').show();
    });
});

