import whisper
import numpy as np
import torch
import pvcobra
import sounddevice as sd
import time


AUDIO_DEVICE = 0  # Remplacez par l'index run test pour savoir
cobra = pvcobra.create(access_key='lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ==')  # Remplace par ta clé

def speech_to_text(audio_data):
    model = whisper.load_model("small")

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

    silence_duration = 0
    max_silence_frames = int(sample_rate / frame_length * silence_threshold_sec)
    audio_buffer = []

    def callback(indata, frames, time_info, status):
        nonlocal silence_duration, audio_buffer
        if status:
            print("Aie", status)

        pcm = np.squeeze(indata).astype(np.int16)
        score = cobra.process(pcm)
        print(f"Score Cobra : {score:.2f}")
        is_voiced = score > 0.5

        if is_voiced:
            audio_buffer.append(pcm.copy())
            silence_duration = 0
            print("Voix détectée...")
        elif len(audio_buffer) > 0:
            silence_duration += 1
            print("... silence ...")
            if silence_duration >= max_silence_frames:
                raise sd.CallbackStop()

    print("En attente de voix...")
    try:
        with sd.InputStream(
            samplerate=sample_rate,
            blocksize=frame_length,
            channels=1,
            dtype='int16',
            callback=callback,
            device=AUDIO_DEVICE
        ):
            sd.sleep(duration_limit * 1000)
    except sd.CallbackStop:
        pass

    if audio_buffer:
        print("Voix terminée. Transcription...")
        audio_np = np.concatenate(audio_buffer, axis=0)
        return speech_to_text(audio_np)
    else:
        return "[Aucune voix détectée]"

if __name__ == "__main__":
    text = transcribe_voice()
    print("Transcription :", text)
