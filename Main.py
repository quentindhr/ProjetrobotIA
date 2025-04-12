import SpeechToText
import Groq
import Text2Speech
import sounddevice as sd
import numpy as np
import pvporcupine

ACCESS_KEY = 'lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ=='  # Ton access key Porcupine
KEYWORD_PATH = "Dis-Robot_fr_mac_v3_0_0/Dis-Robot_fr_mac_v3_0_0.ppn"  # Chemin vers ton .ppn
MODEL_PATH = "porcupine_params_fr.pv"  # Chemin vers porcupine_params_fr.pv

def detect_keyword(porcupine):
    with sd.InputStream(
        channels=1,
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype='int16',
        device=0
    ) as stream:
        while True:
            pcm = stream.read(porcupine.frame_length)[0]
            pcm = np.squeeze(pcm).astype(np.int16)
            if porcupine.process(pcm) >= 0:
                print("Mot-clé détecté !")
                return

def handle_interaction():
    print("Enregistrement en cours...")
    transcription = SpeechToText.transcribe_voice()

    print(f"Transcription : {transcription}")
    response = Groq.ask_groq(transcription)

    
    print(f"Réponse : {response}")
    Text2Speech.speak(response)

def main_loop():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH],
        model_path=MODEL_PATH
    )

    try:
        while True:
            print("En attente du mot-clé...")
            detect_keyword(porcupine)

            handle_interaction()

            print("Retour à l'écoute...\n")
    except KeyboardInterrupt:
        print("Arrêt du programme.")
    finally:
        porcupine.delete()

if __name__ == "__main__":
    main_loop()
