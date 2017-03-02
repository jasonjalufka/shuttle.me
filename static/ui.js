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

    $('.btn-mid, #stop-next').click(function () {
        $('.stop-select').hide();
        $('.distance-select').show();
        $('#distanceInput').focus();
        $('.alert-select').hide();
    });

    $('.btn-right, #distance-next').click(function () {
        $('.stop-select').hide();
        $('.distance-select').hide();
        $('.alert-select').show();
    });

});

