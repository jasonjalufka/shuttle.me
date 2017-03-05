/**
 * Created by Jason on 2/22/17.
 */
$( document ).ready(function() {
    console.log('ready!');

    $(document).ready(function(){
        $('.btn-left').css("background-color", "#25bbf0");
        $('.stop-select').show();
        $('.distance-select').hide();
        $('.alert-select').hide();
    });

    $('.btn-left').click(function () {
        $('.btn-left').css("background-color", "#25bbf0");
        $('.btn-mid').css("background-color", "rgba(255,255,255,0.7)");
        $('.btn-right').css("background-color", "rgba(255,255,255,0.7)");
        $('.stop-select').show();
        $('.distance-select').hide();
        $('.alert-select').hide();
    });

    $('.btn-mid, #stop-next').click(function () {
        $('.btn-left').css("background-color", "rgba(255,255,255,0.7)");
        $('.btn-mid').css("background-color", "#25bbf0");
        $('.btn-right').css("background-color", "rgba(255,255,255,0.7)");
        $('.stop-select').hide();
        $('.distance-select').show();
        $('#distanceInput').focus();
        $('.alert-select').hide();
    });

    $('.btn-right, #distance-next').click(function () {
        $('.btn-left').css("background-color", "rgba(255,255,255,0.7)");
        $('.btn-mid').css("background-color", "rgba(255,255,255,0.7)");
        $('.btn-right').css("background-color", "#25bbf0");
        $('.stop-select').hide();
        $('.distance-select').hide();
        $('.alert-select').show();
    });

});

