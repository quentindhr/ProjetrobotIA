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
        # Chargement des modèles
        SpeechToText.loadingModel()
        #Text2Speech.init_tts()

        # Initialisation de Porcupine
        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH],
            model_path=MODEL_PATH
        )

        # Démarrage de la détection du mot-clé
        self.keyword_thread = threading.Thread(target=self.detect_keyword)
        self.keyword_thread.daemon = True
        self.keyword_thread.start()

        print("Système en écoute... Dites le mot-clé.")

    def detect_keyword(self):
        try:
            with sd.InputStream(
                channels=1,
                samplerate=self.porcupine.sample_rate,
                blocksize=self.porcupine.frame_length,
                dtype='int16',
                device=1  # Laisse None pour utiliser le micro par défaut
            ) as stream:
                while True:
                    pcm = stream.read(self.porcupine.frame_length)[0]
                    pcm = np.squeeze(pcm).astype(np.int16)
                    if self.porcupine.process(pcm) >= 0:
                        print("Mot-clé détecté !")
                        self.handle_interaction()
        except Exception as e:
            print("Erreur dans detect_keyword :", e)

    def handle_interaction(self):
        print("Enregistrement en cours...")
        transcription = SpeechToText.transcribe_voice()
        print(f"Transcription : {transcription}")

        response = Groq.ask_groq(transcription)
        #print(f"Réponse : {response}")

        Text2Speech.speak(response)

if __name__ == "__main__":
    main_app = MainApp()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Arrêt manuel du programme.")
