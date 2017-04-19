/**
 * Created by Jason on 4/10/17.
 */

// var Timer;
// var TotalSeconds;
//
// function CreateTimer(TimerID, Time) {
//     Timer = document.getElementById(TimerID);
//     TotalSeconds = Time;
//
// UpdateTimer()
//     window.setTimeout("Tick()", 1000);
// }
//
// function Tick() {
//     if (TotalSeconds <= 0) {
//         alert("Time's up!")
//
//         return;
//     }
//
//     TotalSeconds -= 1;
//     UpdateTimer()
//     window.setTimeout("Tick()", 1000);
// }
//
// function UpdateTimer() {
//     var Seconds = TotalSeconds;
//
//     var Days = Math.floor(Seconds / 86400);
//     Seconds -= Days * 86400;
//
//     var Hours = Math.floor(Seconds / 3600);
//     Seconds -= Hours * (3600);
//
//     var Minutes = Math.floor(Seconds / 60);
//     Seconds -= Minutes * (60);
//
//     var TimeStr = (LeadingZero(Minutes) + ":" + LeadingZero(Seconds))
//
//
//     Timer.innerHTML = TimeStr;
// }
//
// function LeadingZero(Time) {
//     return (Time < 10) ? "0" + Time : + Time;
// }

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(minutes + ":" + seconds);

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}