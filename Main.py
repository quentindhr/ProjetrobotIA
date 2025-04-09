import vosk
import sounddevice as sd
import json

SEUIL_MINIMUM_VOIX=50

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

def detect_trigger_word(device_index=1):
    global robot_detected
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback, device=device_index):
        print("Microphone détecté. Dites 'robot' pour commencer.")
        while not robot_detected:
            sd.sleep(100)
    return True

def audioRec():
    sample_rate = 16000
    duration = 30  # Durée d'enregistrement en secondes
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Attendre la fin de l'enregistrement

    return audio

def isSilence(audio):
    # Vérifier si le volume moyen est inférieur au seuil minimum
    volume_moyen = audio.mean()
    if volume_moyen < SEUIL_MINIMUM_VOIX:
        print(volume_moyen)
        return True
    else:
        print(volume_moyen)
        return False





# Exemple d'utilisation dans le main
if __name__ == "__main__":
    if detect_trigger_word():
        audio = audioRec()
        while not isSilence(audio):
            print("silence")
            audio = audioRec()
