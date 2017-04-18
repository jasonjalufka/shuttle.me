function updateTimer(bus_info, distance){
    $.ajax({
        type : 'GET',
        contentType : 'application/json',
        url : $SCRIPT_ROOT + '_get_arrival_time',
        dataType : 'json',
        data : { buses: bus_info},
        success : function(data){
            var walkingTime = distance * 60;
            var hms, time, seconds, id;

            for(var i = 0; i < data["number"]; i++) {
                hms = data["buses"][i]["formattedTime"];
                if (hms != -1) {
                    time = hms.split(':');
                    seconds = (+time[0]) * 60 * 60 + (+time[1]) * 60 + (+time[2]) - walkingTime;
                    id = "timer" + i.toString();
                    console.log(id)
                    var hashtag_id = "'#"+id+"'";
                    console.log(hashtag_id);
                    $(hashtag_id).empty()
                    $('.countdown-timers').after("<div ></div>")
                    CreateTimer(id, seconds);
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