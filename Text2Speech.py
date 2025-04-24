from gtts import gTTS
import pygame
import uuid
import os

def speak(text, lang='fr'):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang=lang,slow=False)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        os.remove(filename)
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale : {e}")
