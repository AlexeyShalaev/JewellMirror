from gtts import gTTS
import pygame
import io

# Инициализируем pygame
pygame.mixer.init()


async def say(text):
    # Создаем объект gTTS
    tts = gTTS(text, lang='ru')

    # Преобразуем аудио в байтовый объект
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)

    voice_channel = pygame.mixer.Channel(1)
    voice_sound = pygame.mixer.Sound(audio_stream)

    voice_channel.play(voice_sound)
    while voice_channel.get_busy():
        import asyncio
        await asyncio.sleep(1)
