cat <<EOF > /c/Users/USER/Tutor_Ruso_Pro/app.py
import streamlit as st
from groq import Groq
import os
from gtts import gTTS

# Configuración SEO de la Web App
st.set_page_config(page_title="Tutor Ruso Pro - David Salazar", page_icon="🇷🇺")

# Cargar API Key (En la nube se configura en 'Secrets')
api_key = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=api_key)

st.title("🇷🇺 Tutor de Ruso V39")
st.write("Bienvenido, David. Tu herramienta de IA ahora es una Web App.")

user_input = st.text_input("Escribe tu duda o frase:", placeholder="Ej: Frases para el aeropuerto")

if st.button("Procesar con IA"):
    if user_input and api_key:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Eres un tutor de ruso. Traduce y explica: {user_input}"}],
        )
        res = completion.choices[0].message.content
        st.info(res)
        
        # Audio
        tts = gTTS(text=res, lang='ru')
        tts.save("audio.mp3")
        st.audio("audio.mp3")
    else:
        st.warning("⚠️ Falta texto o la API Key no está configurada en los Secretos.")
EOF