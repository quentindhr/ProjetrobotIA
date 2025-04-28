Il faut telecharger le modele vosk "vosk-model-fr-0.6-linto-2.2.0" sur ce site https://alphacephei.com/vosk/models

Il faut faire attention aux audio device deux à changer :
    -un sur speech to text 
    -un dans le main dans la fonction detect_keyword
    def detect_keyword(self):
        try:
            with sd.InputStream(
                channels=1,
                samplerate=self.porcupine.sample_rate,
                blocksize=self.porcupine.frame_length,
                dtype='int16',
                device=0  # Laisse None pour utiliser le micro par défaut
            ) as stream:

Le code pour connaitre le bon numero de device 

import sounddevice as sd

devices = sd.query_devices()
for i, d in enumerate(devices):
    print(f"ID: {i} | Nom: {d['name']} | Canaux d'entrée: {d['max_input_channels']}")
