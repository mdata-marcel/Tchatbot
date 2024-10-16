import streamlit as st
import os  # Nécessaire pour accéder aux variables d'environnement
from mistralai import Mistral

# Créer une fonction pour générer des réponses
def generate_response(user_input):
    api_key = os.getenv("API_KEY_MISTRAL")  # Récupérer la clé API depuis les variables d'environnement
    model = "mistral-large-latest"

    if not api_key:
        return "Erreur : La clé API n'a pas été définie."

    client = Mistral(api_key=api_key)

    # Personnalisation de la personnalité du chatbot
    personality_prompt = """
    Tu es un chatbot très poétique et tu t'exprimes comme Molière.
    """

    try:
        # Appel à l'API pour générer une réponse
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": personality_prompt},
                {"role": "user", "content": user_input.lower()},
            ]
        )
        
        # Retourne le contenu du message de la première réponse
        return chat_response.choices[0].message.content

    except Exception as e:
        # Gestion des erreurs et affichage dans l'interface
        st.write(f"Erreur rencontrée : {e}")
        return "Désolé, une erreur est survenue."

# Créer l'interface de l'application avec Streamlit
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions !")

# Stocker l'historique des conversations
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Créer un formulaire pour saisir la question
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Vous :", key="input")
    submit_button = st.form_submit_button(label='Envoyer')

# Afficher la réponse du bot
if submit_button and user_input:
    response = generate_response(user_input)
    # Ajouter l'entrée utilisateur et la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Affichage de l'historique des échanges
for sender, message in st.session_state.chat_history:
    if sender == "Vous":
        st.write(f"**{sender}:** {message}")
    else:
        st.write(f"*{sender}:* {message}")
