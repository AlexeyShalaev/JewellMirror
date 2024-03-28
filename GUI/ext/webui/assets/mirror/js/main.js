$(document).ready(function () {

    setInterval(displayDateTime, 1000);
    displayRemainingSeats();
    setInterval(displayRemainingSeats, 5 * 60 * 1000);
    setInterval(displayShabbatTime, 24 * 60 * 60 * 1000);

    generateQR('kabbalat_shabbat_qr', 'https://jewellclub.ru/shabbat/kabbalat-shabbat/', 250);
    generateQR('edu_qr', 'https://edu.jewellclub.ru/', 250);
    showSlides();

    const socket = new WebSocket('ws://localhost:8080');

    socket.onopen = function (event) {
        console.log('Connected to server');
    };

    socket.onmessage = async function (event) {
        const js = JSON.parse(event.data);
        //console.log(js);

        if (js['region'] === 'qr_code') {
            if (js['message'] === '') {
                document.getElementById('bottom_right').innerHTML = '';
            } else {
                generateQR('bottom_right', js['message'], 200);
            }
        } else {
            if (js['region'] === 'bottom_center' && 'user_id' in js) {
                const timestamp = new Date().getTime(); // Get current timestamp
                const animation_url = `https://edu.jewellclub.ru/api/animation/${js['user_id']}?_=${timestamp}`;
                document.getElementById(js['region']).innerHTML = `
                 <img src="${animation_url}" style="border: none;">
                  <br>
                  ${js['message']}
                 `;
            } else {
                document.getElementById(js['region']).innerText = js['message'];
            }

            if (js['region'] === 'center' || js['region'] === 'bottom_center') {
                await new Promise(resolve => setTimeout(function () {
                    document.getElementById(js['region']).innerText = '';
                }, 4000));
            }
        }
    };

    socket.onclose = function (event) {
        console.log('Connection closed');
        if (!isShabbat) location.reload();
    };

});

let isShabbat = false;
let slideIndex = 0;

//Time Region

const months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];

function displayDateTime() {
    const now = new Date();

    let day = now.getDay();
    let hours = now.getHours();

    if ((day === 5 && hours > 12) || (day === 6 && hours < 23)) {
        $("#mirror_body").fadeOut();
        isShabbat = true;
        return;
    } else {
        isShabbat = false;
        $("#mirror_body").fadeIn();
    }


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

function displayShabbatTime() {

    if (isShabbat) return;

    try {
        $.ajax({
                type: 'POST',
                url: '/api/shabbat',
                success: function (result) {
                    const res = JSON.parse(result);
                    if (res.success) {
                        document.getElementById("shabbat_start_time").innerText = "Зажигание: " + res.shabbat['candle'];
                        document.getElementById("shabbat_end_time").innerText = "Авдала: " + res.shabbat['havdalah'];
                    }
                }
            }
        );
    } catch
        (err) {
    }


}

// QR tools

function generateQR(element_id, link, size) {
    var qr = new QRious({
        value: link,
        size: size // размер QR-кода в пикселях
    });

    var qrContainer = document.getElementById(element_id);
    qrContainer.innerHTML = ''; // Очищаем контейнер, если уже был создан QR-код

    // Создаем img элемент и устанавливаем его src равным data URL QR-кода
    var qrImage = document.createElement('img');
    qrImage.src = qr.toDataURL();
    qrContainer.appendChild(qrImage);
}

// slide show

function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1
    }
    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 5000); // Change image every 5 seconds
}