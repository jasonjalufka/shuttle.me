function updateTimer(bus_info, distance){

    $.ajax({
        type : 'GET',
        contentType : 'application/json',
        url : $SCRIPT_ROOT + '_get_arrival_time',
        dataType : 'json',
        data : { buses: bus_info},
        success : function(data){
            console.log("Data: " + data['route']['formattedTime']);
            $("#timer").empty();
            CreateTimer("timer", data['route']['formattedTime'].split(':').reverse().reduce((prev, curr, i) => prev + curr*Math.pow(60, i), 0) - distance;
        }, error : function(data){
            $("#timer").empty();
            $("#nobuses").innerHTML = "All buses are currently past your stop"
        }
    });
}

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