import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
import imageio.v2 as imageio
import requests, io, random, urllib.parse, time
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD V31")
st.title("DRAMA RD - V31 CON DURACION")
st.success("Elige cuanto dura tu pelicula!")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.", height=100)

# AQUI ELIGES 1, 2 o 3 MINUTOS
col1, col2 = st.columns(2)
with col1:
    duracion_min = st.selectbox("¿Cuanto debe durar?", [1, 2, 3], index=0)
with col2:
    st.metric("Duracion total", f"{duracion_min} minuto(s)", f"{duracion_min*60} seg")

PROMPTS = [
    "Dominican woman 30 years furious crying angry close up face tears courtroom, cinematic dramatic movie lighting, Netflix drama",
    "Dominican mother 30 years hugging two children happy crying joy courtroom warm light cinematic movie",
    "Dominican man 40 years furious angry throwing money champagne luxury penthouse night villain cinematic"
]

def get_pelicula(prompt):
    for _ in range(4):
        try:
            seed = random.randint(1,999999)
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=576&seed={seed}&nologo=true&model=flux&enhance=true"
            r = requests.get(url, timeout=90)
            if len(r.content) > 15000:
                img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720), Image.LANCZOS)
                img = ImageEnhance.Contrast(img).enhance(1.2)
                return img
        except:
            time.sleep(1)
    return Image.new('RGB',(1280,720),(20,20,30))

def add_cine_bars(img, texto, escena, tiempo_actual, tiempo_total):
    W,H = img.size
    draw = ImageDraw.Draw(img)
    draw.rectangle([0,0,W,70], fill=(0,0,0))
    draw.rectangle([0,H-110,W,H], fill=(0,0,0))
    draw.rectangle([0,70,W,72], fill=(255,215,0))
    draw.text((30,15), f"DRAMA RD - {tiempo_actual}/{tiempo_total} - ESC {escena}", fill=(255,215,0))
    draw.text((W//2+2, H-62+2), texto.upper()[:60], fill="black", anchor="mm")
    draw.text((W//2, H-62), texto.upper()[:60], fill="white", anchor="mm")
    # Barra progreso abajo
    progreso = int((tiempo_actual / tiempo_total * W)) if tiempo_total>0 else 0
    draw.rectangle([0, H-10, progreso, H], fill=(255,215,0))
    return img

if st.button(f"🎬 CREAR VIDEO DE {duracion_min} MINUTO(S)", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()]
    while len(frases) < 3:
        frases.append(frases[-1] if frases else "Drama en RD")
    frases = frases[:3]

    FPS = 20
    TOTAL_SEGUNDOS = duracion_min * 60
    TOTAL_FRAMES = TOTAL_SEGUNDOS * FPS
    FRAMES_POR_ESCENA = TOTAL_FRAMES // 3

    st.write(f"🎥 Creando video de {TOTAL_SEGUNDOS} segundos = {TOTAL_FRAMES} frames...")
    video_frames = []
    progress = st.progress(0)

    for i in range(3):
        img_base = get_pelicula(PROMPTS[i])
        st.image(img_base, caption=f"Escena {i+1} - durara {TOTAL_SEGUNDOS//3} seg", use_container_width=True)

        # Cada escena dura lo que toca para completar 1,2,3 min
        for f in range(FRAMES_POR_ESCENA):
            seg_actual = (i * FRAMES_POR_ESCENA + f) // FPS
            img_con_texto = add_cine_bars(img_base.copy(), frases[i], i+1, seg_actual, TOTAL_SEGUNDOS)
            video_frames.append(np.array(img_con_texto))

        progress.progress((i+1)/3)

    out = f"/tmp/drama_{duracion_min}min.mp4"
    imageio.mimsave(out, video_frames, fps=FPS, macro_block_size=1)

    try:
        # Audio repite para llenar 1,2,3 minutos
        texto_audio = (". ".join(frases) + ". ") * duracion_min
        ap = "/tmp/audio.mp3"
        gTTS(text=texto_audio, lang='es', tld='com.mx').save(ap)
        st.audio(ap)
    except:
        pass

    with open(out,"rb") as f:
        vbytes = f.read()

    st.success(f"✅ VIDEO DE {duracion_min} MINUTO(S) LISTO - {len(video_frames)} frames!")
    st.video(vbytes)
    st.download_button(f"⬇️ DESCARGAR VIDEO {duracion_min} MIN", vbytes, f"drama_rd_{duracion_min}min.mp4", "video/mp4", use_container_width=True)
    st.balloons()
