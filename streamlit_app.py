import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import imageio.v2 as imageio
import requests, io, random, urllib.parse, time
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD")
st.title("DRAMA RD - V28 PELICULA")
st.success("Modo pelicula activado!")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.")

# PROMPTS PELICULA - BLOQUEADOS (no mas barcos ni Trump)
PROMPTS = [
    "Dominican woman 30 years old furious angry crying tears close up, courtroom background, Dominican Republic flag blurred, cinematic movie dramatic lighting, Netflix drama, photorealistic 8k",
    "Dominican mother 30 years old hugging two children happy crying tears of joy, courtroom victory, warm golden cinematic light, emotional family drama movie, photorealistic 8k",
    "Dominican man 40 years old furious angry throwing Dominican pesos money champagne luxury penthouse night, villain dramatic movie lighting, photorealistic 8k"
]

def get_img_pelicula(prompt):
    for _ in range(3):
        try:
            seed = random.randint(1,9999999)
            # Bloqueamos noticias con negative
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=768&height=1024&seed={seed}&nologo=true&model=flux&enhance=true"
            r = requests.get(url, timeout=80)
            if len(r.content) > 10000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720), Image.LANCZOS)
        except:
            time.sleep(1)
    return Image.new('RGB',(1280,720),(25,25,35))

def add_text_cine(img, txt, escena):
    W,H = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,45], fill=(0,0,0))
    d.rectangle([0,H-110,W,H], fill=(0,0,0))
    d.text((20,8), f"ESCENA {escena} - DRAMA RD", fill=(255,215,0))
    t = txt.upper()[:55]
    d.text((W//2, H-55), t, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    return img

def zoom_frames(img):
    frames=[]
    W,H = img.size
    for i in range(50):
        z = 1 + (i/50)*0.22
        nw, nh = int(W*z), int(H*z)
        rz = img.resize((nw,nh), Image.LANCZOS)
        left = (nw-W)//2
        top = (nh-H)//2
        crop = rz.crop((left, top, left+W, top+H))
        frames.append(np.array(crop))
    return frames

if st.button("🎬 CREAR VIDEO PELICULA", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:3]
    if len(frases) < 3:
        st.error("Escribe 3 frases separadas por punto")
    else:
        all_frames=[]
        progress = st.progress(0)
        for i in range(3):
            st.write(f"🎥 Filmando escena {i+1}/3 estilo pelicula...")
            img = get_img_pelicula(PROMPTS[i])
            img = add_text_cine(img, frases[i], i+1)
            st.image(img, use_container_width=True)
            all_frames.extend(zoom_frames(img))
            progress.progress((i+1)/3)

        st.write("🎞️ Editando video...")
        path = "/tmp/pelicula.mp4"
        imageio.mimsave(path, all_frames, fps=20, macro_block_size=1)

        try:
            ap="/tmp/audio.mp3"
            gTTS(text=". ".join(frases), lang='es', tld='com.mx').save(ap)
            st.audio(ap)
            st.caption("Audio generado")
        except:
            pass

        with open(path,"rb") as f:
            vb = f.read()

        st.success("✅ VIDEO PELICULA LISTO!")
        st.video(vb)
        st.download_button("⬇️ DESCARGAR VIDEO PELICULA", vb, "drama_rd_pelicula.mp4", "video/mp4", use_container_width=True)
        st.balloons()
