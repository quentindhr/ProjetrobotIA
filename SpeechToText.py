import whisper
import numpy as np
import torch

model = whisper.load_model("small")
TRIGGER_WORDS = ["robot", "assistant", "aimigos"]

def speech_to_text(audio_data):
    model = whisper.load_model("small")


    if isinstance(audio_data, np.ndarray):
        audio = audio_data.flatten().astype(np.float32) / 32768.0  
        audio_tensor = torch.tensor(audio)
    else:
        raise ValueError("Le format de l'audio n'est pas reconnu (attendu: np.ndarray)")

    audio_tensor = whisper.pad_or_trim(audio_tensor)
    mel = whisper.log_mel_spectrogram(audio_tensor).to(model.device)

    # Transcription
    _, probs = model.detect_language(mel)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text

def detect_trigger_word(buffer_queue):
    if not is_speech_present(audio_data):
        return False
    
    mel = preprocess_audio_from_buffer(buffer_queue)
    result = model.decode(mel, whisper.DecodingOptions(fp16=False))
    transcription = result.text.lower()
    print("Transcription (buffer) :", transcription)
    return any(word in transcription for word in TRIGGER_WORDS)


def preprocess_audio_from_buffer(buffer_queue):
    audio_data = np.concatenate(list(buffer_queue.queue)).astype(np.float32) / 32768.0
    audio_tensor = torch.tensor(audio_data)
    audio_tensor = whisper.pad_or_trim(audio_tensor)
    mel = whisper.log_mel_spectrogram(audio_tensor).to(model.device)
    return mel

def is_speech_present(audio_data, threshold=500):
    volume = np.abs(audio_data).mean()
    return volume > threshold
