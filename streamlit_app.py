import streamlit as st
import requests, urllib.parse, random, io, tempfile
from PIL import Image
from moviepy.editor import ImageClip, concatenate_videoclips

st.set_page_config(page_title="VIDEO RD 55s SIN VOZ", layout="centered")
st.title("🎬 VIDEO 55s - Solo actuación (sin gTTS)")
st.write("Video real con movimiento, sin voz de robot. Tú le pones la voz en CapCut.")

idea = st.selectbox("Elige tu drama:", (
    "Luisa demanda a Hipolito por 100 millones",
    "El error en producción un viernes a las 5 PM",
    "La guerra de los Pull Requests"
))

prompt_base = st.text_area("Describe la actuación:", value="Dominican woman Luisa crying shouting in courtroom, then happy hugging kids winning, then angry Dominican man spending money in luxury club, cinematic acting", height=100)

if st.button("🚀 GENERAR VIDEO 55s REAL", type="primary", use_container_width=True):
    with st.spinner("Filmando actuación 55s... espera 40 seg"):
        try:
            clips = []
            textos_escena = ["Escena 1: Demanda", "Escena 2: Victoria", "Escena 3: Venganza"]

            for i in range(3):
                seed = random.randint(1,999999)
                prompt = f"{prompt_base} scene {i+1}, Dominican actors realistic face, dramatic acting, vertical 9:16, photorealistic 4k, cinematic"
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={seed}&nologo=true&model=flux"

                img_data = requests.get(url, timeout=60).content
                tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                tmp_img.write(img_data)
                tmp_img.close()

                # Efecto movimiento para que parezca video real, no foto fija
                clip = ImageClip(tmp_img.name).set_duration(18.5).resize(height=1280)
                # Zoom lento = parece que actúa
                clip = clip.resize(lambda t: 1 + 0.02 * t)

                clips.append(clip)
                st.image(img_data, caption=f"{textos_escena[i]} lista", use_container_width=True)

            # Une las 3 escenas = 55.5 segundos
            video_final = concatenate_videoclips(clips, method="compose")
            tmp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            video_final.write_videofile(tmp_video.name, fps=24, codec='libx264', verbose=False, logger=None)

            st.success("¡VIDEO 55s CON ACTUACIÓN LISTO - Sin gTTS!")
            st.video(tmp_video.name)
            st.download_button("⬇️ DESCARGAR VIDEO MP4 55s", open(tmp_video.name, "rb").read(), "drama_55s_sin_gtts.mp4", "video/mp4", use_container_width=True)
            st.info("Súbelo a CapCut y ponle tu voz o la de TikTok, así no suena a robot.")

        except Exception as e:
            st.error(f"Error: {e}")
