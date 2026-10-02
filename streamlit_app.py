import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import imageio.v2 as imageio
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD", page_icon="🎬")
st.title("DRAMA RD - V23 FINAL")
st.caption("Video que si abre y reproduce")

uploaded = st.file_uploader(
    "Sube 3 imagenes (jueza, Luisa+niños, Hipolito)",
    type=["jpg","webp","png"],
    accept_multiple_files=True
)

guion = st.text_area(
    "Guion",
    "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas."
)

def add_text(img, txt):
    W, H = img.size
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, H-110, W, H], fill=(0,0,0))
    t = txt.upper()[:55]
    draw.text((W//2, H-55), t, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    return img

def make_zoom(img):
    frames = []
    W, H = img.size
    for i in range(50):
        z = 1 + (i / 50) * 0.20
        nw = int(W * z)
        nh = int(H * z)
        resized = img.resize((nw, nh), Image.LANCZOS)
        left = (nw - W) // 2
        top = (nh - H) // 2
        crop = resized.crop((left, top, left+W, top+H))
        arr = np.array(crop)
        frames.append(arr)
    return frames

if st.button("CREAR VIDEO", type="primary", use_container_width=True):
    if not uploaded or len(uploaded) < 3:
        st.error("Sube primero las 3 imagenes que te genere arriba")
    else:
        frases = [f.strip() for f in guion.split(".") if f.strip()]
        all_frames = []

        for i in range(3):
            file = uploaded[i]
            texto = frases[i] if i < len(frases) else ""
            img = Image.open(file).convert("RGB")
            img = img.resize((1280, 720), Image.LANCZOS)
            img = add_text(img, texto)
            st.image(img, use_container_width=True)
            zoom_frames = make_zoom(img)
            all_frames.extend(zoom_frames)

        video_path = "/tmp/final.mp4"
        imageio.mimsave(video_path, all_frames, fps=20, macro_block_size=1)

        audio_path = "/tmp/audio.mp3"
        try:
            text_audio = ". ".join(frases)
            gTTS(text=text_audio, lang='es', tld='com.mx').save(audio_path)
            st.audio(audio_path)
        except:
            pass

        st.success("VIDEO LISTO")
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes)
        st.download_button("DESCARGAR VIDEO", video_bytes, "drama_final.mp4", "video/mp4")
        st.balloons()
