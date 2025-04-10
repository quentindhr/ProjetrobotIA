
import sounddevice as sd
import numpy as np
import whisper
import torch
import queue
import time
from SpeechToText import speech_to_text

# Initialisation Whisper
model = whisper.load_model("small")

# Paramètres audio
SAMPLERATE = 16000
BLOCK_DURATION = 0.5  # Réduction pour plus de réactivité
BLOCK_SIZE = int(SAMPLERATE * BLOCK_DURATION)
CHANNELS = 1
BUFFER_LENGTH = 8  # Suffisant pour maintenir quelques secondes de contexte
DEVICE = 0

# Liste des mots-clés
TRIGGER_WORDS = ["robot", "assistant", "aimigos"]

buffer_queue = queue.Queue(maxsize=BUFFER_LENGTH)

def audio_callback(indata, frames, time_info, status):
    if status:
        print("Status:", status)
    audio_chunk = indata.copy().flatten()
    if buffer_queue.full():
        buffer_queue.get()
    buffer_queue.put(audio_chunk)

def preprocess_audio_from_buffer():
    audio_data = np.concatenate(list(buffer_queue.queue)).astype(np.float32) / 32768.0
    audio_tensor = torch.tensor(audio_data)
    audio_tensor = whisper.pad_or_trim(audio_tensor)
    mel = whisper.log_mel_spectrogram(audio_tensor).to(model.device)
    return mel

def detect_trigger_word():
    if buffer_queue.qsize() < 4:
        return False
    mel = preprocess_audio_from_buffer()
    result = model.decode(mel, whisper.DecodingOptions(fp16=False))
    transcription = result.text.lower()
    print("🔍 Transcription :", transcription)
    return any(word in transcription for word in TRIGGER_WORDS)

def record_audio(duration=8):
    print("🎙️ Enregistrement déclenché...")
    audio = sd.rec(int(SAMPLERATE * duration), samplerate=SAMPLERATE,
                   channels=CHANNELS, dtype='int16', device=DEVICE)
    sd.wait()
    return audio

def listen_for_trigger_and_respond():
    print("🟢 En écoute... Dites un mot-clé.")
    with sd.InputStream(callback=audio_callback, channels=CHANNELS,
                        samplerate=SAMPLERATE, blocksize=BLOCK_SIZE,
                        dtype='int16', device=DEVICE):
        while True:
            time.sleep(BLOCK_DURATION)
            if detect_trigger_word():
                recorded_audio = record_audio()
                transcription = speech_to_text(recorded_audio)
                print("📜 Transcription complète :", transcription)
                break

if __name__ == "__main__":
    listen_for_trigger_and_respond()
