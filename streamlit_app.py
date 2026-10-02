import streamlit as st
import requests, urllib.parse, random, io, os
from PIL import Image
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="Generador de Videos para YouTube", page_icon="🎬", layout="centered")
st.title("🎬 Creador de Dramas de 60s")
st.write("Genera videos estilo YouTube Shorts sobre GitHub y programación directamente desde tu móvil.")

idea_rapida = st.selectbox(
    "Elige una idea base para tu video:",
    (
        "Personalizado (Escribir mi propio prompt)",
        "El error en producción un viernes a las 5 PM",
        "La guerra de los Pull Requests (Code Review)",
        "El misterio del commit anónimo a las 3 AM",
        "Luisa demanda a Hipolito por 100 millones"
    )
)

prompt_por_defecto = ""
audio_texto = ""

if "viernes" in idea_rapida:
    prompt_por_defecto = "A stressed software engineer staring at a computer screen with code and error messages, office setting, cinematic lighting"
    audio_texto = "El error en produccion un viernes a las cinco PM, el ingeniero esta estresado"
elif "Pull Requests" in idea_rapida:
    prompt_por_defecto = "A frustrated programmer looking at a laptop reviewing code with glowing annotations, dramatic expression"
    audio_texto = "La guerra de los Pull Requests, el code review se vuelve intenso"
elif "commit" in idea_rapida:
    prompt_por_defecto = "A mysterious glowing computer monitor showing GitHub commits in dark room, cinematic tech thriller"
    audio_texto = "El misterio del commit anonimo a las tres de la mañana"
elif "Luisa" in idea_rapida:
    prompt_por_defecto = "Dominican woman Luisa crying shouting in courtroom demanding 100 million pesos, Dominican actress, vertical 9:16 cinematic"
    audio_texto = "Luisa demanda a Hipolito por cien millones de pesos por abandono y maltrato"

prompt_usuario = st.text_area("Prompt para el video (en inglés para mejor resultado):", value=prompt_por_defecto, height=100)
texto_voz = st.text_input("Texto para la voz en off:", value=audio_texto)

if st.button("🚀 Generar Video", type="primary", use_container_width=True):
    if not prompt_usuario or not texto_voz:
        st.error("Por favor, asegúrate de tener un prompt de imagen y un texto para la voz.")
    else:
        with st.spinner("🎬 Creando tu Short... Por favor espera."):
            try:
                # 1. Generar y guardar el Audio temporal
                tts = gTTS(text=texto_voz, lang='es')
                audio_path = "temp_audio.mp3"
                tts.save(audio_path)
                
                # 2. Simulación de descarga/generación de Imagen (Reemplaza con tu API real)
                # Aquí guardamos una imagen temporal de prueba (puedes conectar tu API de Pollinations/OpenAI aquí)
                img = Image.new('RGB', (1080, 1920), color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                image_path = "temp_image.jpg"
                img.save(image_path)
                
                # 3. COMBINAR EN VIDEO REAL USANDO MOVIEPY
                audio_clip = AudioFileClip(audio_path)
                duracion = audio_clip.duration  # El video durará lo mismo que el audio
                
                # Crear el clip de video a partir de la imagen estática
                video_clip = ImageClip(image_path).set_duration(duracion)
                # Asignarle el audio
                video_clip = video_clip.set_audio(audio_clip)
                
                # Renderizar el archivo final MP4
                output_video_path = "final_short.mp4"
                video_clip.write_videofile(
                    output_video_path, 
                    fps=24, 
                    codec="libx264", 
                    audio_codec="aac"
                )
                
                # Cerrar clips para liberar memoria
                audio_clip.close()
                video_clip.close()
                
                # 4. Mostrar el video en Streamlit
                st.success("¡Video generado con éxito!")
                st.video(output_video_path)
                
                # Limpieza de archivos temporales locales
                os.remove(audio_path)
                os.remove(image_path)
                
            except Exception as e:
                st.error(f"Hubo un error al compilar el video: {e}")
