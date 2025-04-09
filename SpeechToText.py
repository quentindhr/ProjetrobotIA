import whisper

model = whisper.load_model("base")


result = model.transcribe("test.mp3", language="fr", fp16=False)

print(result["text"])