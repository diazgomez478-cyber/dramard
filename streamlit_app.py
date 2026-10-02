import streamlit as st
import requests, urllib.parse, random, io
from PIL import Image
from gtts import gTTS

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
else:
    prompt_por_defecto = ""
    audio_texto = ""

prompt_usuario = st.text_area("Prompt para el video (en inglés para mejor resultado):", value=prompt_por_defecto, height=100)

if st.button("🚀 Generar Video", type="primary", use_container_width=True):
    if not prompt_usuario.strip():
        st.warning("Por favor escribe o selecciona un prompt válido.")
    else:
        with st.spinner("Generando tu video para YouTube Shorts... Esto puede tomar un momento."):
            try:
                # GENERA IMAGEN QUE SI SE VE
                seed = random.randint(1000, 999999)
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_usuario + ' vertical 9:16 photorealistic') }?width=720&height=1280&seed={seed}&nologo=true&model=flux"
                r = requests.get(url, timeout=50)
                img = Image.open(io.BytesIO(r.content)).convert("RGB")
                st.image(img, use_container_width=True)

                # AUDIO QUE SI REPRODUCE - ARREGLO DE TU FOTO 0:00
                if audio_texto == "":
                    audio_texto = prompt_usuario[:150]
                
                tts = gTTS(text=audio_texto, lang='es', slow=False)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                st.audio(mp3_fp, format="audio/mp3")
                
                st.success("¡Tu video está listo!")
                st.markdown('<div style="background-color:#1B5E20; padding:15px; border-radius:10px; color:#A5D6A7;">Escena 1 lista - Audio reproduciendo</div>', unsafe_allow_html=True)
                st.balloons()

            except Exception as e:
                st.error(f"No se pudo generar. Intenta de nuevo. Error: {e}")

st.markdown("---")
st.markdown("💡 *Tip: Recuerda que los Shorts de YouTube funcionan mejor si duran 60 segundos y tienen un gancho fuerte al inicio.*")
