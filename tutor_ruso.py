import os, re, time, threading, random
import tkinter as tk
from gtts import gTTS
import speech_recognition as sr
from groq import Groq
import pygame
import static_ffmpeg

# --- SETUP ---
static_ffmpeg.add_paths()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY_GROQ = ""
client = Groq(api_key=API_KEY_GROQ)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

class TutorRusoLimpio:
    def __init__(self, root):
        self.root = root
        self.root.title("TUTOR RUSO V39 - SIN ASTERISCOS EN VOZ")
        self.root.geometry("850x950")
        self.root.configure(bg="#020617")

        self.text_area = tk.Text(root, height=25, width=95, bg="#000", fg="#38bdf8", 
                                 font=("Consolas", 11), padx=25, pady=25)
        self.text_area.pack(pady=20)
        
        self.user_input = tk.Entry(root, bg="#1e293b", fg="#facc15", font=("Arial", 14), width=50)
        self.user_input.pack(pady=10, ipady=12)
        self.user_input.bind('<Return>', lambda e: self.procesar())

        self.btn_stop = tk.Button(root, text="🛑 CALLAR (Q)", bg="#ef4444", fg="white", command=self.detener)
        self.btn_stop.pack(pady=10)

        self.interrumpir = False
        self.escuchando = True
        self.historial = [{"role": "system", "content": "Tutor de ruso. David es SEO. Formato FICHA de la foto."}]
        
        threading.Thread(target=self.hilo_micro, daemon=True).start()

    def detener(self):
        self.interrumpir = True
        pygame.mixer.stop()

    def procesar(self):
        msg = self.user_input.get()
        if msg.strip():
            self.user_input.delete(0, tk.END)
            self.ejecutar(msg)

    def ejecutar(self, msg):
        self.interrumpir = False
        self.escuchando = False
        threading.Thread(target=self.motor, args=(msg,), daemon=True).start()

    def motor(self, msg):
        self.log(f"\n➤ David: {msg}")
        try:
            self.historial.append({"role": "user", "content": msg})
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=self.historial)
            respuesta = res.choices[0].message.content
            self.hablar(respuesta)
        except: self.log("⚠️ Error.")
        self.escuchando = True

    def limpiar_para_voz(self, texto):
        """Elimina asteriscos y formato Markdown para que no se trabe el audio"""
        # Elimina asteriscos (**)
        t = texto.replace("**", "")
        t = t.replace("*", "")
        # Elimina almohadillas (#)
        t = t.replace("#", "")
        # Elimina guiones de lista al inicio
        t = re.sub(r'^\s*-\s*', '', t)
        # Reemplazos fonéticos específicos para David
        t = t.replace("Л", " El ") 
        return t

    def hablar(self, texto):
        lineas = [l.strip() for l in texto.split('\n') if l.strip()]
        for i, linea in enumerate(lineas):
            if self.interrumpir: break
            self.root.after(0, self.log, linea) # En pantalla sale con asteriscos
            
            texto_limpio = self.limpiar_para_voz(linea) # Al audio va limpio
            lang = 'ru' if bool(re.search(r'[\u0400-\u04FF]', linea)) else 'es'
            
            try:
                tts = gTTS(text=texto_limpio, lang=lang)
                f = os.path.join(BASE_DIR, f"v_{i}.mp3")
                tts.save(f)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(f))
                while pygame.mixer.Channel(1).get_busy() and not self.interrumpir:
                    time.sleep(0.05)
                if os.path.exists(f): os.remove(f)
            except: continue

    def log(self, m):
        self.text_area.insert(tk.END, m + "\n")
        self.text_area.see(tk.END)

    def hilo_micro(self):
        r = sr.Recognizer()
        r.pause_threshold = 2.0
        while True:
            if self.escuchando:
                with sr.Microphone() as s:
                    r.adjust_for_ambient_noise(s)
                    try:
                        a = r.listen(s, timeout=None, phrase_time_limit=10)
                        t = r.recognize_google(a, language="es-ES")
                        self.ejecutar(t)
                    except: pass
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TutorRusoLimpio(root)
    root.mainloop()