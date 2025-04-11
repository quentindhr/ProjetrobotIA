import whisper
import numpy as np
import torch
import pvcobra
import sounddevice as sd
import time
import logging

logging.basicConfig(level=logging.DEBUG)
print("Loading Whisper model...")
model = whisper.load_model("small")


AUDIO_DEVICE = 0  # Remplacez par l'index run test pour savoir
cobra = pvcobra.create(access_key='lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ==')  # Remplace par ta clé

silence_duration = 0
max_silence_frames = 1
audio_buffer = []

def speech_to_text(audio_data):
    

    if isinstance(audio_data, np.ndarray):
        audio = audio_data.flatten().astype(np.float32) / 32768.0
        audio_tensor = torch.tensor(audio)
    else:
        raise ValueError("Le format de l'audio n'est pas reconnu (attendu: np.ndarray)")

    audio_tensor = whisper.pad_or_trim(audio_tensor)
    mel = whisper.log_mel_spectrogram(audio_tensor).to(model.device)

    _, _ = model.detect_language(mel)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text

def transcribe_voice(duration_limit=10, silence_threshold_sec=2):
    sample_rate = cobra.sample_rate
    frame_length = cobra.frame_length

    print("Initialisation du flux audio...")  

    def voice_activity_callback(indata, frames, time_info, status):
        global silence_duration, audio_buffer
        #print("Callback appelé") 

        if status:
            print("Status Stream:", status)

        pcm = np.squeeze(indata).astype(np.int16)

        if is_voiced(pcm):
            audio_buffer.append(pcm.copy())
            silence_duration = 0
            print("Voix détectée...")
        elif len(audio_buffer) > 0 and is_silenced():
            raise sd.CallbackStop()

    #print("En attente de voix...")
    try:
        global silence_duration 
        silence_duration = 0
        
        
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
        print("Callback stopped.")
    except Exception as e:
        print(f"Exception during voice transcription: {e}")

    if audio_buffer:
        #print("Voix terminée. Transcription...")
        audio_np = np.concatenate(audio_buffer, axis=0)
        audio_buffer.clear()
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
    text = transcribe_voice()
    print("Transcription :", text)
