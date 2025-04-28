import asyncio
import edge_tts
import uuid
import os
import pygame

# Option : tu peux choisir ta voix ici (voix françaises de Microsoft)
DEFAULT_VOICE = "fr-FR-HenriNeural"  # Homme
# Exemple homme : "fr-FR-HenriNeural"

async def generate_audio(text, filename, voice=DEFAULT_VOICE):
    """Génère un fichier audio MP3 depuis du texte avec Edge TTS."""
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(filename)

def speak(text, lang='fr'):
    """Joue un texte vocalisé avec Edge TTS."""
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        asyncio.run(generate_audio(text, filename))

        # Lecture avec pygame
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        os.remove(filename)
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale Edge TTS : {e}")

if __name__ == "__main__":
    speak("Bonjour, je suis ton robot")
