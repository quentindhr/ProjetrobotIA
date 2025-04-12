from groq import Groq
from Text2Speech import speak

# Initialiser le client Groq
client = Groq(api_key="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")

# Mots-clés liés aux directions
DIRECTION_KEYWORDS = {"droite", "gauche", "tout droit", "demi-tour"}
VALID_DIRECTIONS = {"à droite", "à gauche", "tout droit", "demi-tour"}

def ask_groq(question):
    """Détermine si la question est liée à une direction et interroge Groq."""
    
    if any(word in question.lower() for word in DIRECTION_KEYWORDS):
        system_prompt = (
            "Tu es un robot de guidage dans une école. "
            "Si on te demande une direction, réponds uniquement par : "
            "'à droite', 'à gauche', 'tout droit' ou 'demi-tour'."
        )
        max_tokens = 10
    else:
        system_prompt = (
            "Tu es un robot  assistant dans une école. Tu peux aider les etudiants sur tous les sujets. "
            "Réponds aux questions sur les salles, les cours, les enseignants, etc."
            
        )
        max_tokens = 100  
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=max_tokens,
        temperature=0
    )
    
    response_text = response.choices[0].message.content.strip()
    
    if response_text in VALID_DIRECTIONS:
        response_text = f"➡️ Direction : {response_text}"
    
     
    return response_text
