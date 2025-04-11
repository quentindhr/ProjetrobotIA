import pyttsx3
import threading
from queue import Queue

engine = pyttsx3.init()
speech_queue = Queue()

def _speech_loop():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

# Lance le thread au démarrage
speech_thread = threading.Thread(target=_speech_loop, daemon=True)
speech_thread.start()

def speak(text):
    speech_queue.put(text)

def stop_speech_loop():
    speech_queue.put(None)
    speech_thread.join()  
