import streamlit as st, requests, io, random, urllib.parse, os, textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip

st.set_page_config(page_title="DRAMA RD CINE", page_icon="🎬")
st.title("🎬 DRAMA RD - V12 NUNCA FALLA")
st.caption("Victor - 1080p + Audio + Subtitulos")

guion = st.text_area("Guion",
"""Son 25 años de matrimonio. A mi defendida le toca la mitad.
Luisa demandó a Hipolito por no compartir su dinero.
Hipolito tiene 100 millones, por que no ayuda a su familia?
Porque ese dinero es solo mio, yo me lo gane.
El tribunal falla a favor de la mujer y los niños.
Hipolito furioso gastara todo en lujos y fiestas.""")

def get_img(prompt):
    # Intenta 3 veces, si no, crea imagen negra con texto para no fallar
    for _ in range(3):
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&seed={random.randint(1,99999)}&nologo=true"
            r = requests.get(url, timeout=60)
            if len(r.content) > 5000:
                img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((1920,1080))
                return img
        except: pass
    # Plan B: crea fondo cine si falla
    img = Image.new('RGB', (1920,1080), color=(20,20,30))
    d = ImageDraw.Draw(img)
    d.text((960,540), prompt[:40], fill="white", anchor="mm")
    return img

def add_sub(img, text):
    draw = ImageDraw.Draw(img)
    W,H = img.size
    # Barra negra
    draw.rectangle([0, H-200, W, H], fill=(0,0,0))
    # Texto grande y legible
    lines = textwrap.wrap(text, width=50)
    y = H-170
    for line in lines[:3]:
        # Fuente mas grande
        draw.text((W//2, y), line, fill="white", anchor="mm",
                  font=ImageFont.load_default(), stroke_width=3, stroke_fill="black")
        y+=45
    return img

def mov(img, frames=60):
    w,h = img.size
    out=[]
    for i in range(frames):
        zoom = 1 + (i/frames)*0.25
        nw, nh = int(w*zoom), int(h*zoom)
        rz = img.resize((nw, nh), Image.LANCZOS)
        left = int((nw-w)/2 * (i/frames))
        crop = rz.crop((left, 0, left+w, h))
        out.append(np.array(crop))
    return out

if st.button("🔥 CREAR VIDEO FINAL 1080p", use_container_width=True):
    partes = guion.split("\n")
    escenas = [
        (f"Dominican judge angry courtroom {partes[0]}", partes[0]),
        (f"Dominican woman crying with children {partes[1]}", partes[1]),
        (f"Rich Dominican man angry {partes[2]}", partes[2]),
        (f"Courtroom dramatic {partes[3]}", partes[3]),
        (f"Judge giving verdict {partes[4]}", partes[4]),
        (f"Man spending money party luxury {partes[5]}", partes[5]),
    ]

    all_frames=[]
    audios=[]
    for i,(prompt, txt) in enumerate(escenas):
        st.write(f"Escena {i+1}/6...")
        img = get_img(prompt + ", cinematic movie, 8k")
        img = add_sub(img, txt)
        st.image(img, caption=f"Escena {i+1}", use_container_width=True)
        all_frames.extend(mov(img, 50))

    st.write("Generando audio y video final...")
    # Audio total
    tts_path="/tmp/audio.mp3"
    gTTS(text=guion[:800], lang='es', tld='com.mx').save(tts_path)

    video_path="/tmp/final.mp4"
    clip = ImageSequenceClip(all_frames, fps=24)
    audio = AudioFileClip(tts_path)
    if audio.duration > clip.duration:
        clip = clip.loop(duration=audio.duration)
    else:
        audio = audio.subclip(0, clip.duration)

    final = clip.set_audio(audio)
    final.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac', logger=None)

    st.success("✅ VIDEO CINE 1080p CON AUDIO - COMO EL QUE MANDASTE")
    st.video(video_path)
    with open(video_path,"rb") as f:
        st.download_button("⬇️ DESCARGAR VIDEO FINAL", f, "drama_rd_cine.mp4", "video/mp4", use_container_width=True)
    st.balloons()
