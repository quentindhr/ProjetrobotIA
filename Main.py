import sounddevice as sd
import numpy as np
import whisper
import torch
import queue
import time
from SpeechToText import *  # tu réutilises ta fonction optimisée ici


SAMPLERATE = 16000
BLOCK_DURATION = 2  # en secondes
BLOCK_SIZE = int(SAMPLERATE * BLOCK_DURATION)
CHANNELS = 1
BUFFER_LENGTH = 5  # Nombre de blocs conservés dans le buffer circulaire

DEVICE = 0  # ID de l'appareil d'entrée audio 


buffer_queue = queue.Queue(maxsize=BUFFER_LENGTH)

def audio_callback(indata, frames, time_info, status):
    if status:
        print("Status:", status)
    audio_chunk = indata.copy().flatten()
    if buffer_queue.full():
        buffer_queue.get()
    buffer_queue.put(audio_chunk)


def record_audio(duration=10):
    print("Enregistrement déclenché...")
    audio = sd.rec(int(SAMPLERATE * duration), 
                   samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16', device=DEVICE)
    sd.wait()
    return audio

def listen_for_trigger_and_respond():
    print("Système de détection lancé")
    with sd.InputStream(callback=audio_callback, channels=CHANNELS,
                        samplerate=SAMPLERATE, blocksize=BLOCK_SIZE, dtype='int16',device=DEVICE):
        while True:
            time.sleep(BLOCK_DURATION)
            if buffer_queue.qsize() >= 3:
                if detect_trigger_word(buffer_queue):
                    print("Mot-clé détecté !")
                    recorded_audio = record_audio()
                    transcription = speech_to_text(recorded_audio)
                    print("Transcription finale :", transcription)
                    break

if __name__ == "__main__":
    listen_for_trigger_and_respond()
