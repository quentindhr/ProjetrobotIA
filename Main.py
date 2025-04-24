import gui
import SpeechToText
import Groq
import Text2Speech
import sounddevice as sd
import numpy as np
import pvporcupine
import threading

ACCESS_KEY = 'lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ=='  # Ton access key Porcupine
KEYWORD_PATH = "Dis-Robot_fr_mac_v3_0_0/Dis-Robot_fr_mac_v3_0_0.ppn"  # Chemin vers ton .ppn
MODEL_PATH = "porcupine_params_fr.pv"  # Chemin vers porcupine_params_fr.pv

class MainApp:
    def __init__(self):

        #gui_app = gui.launch_loading_gui()
        SpeechToText.loadingModel()
        Text2Speech.init_tts()
        #gui.close_loading_gui(gui_app)

        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH],
            model_path=MODEL_PATH
        )

        # Start keyword detection in a separate thread
        self.keyword_thread = threading.Thread(target=self.detect_keyword)
        self.keyword_thread.daemon = True
        self.keyword_thread.start()

    def detect_keyword(self):
        with sd.InputStream(
            channels=1,
            samplerate=self.porcupine.sample_rate,
            blocksize=self.porcupine.frame_length,
            dtype='int16',
            device=0
        ) as stream:
            while True:
                pcm = stream.read(self.porcupine.frame_length)[0]
                pcm = np.squeeze(pcm).astype(np.int16)
                if self.porcupine.process(pcm) >= 0:
                    print("Mot-clé détecté !")
                    self.gui_app.root.after(0, self.handle_interaction)

    def handle_interaction(self):
        print("Enregistrement en cours...")
        transcription = SpeechToText.transcribe_voice()

        print(f"Transcription : {transcription}")
        response = Groq.ask_groq(transcription)

        print(f"Réponse : {response}")
        self.gui_app.update_text_area(f"Réponse : {response}")
        Text2Speech.speak(response)

if __name__ == "__main__":
    
    main_app = MainApp()
    
