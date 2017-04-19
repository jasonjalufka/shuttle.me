function updateTimer(bus_info, distance){
    $.ajax({
        type : 'GET',
        contentType : 'application/json',
        url : $SCRIPT_ROOT + '_get_arrival_time',
        dataType : 'json',
        data : { buses: bus_info},
        success : function(data){
            console.log("number of buses: " + data["number"]);
            var walkingTime = distance * 60;
            var hms, time, seconds, id;
            $('.countdown-timers').empty();

            for(var i = 0; i < data["number"]; i++) {
                hms = data["buses"][i]["formattedTime"];
                if (hms != -1) {
                    time = hms.split(':');
                    seconds = (+time[0]) * 60 * 60 + (+time[1]) * 60 + (+time[2]) - walkingTime;
                    id = 0;
                    var last_id = $('div[class="countdown-timers"]:last').attr('id');
                    console.log(last_id);
                    if(last_id == "timers"){
                        // create a new div and append it to countdown-timers w/ id=0
                        $('div[class="countdown-timers"]').append('<div id="0">');
                        console.log("not last id");
                    }
                    else{
                        $('div[class="countdown-timers"]:last').append('<div id="'+ id +'">');
                        console.log('append to last id')
                    }
                    CreateTimer(id, seconds);
                    id = id+1;
                }
                else {
                    console.log('invalid bus found');
                    continue;
                }
            };
        }, error : function(xhr){
            console.log("An error occurred: " + xhr.status + " " + xhr.statusText);
            $("#nobuses").empty();
            $("#timer").empty();
            $("#nobuses").append("<p>All buses are currently past your stop</p>");
            }
    });
};

// Reads current value of timer and POSTs to server to update preferences file
// Called every 30 seconds
function timeLeft(){
    var time;
    if( $('#timer').is(':empty') ) {
        time = -1;
    }
    else {
        time = $('#timer').val();
    }
    $.ajax({
    type: "POST",
    url: $SCRIPT_ROOT + '_update_preferences',
    data: time,
    success: console.log(time)
    });
};