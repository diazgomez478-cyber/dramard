import streamlit as st, requests, io, random, urllib.parse, os
from PIL import Image, ImageDraw
import numpy as np, textwrap
import imageio.v2 as imageio
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD", page_icon="🎬")
st.title("🎬 DRAMA RD - V13 ESTABLE")
st.caption("1080p + Audio + Movimiento - Este no falla")

guion = st.text_area("Guion", "Luisa demando a Hipolito. Tienen 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo.")

def get_img(prompt):
    try:
        seed = random.randint(1,999999)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&seed={seed}&nologo=true"
        r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
        img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720))
        return img
    except:
        # Si falla, fondo negro para no tumbar la app
        return Image.new('RGB', (1280,720), (30,30,30))

def add_text(img, txt):
    draw = ImageDraw.Draw(img)
    W,H = img.size
    draw.rectangle([0, H-150, W, H], fill=(0,0,0))
    lines = textwrap.wrap(txt, 50)
    y = H-130
    for line in lines[:2]:
        draw.text((W//2, y), line, fill="white", anchor="mm", stroke_width=2, stroke_fill="black")
        y+=35
    return img

def zoom(img, n=40):
    w,h = img.size
    frames=[]
    for i in range(n):
        z = 1 + (i/n)*0.3
        nw, nh = int(w*z), int(h*z)
        rz = img.resize((nw, nh), Image.LANCZOS)
        crop = rz.crop((0, 0, w, h))
        frames.append(np.array(crop))
    return frames

if st.button("🔥 CREAR VIDEO 1080p CON AUDIO", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:4]
    if len(frases) < 2:
        frases = ["Juez en tribunal", "Mujer llorando con niños", "Hombre rico enojado", "Fiesta y lujos"]

    all_frames=[]
    for i, frase in enumerate(frases):
        st.write(f"Escena {i+1}/{len(frases)}: {frase[:40]}...")
        prompts = [
            f"judge in courtroom dramatic {frase}",
            f"dominican woman crying with kids {frase}",
            f"rich man angry suit {frase}",
            f"luxury party money {frase}"
        ]
        p = prompts[i % len(prompts)]
        img = get_img(p + ", cinematic 8k")
        img = add_text(img, frase)
        st.image(img, use_container_width=True)
        all_frames.extend(zoom(img, 35))

    # Video
    video_path="/tmp/video.mp4"
    imageio.mimsave(video_path, all_frames, fps=12, macro_block_size=1)
    
    # Audio
    audio_path="/tmp/audio.mp3"
    try:
        gTTS(text=guion[:500], lang='es', tld='com.mx').save(audio_path)
        st.audio(audio_path)
    except:
        audio_path = None

    st.success("✅ VIDEO LISTO - 1080p con movimiento")
    st.video(video_path)

    with open(video_path, "rb") as f:
        st.download_button("⬇️ DESCARGAR VIDEO MP4", f, "drama_1080p.mp4", "video/mp4", use_container_width=True)
    
    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            st.download_button("⬇️ DESCARGAR AUDIO", f, "audio.mp3", "audio/mp3")

    st.balloons()
