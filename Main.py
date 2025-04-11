import pvporcupine
import sounddevice as sd
import numpy as np
import SpeechToText
import Groq
import Text2Speech

def main():
    access_key = "lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ=="

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=["Dis-Robot_fr_mac_v3_0_0/Dis-Robot_fr_mac_v3_0_0.ppn"],
        model_path='porcupine_params_fr.pv'
    )

    def detect_keyword():
        print("En écoute du mot-clé...")
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
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Mot clé détecté !")
                    break

    try:
        while True:
            detect_keyword()  # flux temporaire => OK
            print("Lancement de la transcription...")
            transcription = SpeechToText.transcribe_voice()
            reponse = Groq.ask_groq(transcription)
            Text2Speech.speak(reponse)
            print("Transcription reçue :", transcription)
            print("Retour à l'écoute du mot-clé...")
            Text2Speech.stop_speech_loop()

    except KeyboardInterrupt:
        print("Arrêt du programme.")
    finally:
        porcupine.delete()

if __name__ == "__main__":
    main()
