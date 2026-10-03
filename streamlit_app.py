import streamlit as st
import requests
import time

st.set_page_config(page_title="Generador de Películas IA", page_icon="🎬", layout="centered")
st.title("🎬 Creador de Videos Cinemáticos")
st.write("Genera y reproduce tus dramas de 55 segundos con estilo de película directamente en tu móvil.")

# Gestión de credenciales
API_KEY = st.text_input(
    "Introduce tu Kling AI API Key:",
    value="api-key-kling-cQHpThKJLwWNN07q8G0huGtLG0z9yIzOM41Ac9VgnOY",
    type="password"
)

formato_pantalla = st.selectbox(
    "📺 Selecciona el formato del video:",
    ("Short de YouTube / Reel (Vertical 9:16)", "Película de Cine / YouTube Tradicional (Horizontal 16:9)")
)

aspect_ratio_api = "9:16" if "9:16" in formato_pantalla else "16:9"

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
        # Limpiamos la clave por si pegaste "api-key-kling-"
        clean_key = API_KEY.replace("api-key-kling-", "").strip()

        st.info("🛰️ Enviando escena al servidor de Kling AI...")

        # ENDPOINTS CORREGIDOS
        endpoint_crear = "https://api-singapore.klingai.com/v1/videos/text2video"
        headers = {
            "Authorization": f"Bearer {clean_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt_usuario,
            "duration": "5", # Kling solo permite 5 o 10, 55 no existe, luego lo unimos
            "aspect_ratio": aspect_ratio_api,
            "mode": "std"
        }

        try:
            respuesta_crear = requests.post(endpoint_crear, json=payload, headers=headers)

            if respuesta_crear.status_code == 200 or respuesta_crear.status_code == 201:
                data = respuesta_crear.json()
                id_tarea = data.get("data", {}).get("task_id") or data.get("task_id")
                st.warning(f"⏳ Video en cola. ID: {id_tarea}")

                barra_progreso = st.progress(0)
                video_url = None

                for i in range(1, 61):
                    time.sleep(3)
                    barra_progreso.progress(int(i*100/60))

                    endpoint_estado = f"https://api-singapore.klingai.com/v1/videos/text2video/{id_tarea}"
                    check_resp = requests.get(endpoint_estado, headers=headers)
                    check_status = check_resp.json()

                    status = check_status.get("data", {}).get("task_status")
                    st.write(f"Estado: {status} - {i*3}s")

                    if status == "succeed":
                        video_url = check_status.get("data", {}).get("task_result", {}).get("videos", [{}])[0].get("url")
                        break
                    if status == "failed":
                        st.error(f"Falló: {check_status}")
                        break

                if video_url:
                    st.success("✨ ¡Película generada!")
                    video_bytes = requests.get(video_url).content
                    st.video(video_url)
                    st.download_button(
                        label="⬇️ Descargar Video (.mp4)",
                        data=video_bytes,
                        file_name="drama_55s.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error("⏱️ Sigue en proceso, espera 1 min y recarga.")
            else:
                st.error(f"Error API {respuesta_crear.status_code}: {respuesta_crear.text}")

        except Exception as e:
            st.error(f"Error crítico: {e}")
