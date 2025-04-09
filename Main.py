import vosk
import sounddevice as sd
import json

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

# Exemple d'utilisation dans le main
if __name__ == "__main__":
    if detect_trigger_word():
        print("Le mot 'robot' a été détecté !")
