import streamlit as st
from groq import Groq
import os
from gtts import gTTS

st.set_page_config(page_title="Tutor Ruso Pro", page_icon="🇷🇺")

# Cargar API Key
api_key = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=api_key)

st.title("🇷🇺 Tutor de Ruso V39")
st.write("David, tu sistema de IA ya está listo para la web.")

user_input = st.text_input("Ingresa una palabra o frase:", placeholder="Ej: ¿Cómo se dice cerveza?")

if st.button("Procesar"):
    if user_input and api_key:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Traduce al ruso y explica: {user_input}"}],
        )
        res = completion.choices[0].message.content
        st.success(res)
        
        # Audio
        tts = gTTS(text=res, lang='ru')
        tts.save("audio.mp3")
        st.audio("audio.mp3")
    else:
        st.warning("Escribe algo y asegúrate de configurar la API Key.")
