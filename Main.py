
import pvporcupine
import sounddevice as sd
import numpy as np
import SpeechToText  # Assurez-vous que ce module contient une fonction `start_recognition()`

def main():
    access_key = "lT3UyHC0V/4JeDsM4EupWUvMcTpHIdf5pPjvWvBWrGR2CXd62i/GpQ=="  # Remplacez par votre clé d'accès Picovoice

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=["Dis-Robot_fr_mac_v3_0_0/Dis-Robot_fr_mac_v3_0_0.ppn"],  # Vous pouvez changer ce mot clé ou en ajouter
        model_path='porcupine_params_fr.pv'
    )

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Status du stream: {status}")
        pcm = np.squeeze(indata).astype(np.int16)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Mot clé détecté!")
            SpeechToText.transcribe_voice(duration_limit=10, silence_threshold_sec=2)

    try:
        with sd.InputStream(
            channels=1,
            samplerate=porcupine.sample_rate,
            blocksize=porcupine.frame_length,
            dtype='int16',
            callback=audio_callback
        ):
            print("En écoute... Appuyez sur CTRL+C pour arrêter.")
            while True:
                pass
    except KeyboardInterrupt:
        print("Arrêt du programme.")
    finally:
        porcupine.delete()

if __name__ == "__main__":
    main()
