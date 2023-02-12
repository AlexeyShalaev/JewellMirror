$(document).ready(function () {
    setInterval(displayDateTime, 1000);
    setInterval(displayRemainingSeats, 5000); // todo 5 min ???
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
//https://jewellclub.ru/shabbat/kabbalat-shabbat/
    //todo
    /*
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://example.com", true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        console.log(xhr.responseText);
      }
    };
    xhr.send();
    */

    /*
      fetch("https://jewellclub.ru/shabbat/kabbalat-shabbat/")
        .then(response => console.log(response.text()))
        .then(text => console.log(text))
        .catch(error => console.error(error));
     */
    /*
    fetch("https://www.example.com/")
      .then(function(response) {
        return response.text();
      })
      .then(function(text) {
        console.log(text);
      });
    */
    /*
    fetch('http://example.com/movies.json')
  .then((response) => response.json())
  .then((data) => console.log(data));
     */
    /*
    let response = await fetch(url);
    let commits = await response.json(); // читаем ответ в формате JSON
    alert(commits[0].author.login);
     */
    /*
    fetch('https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits')
  .then(response => response.json())
  .then(commits => alert(commits[0].author.login));
     */

    document.getElementById("kabbalat_shabbat").innerText = "число мест";
}

/*
function displayShabbatTime(){
    //todo
    document.getElementById("shabbat_start_time").innerText = "start";
    document.getElementById("shabbat_end_time").innerText = "end";
}
 */