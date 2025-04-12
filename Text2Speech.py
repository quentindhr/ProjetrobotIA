import pyttsx3
import threading
from queue import Queue


engine = None  # Variable globale pour le moteur TTS

def init_tts():
    global engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Vitesse de la voix
    engine.setProperty('volume', 1)  # Volume (0.0 à 1.0)
    engine.setProperty('voice', 'french')  # Choisir la voix française
    print("Moteur TTS initialisé.")

    return engine

def speak(text):
    global engine
    engine.say(text)
    engine.runAndWait()
    engine.stop()

init_tts()