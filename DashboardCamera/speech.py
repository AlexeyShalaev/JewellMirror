from gtts import gTTS
import pygame
import io

# Инициализируем pygame
pygame.mixer.init()


def say(text):
    # Создаем объект gTTS
    tts = gTTS(text, lang='ru')

    # Преобразуем аудио в байтовый объект
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)

    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

    # Ожидаем завершения воспроизведения
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
