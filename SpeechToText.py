import whisper
import numpy as np
import torch

def speech_to_text(audio_data):
    model = whisper.load_model("small")

    if isinstance(audio_data, np.ndarray):
        audio = audio_data.flatten().astype(np.float32) / 32768.0  
        audio_tensor = torch.tensor(audio)
    else:
        raise ValueError("Le format de l'audio n'est pas reconnu (attendu: np.ndarray)")


    audio_tensor = whisper.pad_or_trim(audio_tensor)
    mel = whisper.log_mel_spectrogram(audio_tensor).to(model.device)


    _, probs = model.detect_language(mel)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text