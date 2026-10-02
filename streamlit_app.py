import streamlit as st
import requests, urllib.parse, random, io
from PIL import Image

st.set_page_config(page_title="DRAMA RD 90s", page_icon="🎬", layout="centered")
st.title("🎬 Creador de Dramas de 90s RD")
st.write("Genera videos estilo YouTube Shorts de DRAMA DOMINICANO con actuación real.")

idea_rapida = st.selectbox("Elige una idea base para tu video:", (
    "Personalizado (Escribir mi propio prompt)",
    "Luisa demanda a Hipolito por 100 millones y gana",
    "Madre soltera gana juicio - padre lo gasta en lujos",
    "El juez falla a favor de Luisa y los niños"
))

prompt_por_defecto = ""
if "Luisa" in idea_rapida:
    prompt_por_defecto = "Dominican woman Luisa suing Hipolito for 100 million pesos in courtroom crying dramatic acting, victory with kids, angry man spending money in luxury club"
elif "Madre" in idea_rapida:
    prompt_por_defecto = "Dominican single mother wins court case hugging kids happy, father angry spending money in nightclub with bottles"
elif "juez" in idea_rapida:
    prompt_por_defecto = "Dominican judge hitting gavel in favor of mother and kids, dramatic courtroom"

prompt_usuario = st.text_area("Prompt para el video:", value=prompt_por_defecto, height=100)

if st.button("🚀 Generar Video 90s", type="primary", use_container_width=True):
    if not prompt_usuario.strip():
        st.warning("Escribe tu drama")
    else:
        with st.spinner("Filmando tu drama 90s con actores... 20 seg"):
            for i in range(3):
                st.subheader(f"Escena {i+1} - 30s actuación")
                seed = random.randint(1,999999)
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_usuario + f' scene {i+1}, dominican actors, vertical 9:16 cinematic') }?width=720&height=1280&seed={seed}&nologo=true"
                try:
                    r = requests.get(url, timeout=45)
                    img = Image.open(io.BytesIO(r.content))
                    st.image(img, use_container_width=True)
                    st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(prompt_usuario[:150])}&tl=es&client=tw-ob")
                    st.success(f"Escena {i+1} lista")
                except:
                    st.error("Reintenta")
            st.balloons()
            st.success("¡Tu video 90s está listo! 90 segundos total")

st.markdown("---")
st.markdown("💡 Tip: 90s funciona mejor: 30s inicio triste, 30s victoria, 30s venganza")
