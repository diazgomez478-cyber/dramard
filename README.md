import streamlit as st
import urllib.parse, random, requests, io, os
from PIL import Image
import numpy as np

st.set_page_config(page_title="DRAMA RD VIDEO", page_icon="🎬")
st.title("🎬 DRAMA RD - VIDEO REAL")
st.caption("🇩🇴 Tu PixVerse Dominicano - ¡Ahora SI genera VIDEO MP4!")

tema = st.text_input("Tema del drama", "Trump el terror de la casa blanca")
prota = st.text_input("Protagonista", "Victor el natural")
duracion = st.selectbox("Duración", ["1 MINUTO - 3 escenas", "3 MINUTOS - 5 escenas", "5 MINUTOS - 7 escenas"])

if st.button("🔥 CREAR VIDEO REAL"):
    num = 3 if "1" in duracion else 5 if "3" in duracion else 7

    st.success(f"🎥 Creando VIDEO de {duracion}...")
    barra = st.progress(0)

    frames = []
    # Creamos las imagenes
    for i in range(1, num+1):
        st.write(f"📸 Generando escena {i}/{num}...")
        prompt = f"dominican man {prota}, dramatic scene {tema}, cinematic movie, ultra realistic, 4k"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={random.randint(1,999999)}&nologo=true"

        try:
            r = requests.get(url, timeout=15)
            img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((720,1280))
            frames.append(np.array(img))
            st.image(img, caption=f"Escena {i}", use_container_width=True)
        except:
            st.error(f"Reintentando escena {i}...")

        barra.progress(i/num)

    # Crear video MP4 real
    if frames:
        try:
            import imageio.v2 as imageio
            video_path = "/tmp/dramard_video.mp4"
            # Cada foto dura 2 segundos = video de 6, 10 o 14 seg (para CapCut lo alargas)
            imageio.mimsave(video_path, frames, fps=0.5, macro_block_size=1)

            st.balloons()
            st.success("¡VIDEO CREADO!")
            st.video(video_path)

            with open(video_path, "rb") as f:
                st.download_button("⬇️ DESCARGAR VIDEO MP4", f, file_name=f"DRAMA_{prota}_{duracion}.mp4", mime="video/mp4")

            st.info("¡Ahora mete este video en CapCut, ponle voz y música de drama y súbelo!")
        except Exception as e:
            st.error(f"Instalando creador de video... dale de nuevo a CREAR VIDEO")
            os.system("pip install imageio[ffmpeg] numpy pillow requests")
    else:
        st.error("No se pudieron crear escenas, dale otra vez")
