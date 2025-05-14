
# 🤖 AImigos – Module IA

Bienvenue dans le dépôt GitHub du **module Intelligence Artificielle** du projet **AImigos**, un robot multiservice conçu pour assister les étudiants dans leur quotidien grâce à l'intelligence artificielle.

## 🎯 Objectif

Le robot AImigos est capable de répondre à des questions orales sur la vie scolaire (emploi du temps, professeurs, localisation des salles, etc.) via une interface vocale intuitive. Ce module regroupe les composants liés à l'intelligence artificielle embarquée qui permettent cette interaction.

## 🧠 Fonctionnalités IA

- **Détection de mot-clé (wake word)** avec [Picovoice Porcupine](https://github.com/Picovoice/porcupine)
- **Détection de voix active (VAD)** avec [Picovoice Cobra](https://github.com/Picovoice/cobra)
- **Transcription vocale** via [OpenAI Whisper](https://github.com/openai/whisper)
- **Compréhension et génération de réponses** via un modèle d'IA générative 
- **Requêtes orientées contexte** sur des données personnalisées (emplois du temps, informations internes à l’école, etc.)

## 🛠️ Stack technique

| Composant | Description |
|----------|-------------|
| **Python** | Langage principal |
| **Whisper** | Reconnaissance vocale |
| **Porcupine** | Wake word detection (ex : "Dis Robot") |
| **Cobra** | Voice activity detection |
| **Transformers / LLM local** | Pour le traitement du langage naturel |
| **Base de données locale** | Stockage des informations de l'école |
| **MQTT (optionnel)** | Communication avec d'autres modules du robot |

## 🧩 Architecture

Microphone<br>
│<br>
▼<br>
Porcupine (Wake Word Detection)<br>
│<br>
▼<br>
Cobra (Voice Activity Detection)<br>
│<br>
▼<br>
Whisper (Speech-to-Text)<br>
│<br>
▼<br>
LLM local (Analyse + Génération de réponse)<br>
│<br>
▼<br>
Réponse vocale ou action du robot<br>

## Lancer le module

`git clone https://github.com/votre-utilisateur/aimigos-ia.git`<br>

`cd aimigos-i`<br>

`pip install -r requirements.txt`<br>

`python main.py`

