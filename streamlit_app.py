import streamlit as st
import requests
import time

# Configuración de interfaz optimizada para teléfonos móviles
st.set_page_config(
    page_title="Kling AI 55s Creator", 
    page_icon="🎥", 
    layout="centered"
)

st.title("🎥 Generador de Videos y Actuación (55s) IA")
st.write("Generación de video real con actuación fluida de 55 segundos mediante Kling AI.")

# Reemplaza aquí con tu clave secreta de Kling AI de forma segura
KLING_API_KEY = "TU_KLING_API_KEY_AQUI"

# Menú dinámico de actuación
idea_actuacion = st.selectbox(
    "Elige el tipo de escena de acción/drama (Configurada a 55 segundos):",
    (
        "Personalizado (Escribir mi propia escena)",
        "Spiderman colgado de cables en set con pantalla azul, detrás de cámaras",
        "Actor esquivando una explosión en cámara lenta, cinematic",
        "Discusión dramática intensa en un set de televisión, primer plano",
        "Escena de riesgo saltando entre edificios de noche"
    )
)

# Configuración de los prompts detallados
prompt_defecto = ""
if "Spiderman" in idea_actuacion:
    prompt_defecto = "Spiderman performing a stunt hanging from wires over a miniature city build, blue screen studio background, high production behind the scenes, realistic movement, 9:16 vertical, exact 55 seconds duration sequence"
elif "explosión" in idea_actuacion:
    prompt_defecto = "Stuntman running and jumping away from a massive explosion, slow motion, cinematic action sequence, vertical 9:16, real acting, continuous 55 seconds video"
elif "Discusión" in idea_actuacion:
    prompt_defecto = "Two actors arguing intensely, emotional expressions, dramatic studio lighting, cinematic acting, close-up shot, 55 seconds long full performance"
elif "edificios" in idea_actuacion:
    prompt_defecto = "Action scene of a stunt double leaping between high-rise building rooftops at night, dramatic lighting, fast-paced motion, 55 seconds continuous timeline"

prompt_final = st.text_area("Instrucciones de actuación para la IA:", value=prompt_defecto, height=120)

# Botón para activar el proceso real
if st.button("🚀 Generar Video de Actuación", type="primary", use_container_width=True):
    if KLING_API_KEY == "TU_KLING_API_KEY_AQUI":
        st.error("Por favor, introduce tu API Key real de Kling AI en el código para poder generar.")
    elif not prompt_final:
        st.error("Por favor, describe la escena que deseas que la IA actúe.")
    else:
        # Contenedor de progreso en tiempo real para móviles
        estado_placeholder = st.empty()
        
        try:
            # --- PASO 1: ENVIAR SOLICITUD A KLING AI ---
            headers = {
                "Authorization": f"Bearer {KLING_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload_task = {
                "prompt": prompt_final,
                "duration": 55, # Solicitud explícita de tus 55 segundos
                "aspect_ratio": "9:16",
                "camera_control": "auto"
            }
            
            # Endpoint de creación de tareas en la API de Kling
            task_response = requests.post("https://klingai.com", json=payload_task, headers=headers, timeout=15)
            
            if task_response.status_code in:
                task_data = task_response.json()
                task_id = task_data.get("data", {}).get("task_id")
                
                # --- PASO 2: CONSULTAR ESTADO DE LA ACTUACIÓN (*POLLING*) ---
                video_ready_url = None
                
                # Bucle de espera controlado
                for intento in range(30): 
                    estado_placeholder.info(f"🎬 La IA está actuando y procesando la escena... (Tiempo transcurrido: {intento * 5}s)")
                    time.sleep(5)
                    
                    # Consultamos el estado usando el identificador de la tarea
                    status_response = requests.get(f"https://klingai.com/{task_id}", headers=headers, timeout=10)
                    status_data = status_response.json()
                    
                    task_status = status_data.get("data", {}).get("task_status")
                    
                    if task_status == "SUCCESS":
                        # Obtenemos la URL final del video generado por Kling AI
                        video_ready_url = status_data.get("data", {}).get("video_url")
                        break
                    elif task_status == "FAILED":
                        st.error("La generación del video falló en los servidores de Kling AI.")
                        break
                
                # --- PASO 3: DESCARGA E INYECCIÓN SEGURA DEL ARCHIVO MP4 ---
                if video_ready_url:
                    estado_placeholder.empty()
                    
                    # Descargamos los datos binarios directamente a la memoria de la aplicación
                    video_response = requests.get(video_ready_url, timeout=30)
                    video_bytes = video_response.content
                    
                    st.success("✨ ¡Tu video de actuación de 55 segundos está listo!")
                    
                    # Despliegue seguro y nativo sin depender de enlaces externos rotos
                    st.video(video_bytes, format="video/mp4")
                    
                    # Botón de almacenamiento directo
                    st.download_button(
                        label="📥 Descargar Video 55s (.mp4)",
                        data=video_bytes,
                        file_name="drama_kling_55s.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    estado_placeholder.error("El tiempo de espera expiró o la API no entregó el video. Intenta nuevamente.")
            else:
                st.error(f"Error de conexión con la API de Kling: {task_response.status_code}")
                
        except Exception as e:
            st.error(f"Ocurrió un error inesperado al procesar: {e}")
