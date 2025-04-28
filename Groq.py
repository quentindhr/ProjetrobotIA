# ask_groq_v2.py

from groq import Groq
import random

# Initialiser le client Groq
client = Groq(api_key="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")

# Mots-clés liés aux directions
DIRECTION_KEYWORDS = {"droite", "gauche", "tout droit", "demi-tour"}
VALID_DIRECTIONS = {"à droite", "à gauche", "tout droit", "demi-tour"}

# Prompts dynamiques
PROMPTS_DIRECTION = [
    "Tu es un robot de guidage dans une école. Réponds uniquement par 'à droite', 'à gauche', 'tout droit' ou 'demi-tour'.",
    "Indique uniquement la direction : à droite, à gauche, tout droit ou demi-tour. Rien d'autre."
]

PROMPTS_GENERAL = [
    "Tu es un assistant bienveillant dans une école. Aide les étudiants avec des réponses claires sur les salles, les cours et les enseignants.",
    "Ton rôle est d'assister les étudiants dans leur vie scolaire. Sois clair et précis."
]

# Réponses de secours
FALLBACK_RESPONSES = [
    "Je n'ai pas bien compris ta demande, peux-tu reformuler ?",
    "Désolé, je rencontre un problème. Peux-tu reposer ta question ?",
    "Je ne suis pas sûr d'avoir compris. Essayons encore !"
]

def ask_groq(question):
    """Détermine si la question est liée à une direction et interroge Groq."""
    question = question.strip().lower()  # Nettoyage basique de l'entrée

    try:
        # Détecter si la question est une direction
        is_direction = any(word in question for word in DIRECTION_KEYWORDS)

        # Choix dynamique du prompt
        system_prompt = random.choice(PROMPTS_DIRECTION) if is_direction else random.choice(PROMPTS_GENERAL)

        # Paramètres adaptés
        max_tokens = 10 if is_direction else 100
        top_p = 0.5  # Limite encore plus les réponses imprévues

        print("🤖 Je réfléchis...")  # Feedback utilisateur pendant génération

        # Appel API
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model="llama-3-70b-8192",
            max_tokens=max_tokens,
            temperature=0,
            top_p=top_p
        )

        # Extraction et nettoyage de la réponse
        response_text = response.choices[0].message.content.strip()

        # Vérification si la réponse est acceptable (fallback si vide)
        if not response_text:
            return random.choice(FALLBACK_RESPONSES)

        return response_text

    except Exception as e:
        print(f"⚠️ Erreur avec Groq API : {e}")
        return random.choice(FALLBACK_RESPONSES)

