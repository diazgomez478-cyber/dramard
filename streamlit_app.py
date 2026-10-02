import streamlit as st
import requests, urllib.parse, random, tempfile
# PARCHE para el error de tu foto
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import ImageClip, concatenate_videoclips

st.set_page_config(page_title="VIDEO RD 55s SIN VOZ", layout="centered")
st.title("Solo actuación (sin gTTS)")
st.write("Video real con movimiento, sin voz de robot. Tú le pones la voz en CapCut.")

idea = st.selectbox("Elige tu drama:", (
    "Luisa demanda a Hipolito por 100 millones",
    "El error en producción un viernes a las 5 PM",
    "La guerra de los Pull Requests"
))

prompt_base = st.text_area("Describe la actuación:", value="Dominican woman Luisa crying shouting in courtroom, then happy hugging kids winning, then angry Dominican man spending money in luxury club, cinematic acting", height=120)

if st.button("🚀 GENERAR VIDEO 55s REAL", type="primary", use_container_width=True):
    with st.spinner("Filmando 55s... 40 seg"):
        try:
            clips = []
            for i in range(3):
                seed = random.randint(1,999999)
                prompt = f"{idea} {prompt_base} scene {i+1}, vertical 9:16 photorealistic 4k"
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={seed}&nologo=true&model=flux"
                img_data = requests.get(url, timeout=60).content
                tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                tmp_img.write(img_data)
                tmp_img.close()

                clip = ImageClip(tmp_img.name).set_duration(18.5).resize(height=1280)
                clip = clip.resize(lambda t: 1 + 0.015 * t) # zoom lento = efecto actuación
                clips.append(clip)

            video_final = concatenate_videoclips(clips, method="compose")
            tmp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            video_final.write_videofile(tmp_video.name, fps=24, codec='libx264', verbose=False, logger=None)

            st.success("¡VIDEO 55s LISTO!")
            st.video(tmp_video.name)
            st.download_button("⬇️ DESCARGAR VIDEO MP4", open(tmp_video.name, "rb").read(), "drama_55s.mp4", "video/mp4", use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Manage app > Reboot después de cambiar requirements.txt")
