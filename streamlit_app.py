import streamlit as st, requests, io, random, urllib.parse, os, textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip

st.set_page_config(page_title="DRAMA RD CINE", page_icon="🎬")
st.title("🎬 DRAMA RD - CINE REAL 1080p")
st.caption("🇩🇴 Como el video que mandaste - con subtitulos y audio")

# Historia como la del video que mandaste
guion = st.text_area("Guion (pon tu historia)", 
"""Son veinticinco años de matrimonio. A mi defendida le toca la mitad.
Luisa buscó un abogado y lo demandó por no compartir su dinero.
Hipolito teniendo cien millones en su cuenta, por qué no ayuda a su familia?
Porque ese dinero es solo mio. Yo me lo gané con mi sudor.
Este tribunal falla a favor de la mujer y los niños. 50 millones para Luisa.
Hipolito furioso decidió GASTAR TODO su dinero en lujos, mujeres y fiestas.
Para que no le quedara nada a su familia.""")

def get_cinematic(prompt, w=1920, h=1080):
    for _ in range(6):
        try:
            seed = random.randint(1,999999)
            # Prompt mejorado para que no salga tieso
            full = f"{prompt}, cinematic movie still, dramatic lighting, 8k, photorealistic, film grain, courtroom drama"
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full)}?width={w}&height={h}&seed={seed}&nologo=true&enhance=true"
            r = requests.get(url, timeout=90, headers={"User-Agent":"Mozilla/5.0"})
            if len(r.content) > 15000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((1920,1080))
        except: pass
    return None

def add_subtitle(img, text):
    # Pone subtitulos blancos abajo como en tu video
    draw = ImageDraw.Draw(img)
    W, H = img.size
    # fondo negro semitransparente
    draw.rectangle([0, H-180, W, H], fill=(0,0,0,180))
    # texto
    wrapped = textwrap.wrap(text, width=60)
    y = H-160
    for line in wrapped[:3]:
        draw.text((W//2, y), line, fill="white", anchor="mm", 
                  stroke_width=2, stroke_fill="black", font=ImageFont.load_default())
        y+=35
    return img

def ken_burns(img, frames=70):
    w,h = img.size
    out=[]
    for i in range(frames):
        zoom = 1.0 + (i/frames)*0.3
        nw, nh = int(w*zoom), int(h*zoom)
        resized = img.resize((nw, nh), Image.LANCZOS)
        # movimiento suave
        left = int((nw-w) * (i/frames) * 0.5)
        top = int((nh-h) * 0.3)
        crop = resized.crop((left, top, left+w, top+h))
        out.append(np.array(crop))
    return out

if st.button("🔥 CREAR VIDEO CINE CON AUDIO", use_container_width=True):
    escenas = [
        ("Juez en tribunal gritando, dominican judge angry, black robe, courtroom", "Son veinticinco años de matrimonio. A mi defendida le toca la mitad."),
        ("Mujer dominicana llorando con dos niños abrazados, triste, lagrimas, cinematic", "LUISA buscó un abogado y lo demandó por no compartir su dinero. Prefiere el divorcio."),
        ("Juez viejo serio en estrado, wooden courtroom, dramatic", "Hipolito, teniendo usted 100 millones en su cuenta, por qué no ayuda a su propia familia?"),
        ("Hombre rico dominicano traje marron gritando en corte, furioso", "Porque ese dinero es solo mio señoria, yo me lo gane con mi sudor, ella no trabajo nada."),
        ("Mujer llorando abrazando niños, final feliz, cinematic", "Este tribunal falla a favor de la mujer y los niños. Se le otorga la mitad, 50 millones para Luisa."),
        ("Hombre con dinero, fiesta, mujeres, champan, carro deportivo, noche", "HIPOLITO furioso, decidió GASTAR TODO su dinero en lujos, mujeres y fiestas...")
    ]

    imgs=[]
    for i,(prompt, texto) in enumerate(escenas):
        st.write(f"Escena {i+1}/6: {texto[:40]}...")
        img = get_cinematic(prompt)
        if img:
            img = add_subtitle(img.copy(), texto)
            imgs.append((img, texto))
            st.image(img, use_container_width=True)

    if len(imgs) < 3:
        st.error("Pollinations lento, dale de nuevo en 1 min")
    else:
        # Crear video con movimiento
        all_frames=[]
        for img, txt in imgs:
            all_frames.extend(ken_burns(img, 60))

        # Audio
        audio_path="/tmp/full_audio.mp3"
        full_text = " ".join([t for _, t in imgs])
        tts = gTTS(text=full_text[:800], lang='es', tld='com.mx', slow=False)
        tts.save(audio_path)

        video_path="/tmp/cine_final.mp4"
        clip = ImageSequenceClip(all_frames, fps=24)
        audio = AudioFileClip(audio_path)
        if audio.duration > clip.duration:
            clip = clip.loop(duration=audio.duration)
        final = clip.set_audio(audio)
        final.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac', logger=None)

        st.success("✅ ¡VIDEO CINE LISTO! Como el que mandaste")
        st.video(video_path)
        with open(video_path,"rb") as f:
            st.download_button("⬇️ DESCARGAR VIDEO 1080p CON AUDIO", f, "drama_cine_1080p.mp4", "video/mp4", use_container_width=True)
        st.balloons()
