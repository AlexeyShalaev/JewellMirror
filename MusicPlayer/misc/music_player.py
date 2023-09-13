import os

import pygame

from MusicPlayer.misc import config
from MusicPlayer.misc.tools import is_free_time, singleton
from MusicPlayer.models.song import Song


def check_permission(func):
    def wrapper(self, *args, **kwargs):
        if self.admin_permission and is_free_time():
            return func(self, *args, **kwargs)

    return wrapper


@singleton
class MusicPlayer:
    def __init__(self):
        self.music_folder = config.songs_path
        self.music_queue = []
        self.current_song = None
        self.earlier_volume = 1
        self.is_paused = True
        self.is_muted = False
        self.admin_permission = True

        # Инициализация Pygame для воспроизведения музыки
        pygame.init()

        # Устанавливаем событие для окончания трека
        self.END_OF_TRACK = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.END_OF_TRACK)

    def load_song(self, song: Song):
        pygame.mixer.music.load(os.path.join(self.music_folder, 'audios', str(song.id) + '.mp3'))

    def reload(self):
        # Остановить воспроизведение музыки
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Очистить очередь песен и сбросить состояние
        self.music_queue = []
        self.current_song = None
        self.earlier_volume = 1
        self.is_paused = True
        self.is_muted = False
        self.admin_permission = True

    @check_permission
    def add_song(self, song: Song):
        self.music_queue.append(song)

    def get_queue(self):
        return self.music_queue

    @check_permission
    def play_next_track(self):
        if self.music_queue:
            if self.current_song is not None:
                pygame.mixer.music.stop()

            self.current_song = self.music_queue.pop(0)
            self.load_song(self.current_song)
            pygame.mixer.music.play()
            self.is_paused = False
        else:
            self.is_paused = True
            self.current_song = None

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = True

    @check_permission
    def resume(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    @check_permission
    def mute(self):
        if not self.is_muted:
            self.earlier_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            self.is_muted = True

    def unmute(self):
        if self.is_muted:
            pygame.mixer.music.set_volume(self.earlier_volume)
            self.is_muted = False

    def change_volume(self, volume):
        self.is_muted = False
        pygame.mixer.music.set_volume(volume)

    @check_permission
    def skip_song(self):
        pygame.mixer.music.stop()
        # play_loop -> gona play next track

    @check_permission
    def play_loop(self):
        for event in pygame.event.get():
            if event.type == self.END_OF_TRACK:
                self.play_next_track()

    def get_current_time(self):
        if self.current_song is not None:
            pos = pygame.mixer.music.get_pos()
            if pos == -1:
                return 0
            return pos // 1000  # Преобразование миллисекунд в секунды
        return 0  # Возвращаем 0, если нет текущего трека или трек не воспроизводится

    def to_json(self):
        data = {
            "music_queue": [song.to_json() for song in self.music_queue],
            "current_song": self.current_song.to_json() if self.current_song is not None else 'none',
            "volume": pygame.mixer.music.get_volume(),
            "is_paused": self.is_paused,
            "is_muted": self.is_muted,
            "current_time": self.get_current_time()
        }
        return data

    @staticmethod
    def get_song_duration(song_path):
        try:
            # Загрузка аудиофайла
            sound = pygame.mixer.Sound(song_path)
            # Получение длительности аудиофайла в секундах
            return int(sound.get_length())
        except:
            return 0
