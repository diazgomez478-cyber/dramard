import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import imageio.v2 as imageio
import requests, io, random, urllib.parse, time
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD")
st.title("DRAMA RD - V28 PELICULA")
st.success("Modo pelicula - ya sin error de Java!")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.")

PROMPTS = [
    "Dominican woman furious angry crying tears courtroom close up cinematic movie lighting photorealistic",
    "Dominican mother happy hugging two children tears joy courtroom warm golden cinematic movie",
    "Dominican man furious angry throwing money champagne luxury penthouse night cinematic movie"
]

def get_img(prompt):
    for _ in range(3):
        try:
            seed = random.randint(1,9999999)
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=768&height=1024&seed={seed}&nologo=true&model=flux"
            r = requests.get(url, timeout=80)
            if len(r.content) > 10000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720), Image.LANCZOS)
        except:
            time.sleep(1)
    return Image.new('RGB',(1280,720),(20,20,30))

def add_text(img, txt, num):
    W,H = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,45], fill=(0,0,0))
    d.rectangle([0,H-100,W,H], fill=(0,0,0))
    d.text((20,8), f"ESCENA {num}", fill="gold")
    d.text((W//2, H-55), txt.upper()[:55], fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    return img

def zoom(img):
    frames=[]
    for i in range(50):
        z = 1 + (i/50)*0.22
        nw, nh = int(1280*z), int(720*z)
        rz = img.resize((nw,nh), Image.LANCZOS)
        frames.append(np.array(rz.crop(((nw-1280)//2, (nh-720)//2, (nw-1280)//2+1280, (nh-720)//2+720))))
    return frames

if st.button("CREAR VIDEO PELICULA", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:3]
    all_frames=[]
    for i in range(3):
        st.write(f"Filmando escena {i+1}...")
        im = get_img(PROMPTS[i])
        im = add_text(im, frases[i] if i < len(frases) else "", i+1)
        st.image(im, use_container_width=True)
        all_frames.extend(zoom(im))

    path="/tmp/pelicula.mp4"
    imageio.mimsave(path, all_frames, fps=20, macro_block_size=1)

    try:
        ap="/tmp/audio.mp3"
        gTTS(text=". ".join(frases), lang='es', tld='com.mx').save(ap)
        st.audio(ap)
    except: pass

    with open(path,"rb") as f:
        vb=f.read()
    st.video(vb)
    st.download_button("DESCARGAR VIDEO", vb, "drama_pelicula.mp4", "video/mp4")
    st.balloons()
