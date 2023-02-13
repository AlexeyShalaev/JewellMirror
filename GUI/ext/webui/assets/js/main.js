$(document).ready(function () {
    setInterval(displayDateTime, 1000);
    setInterval(displayRemainingSeats, 5*60*1000);
    //setInterval(displayShabbatTime, 1000); // todo every friday or every 24 hours if jinja not works
});


//Time Region

const months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];

function displayDateTime() {
    const now = new Date();

    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }
    if (seconds < 10) {
        seconds = '0' + seconds;
    }
    const time = `${hours}:${minutes}:${seconds}`;

    const date = [now.getDate(), months[now.getMonth()]].join(' ');

    document.getElementById("current_time").innerText = time;
    document.getElementById("current_date").innerText = date;
}

// Shabbat Region

function displayRemainingSeats() {
    try {
        $.ajax({
                type: 'POST',
                url: '/api/shabbat/kabbalat',
                success: function (result) {
                    const res = JSON.parse(result);
                    if(res.success){
                        document.getElementById("kabbalat_shabbat").innerText = "Мест на шаббат осталось: "+res.seats;
                    } else{
                        document.getElementById("kabbalat_shabbat").innerText = "";
                    }
                }
            }
        );
    } catch
        (err) {
    }


}

/*
function displayShabbatTime(){
    document.getElementById("shabbat_start_time").innerText = "start";
    document.getElementById("shabbat_end_time").innerText = "end";
}
 */