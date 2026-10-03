import streamlit as st
import requests
import time

# Configuración de interfaz optimizada para teléfonos móviles
st.set_page_config(
    page_title="Kling AI 55s Creator", 
    page_icon="🎥", 
    layout="centered"
)

st.title("🎥 Generador de Videos Geopolíticos (55s)")
st.write("Genera escenas y fragmentos de actuación real sobre la era política y conflictos globales mediante Kling AI.")

# Coloca aquí tu clave secreta de Kling AI de forma segura dentro de las comillas
KLING_API_KEY = st.secrets["KLING_API_KEY"]


# Menú interactivo basado en las escenas de tu guion
escena_guion = st.selectbox(
    "Elige la escena del guion para generar (Fijado a 55 segundos):",
    (
        "Personalizado (Escribir mi propia escena)",
        "Intro: Donald Trump en un podio con mapas geopolíticos en rojo de fondo",
        "Bloque 1: El Congreso de EE.UU. dividido con gráficos animados y debates",
        "Bloque 2: Tensiones en el Medio Oriente (Israel e Irán y el Estrecho de Ormuz)",
        "Bloque 3: Reunión diplomática tensa sobre el conflicto Rusia-Ucrania"
    )
)

# Configuración automática de prompts descriptivos y cinemáticos en inglés para Kling AI
prompt_defecto = ""
if "Intro" in escena_guion:
    prompt_defecto = "Cinematic slow motion shot of Donald Trump standing at a presidential podium, dark background with glowing red global geopolitical maps, dramatic professional lighting, 9:16 vertical aspect ratio, continuous 55 seconds scene"
elif "Bloque 1" in escena_guion:
    prompt_defecto = "Dramatic scene of the US Congress interior, politicians debating intensely with motion graphics overlays representing electoral split, cinematic atmosphere, 55 seconds duration sequence"
elif "Bloque 2" in escena_guion:
    prompt_defecto = "Geopolitical tension visualization, military ships near the Strait of Hormuz, dramatic sky, high-production cinematic look, continuous 55 seconds video timeline"
elif "Bloque 3" in escena_guion:
    prompt_defecto = "Tense diplomatic meeting room with world leaders looking at maps of Russia and Ukraine, emotional expressions, cinematic lighting, close-up shot, 55 seconds long full performance"

prompt_final = st.text_area("Instrucciones de actuación e imagen para la IA:", value=prompt_defecto, height=120)

# Botón principal para activar la generación real
if st.button("🚀 Generar Video de Actuación", type="primary", use_container_width=True):
    if KLING_API_KEY == "TU_KLING_API_KEY_AQUI":
        st.error("Por favor, introduce tu API Key real de Kling AI en la línea 17 del código para poder generar.")
    elif not prompt_final:
        st.error("Por favor, describe la escena geopolítica que deseas que la IA actúe.")
    else:
        # Marcador de posición para actualizar el estado en tiempo real en la pantalla del móvil
        estado_placeholder = st.empty()
        
        try:
            # --- PASO 1: ENVIAR SOLICITUD A LA API DE KLING AI ---
            headers = {
    "Authorization": f"Bearer {KLING_API_KEY}",
    "Content-Type": "application/json"
}
                
            
            
            payload_task = {
                "prompt": prompt_final,
                "duration": 55,  # Tus 55 segundos exactos
                "aspect_ratio": "9:16",
                "camera_control": "auto"
            }
            
            # Endpoint oficial de tareas de Kling AI
            task_response = requests.post("https://api-singapore.klingai.com/v1/videos/text2video", headers=headers, json=payload_task)
            
            if task_response.status_code == 200 or task_response.status_code == 201:
                task_data = task_response.json()
                task_id = task_data.get("data", {}).get("task_id")
                
                # --- PASO 2: CONSULTAR ESTADO DE LA GENERACIÓN (POLLING) ---
                video_ready_url = None
                
                # Bucle de consulta cada 5 segundos (máximo 30 intentos = 2.5 minutos)
                for intento in range(30): 
                    estado_placeholder.info(f"🎬 La IA está actuando y procesando la escena geopolítica... (Tiempo transcurrido: {intento * 5}s)")
                    
                    status_data = status_response.json()
                    status_response = requests.get(f"https://api-singapore.klingai.com/v1/videos/text2video/{task_id}", headers=headers)
                    task_status = status_data.get("data", {}).get("task_status")
                    
                    if task_status == "SUCCESS":
                        video_ready_url = status_data.get("data", {}).get("video_url")
                        break
                    elif task_status == "FAILED":
                        st.error("La generación de la escena falló en los servidores de Kling AI.")
                        break
                
                # --- PASO 3: DESCARGA E INYECCIÓN SEGURA DEL VIDEO GENERADO ---
                if video_ready_url:
                    estado_placeholder.empty()
                    
                    # Se descarga el archivo en bytes directo a la memoria para evitar reproductores rotos
                    video_response = requests.get(video_ready_url, timeout=30)
                    video_bytes = video_response.content
                    
                    st.success("✨ ¡Tu escena de video de 55 segundos está listo!")
                    
                    # Reproductor nativo móvil usando los bytes descargados
                    st.video(video_bytes, format="video/mp4")
                    
                    # Botón de descarga directa al carrete o almacenamiento del teléfono
                    st.download_button(
                        label="📥 Descargar Escena 55s (.mp4)",
                        data=video_bytes,
                        file_name="escena_guion_trump_55s.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    estado_placeholder.error("El tiempo de espera expiró. Por favor, intenta generar la escena nuevamente.")
            else:
                st.error(f"Error al conectar con la API de Kling: Código de Estado {task_response.status_code}")
                
        except Exception as e:
            st.error(f"Ocurrió un error inesperado al procesar el video: {e}")
