import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import imageio.v2 as imageio
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD")
st.title("DRAMA RD - V24")
st.caption("Sube 1 por 1 - formato celular")

st.info("Sube las 3 imagenes de 1 en 1. Si no te deja WEBP, hazle captura de pantalla a la imagen y sube la captura (JPG)")

col1, col2, col3 = st.columns(3)
with col1:
    f1 = st.file_uploader("Foto 1 - Jueza", type=["jpg","jpeg","png","webp"], key="f1")
with col2:
    f2 = st.file_uploader("Foto 2 - Luisa", type=["jpg","jpeg","png","webp"], key="f2")
with col3:
    f3 = st.file_uploader("Foto 3 - Hipolito", type=["jpg","jpeg","png","webp"], key="f3")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.")

def add_text(img, txt):
    W,H = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0, H-100, W, H], fill=(0,0,0))
    d.text((W//2, H-50), txt.upper()[:50], fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    return img

def zoom_frames(img, n=50):
    frames=[]
    W,H = img.size
    for i in range(n):
        z = 1 + (i/n)*0.20
        nw, nh = int(W*z), int(H*z)
        rz = img.resize((nw, nh), Image.LANCZOS)
        crop = rz.crop(((nw-W)//2, (nh-H)//2, (nw-W)//2+W, (nh-H)//2+H))
        frames.append(np.array(crop))
    return frames

if st.button("CREAR VIDEO", type="primary", use_container_width=True):
    if not f1 or not f2 or not f3:
        st.error(f"Te faltan fotos: {3 - sum([1 for x in [f1,f2,f3] if x])} foto(s). Debes subir las 3, una en cada casilla.")
    else:
        frases = [s.strip() for s in guion.split(".") if s.strip()]
        all_frames=[]
        files = [f1,f2,f3]

        for i in range(3):
            img = Image.open(files[i]).convert("RGB")
            img = img.resize((1280,720), Image.LANCZOS)
            txt = frases[i] if i < len(frases) else ""
            img = add_text(img, txt)
            st.image(img, use_container_width=True)
            all_frames.extend(zoom_frames(img, 55))

        video_path = "/tmp/final.mp4"
        imageio.mimsave(video_path, all_frames, fps=20, macro_block_size=1)

        try:
            audio_path="/tmp/audio.mp3"
            gTTS(text=". ".join(frases), lang='es', tld='com.mx').save(audio_path)
            st.audio(audio_path)
        except: pass

        with open(video_path, "rb") as f:
            vb = f.read()
        st.video(vb)
        st.success("VIDEO CREADO")
        st.download_button("DESCARGAR VIDEO", vb, "drama_rd.mp4", "video/mp4")
        st.balloons()
