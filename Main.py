import vosk
import sounddevice as sd
import json
import numpy as np
from tqdm import tqdm
import time
from SpeechToText import speech_to_text

SEUIL_MINIMUM_VOIX = 50
DEVICE_INDEX = 0 # Index du microphone à utiliser 1 pour le MAC

# Initialisation du modèle Vosk (FR)
model = vosk.Model("vosk-model-fr")
rec = vosk.KaldiRecognizer(model, 16000)

# Variable pour suivre la détection du mot "robot"
robot_detected = False

def callback(indata, frames, time_info, status):
    global robot_detected
    if status:
        print(f"Statut du micro : {status}", flush=True)

    try:
        if rec.AcceptWaveform(bytes(indata)):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()

            if "robot" in text:
                robot_detected = True
    except Exception as e:
        print(f"Erreur dans le callback audio : {e}")

def detect_trigger_word():
    global robot_detected
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback, device=DEVICE_INDEX):
        print("Microphone détecté. Dites 'robot' pour commencer.")
        while not robot_detected:
            sd.sleep(100)
    return True

def audioRec(duration=5):
    ProgressRec()
    sample_rate = 16000
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16',device=DEVICE_INDEX)
    sd.wait()  # Attendre la fin de l'enregistrement
    return audio

def isSilence(audio):
    # Vérifier si le volume moyen est inférieur au seuil minimum
    volume_moyen = np.abs(audio).mean()
    print(f"Volume moyen : {volume_moyen}")
    return volume_moyen < SEUIL_MINIMUM_VOIX

def ProgressRec():
    # Fonction pour afficher une barre de progression
    for i in tqdm(range(50), desc="Enregistrement en cours", unit="%", ncols=100):
        time.sleep(0.1)  # Simuler le temps d'enregistrement

# Exemple d'utilisation dans le main
if __name__ == "__main__":
    if detect_trigger_word():
        print("Je vous écoute...")
        audio_list = []
        audio = audioRec()
        text = speech_to_text(audio)
        print(text)
        while not isSilence(audio):
            audio_list.append(audio)
            audio = audioRec()
        
        #for audio in audio_list:
            #text = speech_to_text(audio)
            #print(text)
        
