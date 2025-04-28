import numpy as np
import pvcobra
import sounddevice as sd
import logging
import queue
import vosk
import json

logging.basicConfig(level=logging.DEBUG)

AUDIO_DEVICE = 0  # Remplacer par l'index correct
MODEL_PATH = "/Users/quentindeharo/AIMigos/vosk-model-fr-0.6-linto-2.2.0"  # Dossier contenant le modèle Vosk français (ex: 'vosk-model-small-fr-0.22')

cobra = pvcobra.create(access_key='lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ==')

silence_duration = 0
max_silence_frames = 3
audio_buffer = []

model = None

def loadingModel():
    global model
    model = vosk.Model(MODEL_PATH)
    print("Modèle Vosk chargé.")
    return model

def speech_to_text(audio_data):
    if isinstance(audio_data, np.ndarray):
        audio = audio_data.flatten().astype(np.int16)
    else:
        raise ValueError("Le format de l'audio n'est pas reconnu (attendu: np.ndarray)")

    recognizer = vosk.KaldiRecognizer(model, cobra.sample_rate)
    recognizer.SetWords(True)

    if recognizer.AcceptWaveform(audio_data.tobytes()):
        result = recognizer.Result()
        text = json.loads(result)["text"]
    else:
        text = json.loads(recognizer.FinalResult())["text"]

    return text

def transcribe_voice(duration_limit=10, silence_threshold_sec=2):
    sample_rate = cobra.sample_rate
    frame_length = cobra.frame_length
    silence_reset_threshold = int(sample_rate / frame_length * silence_threshold_sec)

    print("En attente de voix...")  
    local_buffer = []
    silence_counter = 0

    def voice_activity_callback(indata, frames, time_info, status):
        nonlocal silence_counter, local_buffer
        if status:
            print("Status:", status)

        pcm = np.squeeze(indata).astype(np.int16)

        if is_voiced(pcm):
            local_buffer.append(pcm.copy())
            silence_counter = 0
            print("🔊 Voix détectée...")
        elif local_buffer:
            silence_counter += 1
            if silence_counter > silence_reset_threshold:
                print("Silence prolongé détecté. Fin de l'enregistrement.")
                raise sd.CallbackStop()

    try:
        with sd.InputStream(
            samplerate=sample_rate,
            blocksize=frame_length,
            channels=1,
            dtype='int16',
            callback=voice_activity_callback,
            device=AUDIO_DEVICE
        ):
            sd.sleep(duration_limit * 1000)
    except sd.CallbackStop:
        pass
    except Exception as e:
        print(f"Erreur durant la transcription : {e}")

    if local_buffer:
        audio_np = np.concatenate(local_buffer, axis=0)
        return speech_to_text(audio_np)
    else:
        return "[Aucune voix détectée]"

def is_voiced(pcm):
    score = cobra.process(pcm)
    #print(f"Score Cobra : {score:.2f}")
    return score > 0.5  # seuil ajustable

def is_silenced():
    global silence_duration
    silence_duration += 1
    #print("... silence ...")
    return silence_duration >= max_silence_frames

if __name__ == "__main__":
    loadingModel()
    text = transcribe_voice()
    print("Transcription :", text)
