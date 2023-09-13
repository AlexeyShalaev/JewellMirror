$(document).ready(function () {

    document.querySelectorAll('[data-delay-click]').forEach(function (element) {
        element.addEventListener('click', handleDelayedClick);
    });


    // Выполнение запроса каждую секунду
    setInterval(get_music_player, 1000);

});

let last_cur_song_id = null;
let last_music_queue = null;

function handleDelayedClick(event) {
    const element = event.target;

    if (!element.disabled) {
        element.disabled = true;

        const delay = parseInt(element.getAttribute("data-delay-click")) || 1000;
        const method = element.getAttribute("data-method");

        if (method && typeof window[method] === 'function') {
            window[method](); // Вызываем указанный метод
        }

        setTimeout(function () {
            element.disabled = false;
        }, delay);
    }
}

function get_music_player() {
    try {
        $.ajax({
                type: 'GET',
                url: '/music/player/json',
                success: function (result) {
                    const mp = JSON.parse(result);
                    const current_song = mp['current_song'];

                    if (mp.is_muted) {
                        document.getElementById("current_song_mute").classList = "mejs__button mejs__volume-button mejs__unmute";
                    } else {
                        document.getElementById("current_song_mute").classList = "mejs__button mejs__volume-button mejs__mute";
                    }

                    document.getElementById("mp_volume").value = mp.volume * 100;

                    if (mp.is_paused) {
                        document.getElementById("current_song_mode").classList = "mejs__button mejs__playpause-button mejs__play";
                    } else {
                        document.getElementById("current_song_mode").classList = "mejs__button mejs__playpause-button mejs__pause";
                    }


                    if (current_song === 'none') {
                        // no music playing
                        document.getElementById("current_song_author").innerText = '';
                        document.getElementById("current_song_title").innerText = '';
                        document.getElementById("current_song_image").src = "/music/songs/images/default";
                        document.getElementById("current_song_time").innerText = beauty_seconds(0);
                        document.getElementById("current_song_duration").innerText = beauty_seconds(0);
                    } else {
                        document.getElementById("current_song_time").innerText = beauty_seconds(mp.current_time);
                        document.getElementById("current_song_progress").style.transform = `scaleX(${mp.current_time / current_song.duration})`;


                        if (last_cur_song_id == null || last_cur_song_id !== current_song.id) {
                            // new song
                            last_cur_song_id = current_song.id;

                            document.getElementById("current_song_image").src = "/music/songs/images/" + current_song.id;

                            document.getElementById("current_song_author").innerText = current_song.author;

                            if (current_song.name.length > 18) {
                                document.getElementById("current_song_title").innerHTML = '<marquee width="275px;" behavior="scroll" direction="left" class="mt-2">' + current_song.name + '</marquee>';
                            } else {
                                document.getElementById("current_song_title").innerText = current_song.name;
                            }

                            document.getElementById("current_song_duration").innerText = beauty_seconds(current_song.duration);
                        }
                    }

                    const music_queue = mp['music_queue'];
                    if (last_music_queue == null || JSON.stringify(last_music_queue) !== JSON.stringify(music_queue)) {
                        last_music_queue = music_queue;
                        // Заполнение таблицы данными из music_queue
                        var tableBody = document.getElementById("kt_datatable_songs_queue").getElementsByTagName("tbody")[0];
                        tableBody.innerHTML = '';
                        for (var i = 0; i < music_queue.length; ++i) {
                            var song = music_queue[i];
                            var row = tableBody.insertRow();

                            // Создание ячейки для изображения трека
                            var imageCell = row.insertCell(0);
                            var image = document.createElement("img");
                            image.src = "/music/songs/images/" + song.id;
                            image.width = 25;
                            imageCell.appendChild(image);

                            // Создание ячеек для названия, автора и длительности
                            var nameCell = row.insertCell(1);
                            nameCell.innerText = song.name;

                            var authorCell = row.insertCell(2);
                            authorCell.innerText = song.author;

                            var durationCell = row.insertCell(3);
                            durationCell.innerText = beauty_seconds(song.duration);
                        }
                    }

                }
            }
        );
    } catch
        (err) {
    }
}

function beauty_seconds(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = (totalSeconds % 60).toString().padStart(2, '0');

    return `${minutes}:${seconds}`;
}

function change_song_mode() {
    try {
        $.ajax({
                type: 'GET',
                url: '/music/player/change/mode'
            }
        );
    } catch
        (err) {
    }
}

function change_song_mute() {
    try {
        $.ajax({
                type: 'GET',
                url: '/music/player/change/mute'
            }
        );
    } catch
        (err) {
    }
}

function play_skip_song() {
    // Ваш код для воспроизведения следующей песни
    try {
        $.ajax({
                type: 'GET',
                url: '/music/player/skip'
            }
        );
    } catch
        (err) {
    }
}

function handleVolumeChange(value) {
    try {
        $.ajax({
                type: 'POST',
                data: {
                    'volume': value
                },
                url: '/music/player/change/volume'
            }
        );
    } catch
        (err) {
    }
}