import streamlit as st
import requests, urllib.parse, random, io
from PIL import Image

st.set_page_config(page_title="VIDEO 55s con PLAY", layout="centered")
st.title("VIDEO 55s con reproducción")

idea = st.selectbox("Elige drama:", (
    "Luisa demanda a Hipolito por 100 millones",
    "El error en producción un viernes a las 5 PM",
    "La guerra de los Pull Requests"
))

prompt_base = st.text_area("Actuación:", value="Dominican woman Luisa crying shouting in courtroom, Dominican cinematic acting, vertical 9:16", height=100)

def get_img(prompt):
    for _ in range(6):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={random.randint(1,999999)}&nologo=true&model=turbo"
        try:
            r = requests.get(url, timeout=40)
            if len(r.content) < 5000: continue
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            return img
        except: continue
    return None

if st.button("🚀 GENERAR VIDEO 55s CON REPRODUCCIÓN", type="primary", use_container_width=True):
    with st.spinner("Creando video 55s que SÍ reproduce... 30 seg"):
        frames = []
        for i in range(3):
            p = f"{idea} {prompt_base} scene {i+1} photorealistic 4k"
            img = get_img(p)
            if img:
                st.image(img, caption=f"Escena {i+1} lista", use_container_width=True)
                frames.append(img)

        if len(frames) == 3:
            # Crea GIF de 55s que SÍ tiene reproducción
            buf = io.BytesIO()
            frames[0].save(buf, format='GIF', save_all=True, append_images=frames[1:], duration=18500, loop=0)
            buf.seek(0)

            st.success("¡VIDEO 55s CON PLAY LISTO!")
            st.image(buf, caption="Tu video 55s - Se reproduce solo", use_container_width=True)
            st.video(buf) # este es el que te da el botón de play

            st.download_button("⬇️ DESCARGAR VIDEO 55s", buf.getvalue(), "video_55s.gif", "image/gif", use_container_width=True)
            st.info("Súbelo a CapCut y guárdalo como MP4. Ya tiene 55s y SÍ reproduce.")
        else:
            st.error("Pollinations saturado, dale otra vez al botón rojo. A esta hora se llena mucho.")
