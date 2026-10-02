import streamlit as st
import requests, io, random, urllib.parse, time
from PIL import Image, ImageDraw
import numpy as np, textwrap
import imageio.v2 as imageio
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD")
st.title("🎬 DRAMA RD - V22")
st.caption("Video con texto - Si abre")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.")

def get_img(prompt):
    for _ in range(3):
        try:
            seed = random.randint(1,999999)
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=512&height=512&seed={seed}&nologo=true&model=flux"
            r = requests.get(url, timeout=60)
            if r.status_code==200 and len(r.content)>8000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720))
        except:
            time.sleep(1)
    return Image.new('RGB',(1280,720),(30,30,40))

def add_text(img, txt):
    draw = ImageDraw.Draw(img)
    W,H = img.size
    draw.rectangle([0, H-110, W, H], fill=(0,0,0,180))
    # Texto grande blanco como tu video
    t = txt.upper()[:60]
    draw.text((W//2, H-55), t, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    return img

if st.button("CREAR VIDEO", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:3]
    prompts = [
        "dominican female judge black robe courtroom",
        "dominican mother crying happy with two kids courtroom",
        "dominican man angry throwing money luxury party"
    ]
    frames = []
    for i, frase in enumerate(frases):
        st.write(f"Escena {i+1}...")
        img = get_img(prompts[i] + ", cinematic photorealistic")
        img = add_text(img, frase)
        st.image(img, use_container_width=True)
        # Crear zoom
        for j in range(40):
            z = 1 + (j/40)*0.15
            nw, nh = int(1280*z), int(720*z)
            rz = img.resize((nw,nh), Image.LANCZOS)
            frames.append(np.array(rz.crop(((nw-1280)//2, (nh-720)//2, (nw-1280)//2+1280, (nh-720)//2+720)))

    # Guardar video
    path = "/tmp/final.mp4"
    imageio.mimsave(path, frames, fps=12, macro_block_size=1)

    st.success("Video creado")
    st.video(path)

    # Audio aparte que si funciona
    try:
        ap = "/tmp/audio.mp3"
        gTTS(text=". ".join(frases), lang='es', tld='com.mx').save(ap)
        st.audio(ap)
    except:
        pass

    with open(path, "rb") as f:
        st.download_button("DESCARGAR VIDEO MP4", f.read(), "drama.mp4", "video/mp4")
