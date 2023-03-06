$(document).ready(function () {

    setInterval(displayDateTime, 1000);
    setInterval(displayRemainingSeats, 5 * 60 * 1000);

    const socket = new WebSocket('ws://localhost:8080');

    socket.onopen = function (event) {
        console.log('Connected to server');
    };

    socket.onmessage = function (event) {
        const js = JSON.parse(event.data);
        //console.log(js);
        document.getElementById(js['region']).innerText = js['message'];
    };

    socket.onclose = function (event) {
        console.log('Connection closed');
        if (!isShabbat) location.reload();
    };


});

let isShabbat = false;

//Time Region

const months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];

function displayDateTime() {
    const now = new Date();

    let day = now.getDay();
    let hours = now.getHours();

    if ((day === 5 && hours >= 12) || (day === 6 && hours < 23)) {
        document.getElementById("center").innerText = "";
        document.getElementById("bottom_center").innerText = "";
        document.getElementById("bottom_left").innerText = "";

        document.getElementById("shabbat_start_time").innerText = "";
        document.getElementById("shabbat_end_time").innerText = "";

        document.getElementById("kabbalat_shabbat").innerText = "";

        document.getElementById("current_date").innerText = "";
        document.getElementById("current_date").innerText = "";

        isShabbat = true;
        return;
    } else isShabbat = false;


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

    if (isShabbat) return;

    try {
        $.ajax({
                type: 'POST',
                url: '/api/shabbat/kabbalat',
                success: function (result) {
                    const res = JSON.parse(result);
                    if (res.success) {
                        document.getElementById("kabbalat_shabbat").innerText = "Мест на шаббат осталось: " + res.seats;
                    } else {
                        document.getElementById("kabbalat_shabbat").innerText = "";
                    }
                }
            }
        );
    } catch
        (err) {
    }


}

