function updateTimer(bus_info, distance){
    console.log("updateTimer called");
    $.ajax({
        type : 'GET',
        contentType : 'application/json',
        url : $SCRIPT_ROOT + '_get_arrival_time',
        dataType : 'json',
        data : { buses: bus_info},
        success : function(data){
            console.log("number of buses: " + data["number"]);
            var walkingTime = distance * 60;
            var hms, time, seconds, timer_id;
            $('#nobuses').empty();
            $('.countdown-timers').empty();
            $('#0').timer('remove');
            $('#1').timer('remove');
            $('#2').timer('remove');
            $('#3').timer('remove');
            $('#4').timer('remove');
            $('#5').timer('remove');

            timer_id = 0;
            if(data["number"] > 0) {
                for (var i = 0; i < data["number"]; i++) {
                    var busDataId = "busData" + i;
                    console.log("Bus id: " + data["buses"][i]["id"])
                    hms = data["buses"][i]["formattedTime"];
                    if (hms != -1) {
                        time = hms.split(':');
                        seconds = (+time[0]) * 60 * 60 + (+time[1]) * 60 + (+time[2]) - walkingTime;
                        if (seconds <= 0) {
                            var this_id = i;
                            $('#' + i).timer('remove');
                            $('#nobuses').append("<p>You won't catch bus " + data["buses"][i]["id"] + "</p><i class='fa fa-frown-o' aria-hidden='true'></i>");
                        }
                        else {
                            var last_id = $('div[class="childTimer"]:last').attr('id');
                            console.log("last id: " + last_id);
                            if (!last_id) {
                                // create a new div and append it to countdown-timers w/ id=0
                                $('.countdown-timers').append('<div id="busData0"><i class="fa fa-bus fa-2" aria-hidden="true"></i> Bus #'+ data["buses"][i]["id"] +'</div>')
                                $('div[class="countdown-timers"]:last').append('<div id="0" class="childTimer"></div>');
                                $('#0').timer({
                                    countdown: true,
                                    duration: seconds,
                                    callback: function () {
                                        $('#0').timer('remove');
                                    }
                                });
                                console.log("no timers, appending to countdown-timers div");
                            }
                            else {
                                $('.countdown-timers:last').append('<div id="'+ busDataId + '"><i class="fa fa-bus fa-2" aria-hidden="true"></i> Bus #'+ data["buses"][i]["id"] +'</div>')
                                $('div[class="countdown-timers"]:last').append('<div id="' + timer_id + '" class="childTimer">' + data["buses"][i]["id"] + '</div>');
                                $('#' + timer_id).timer({
                                    countdown: true,
                                    duration: seconds,
                                    callback: function () {
                                        $('#' + timer_id).timer('remove');
                                    }
                                });
                                console.log('append to previous timer');
                            }
                            timer_id = timer_id + 1;
                        }
                    }
                    else {
                        $('#nobuses').append("<h3><i class='fa fa-frown-o' aria-hidden='true'></i> Bus " + data["buses"][i]["id"] + " is past your stop.</h3>");
                        console.log('invalid bus found');
                        continue;
                    }
                }
            }
            else {
                $('#nobuses').append("<h3><i class='fa fa-frown-o' aria-hidden='true'></i> There are no buses running on your route at the moment</h3>");
                console.log("no buses running");
            }
        }, error : function(xhr){
            console.log("An error occurred: " + xhr.status + " " + xhr.statusText);
            $("#nobuses").empty();
            $("#timer").empty();
            $("#nobuses").append("<h3><i class='fa fa-frown-o' aria-hidden='true'></i> All buses are currently past your stop</h3>");
            }
    });
};

// Reads current value of timer and POSTs to server to update preferences file
// Called every 30 seconds
function timeLeft(){
    var time;

    if( $('#0').is(':empty') ) {
        time = -1;
    }
    else {
        time = $('#0').val();

    }
    $.post('_update_preferences', { timeLeft: time},
        function(data){
            console.log(data);
        });
};