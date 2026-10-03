import streamlit as st
import requests
import time

st.set_page_config(page_title="Generador de Películas IA", page_icon="🎬", layout="centered")
st.title("🎬 Creador de Videos Cinemáticos")
st.write("Genera y reproduce tus dramas de 55 segundos con estilo de película directamente en tu móvil.")

# Gestión de credenciales
API_KEY = st.text_input("Introduce tu Kling AI API Key:", type="password")

# Prompt cinemático basado en tu guión de la Era de Trump
prompt_defecto = (
    "Cinematic movie trailer style, intense political thriller, close up shot of a leader "
    "looking worried in high contrast studio lighting, world maps background with glowing red "
    "and blue lines, ultra realistic 4k, 24fps atmosphere."
)

prompt_usuario = st.text_area("Prompt de video para la película:", value=prompt_defecto, height=100)

if st.button("🚀 Iniciar Generación de Video Real", type="primary", use_container_width=True):
    if not API_KEY:
        st.error("❌ Por favor, escribe tu API Key para poder procesar el video.")
    else:
        st.info("🛰️ Enviando escena al servidor de Kling AI...")
        
        # 1. Petición inicial para crear la tarea de video
        endpoint_crear = "https://klingai.com"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt_usuario,
            "duration": 55,       # Tu preferencia estricta de 55 segundos
            "aspect_ratio": "16:9", # Formato de película horizontal
            "quality": "high"
        }
        
        try:
            # Quitamos la simulación para llamar al servidor real
            respuesta_crear = requests.post(endpoint_crear, json=payload, headers=headers)
            
            if respuesta_crear.status_code in:
                id_tarea = respuesta_crear.json().get("task_id")
                st.warning(f"⏳ Video en cola de renderizado. ID: {id_tarea}")
                
                # Barra de progreso interactiva en el móvil mientras la IA dibuja el video
                barra_progreso = st.progress(0)
                status_video = "processing"
                video_url = None
                
                # Bucle de control para verificar el estado real en el servidor
                for i in range(1, 101):
                    time.sleep(2) # Pausa entre consultas para no saturar tu conexión
                    barra_progreso.progress(i)
                    
                    # Consultar si el archivo ya está listo para descargar
                    endpoint_estado = f"https://klingai.com{id_tarea}"
                    check_status = requests.get(endpoint_estado, headers=headers).json()
                    
                    if check_status.get("status") == "completed":
                        video_url = check_status.get("video_url")
                        break
                
                # 2. Descarga e incrustación del archivo multimedia real
                if video_url:
                    st.success("✨ ¡Película generada exitosamente!")
                    
                    # Descargamos los bytes reales de la URL entregada por la IA
                    video_bytes = requests.get(video_url).content
                    
                    # Renderizador de video integrado para que lo veas en la app sin salir de ella
                    st.video(video_bytes)
                    
                    # Botón de descarga móvil funcional
                    st.download_button(
                        label="⬇️ Descargar Video de Película (.mp4)",
                        data=video_bytes,
                        file_name="drama_trump_55s.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error("⏱️ El servidor está tardando más de lo esperado. Intenta presionar el botón de nuevo.")
            else:
                st.error(f"Error de API: {respuesta_crear.text}")
                
        except Exception as e:
            st.error(f"Error crítico en la conexión móvil: {e}")
