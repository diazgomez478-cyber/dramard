import streamlit as st, urllib.parse, random, requests, io, time, os
from PIL import Image
import numpy as np
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip

st.set_page_config(page_title="DRAMA RD 1080p", page_icon="🎬")
st.title("🎬 DRAMA RD - 1080p + AUDIO")
st.caption("🇩🇴 Victor el natural - Full HD")

tema = st.text_area("Tema / Guion para audio", "Trump el terror de la casa blanca. Victor el natural te cuenta la verdad sin censura.")
prota = st.text_input("Protagonista", "Victor el natural")

def get_img(prompt):
    for _ in range(5):
        try:
            # 1080p = 1920x1080
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1920&height=1080&seed={random.randint(1,999999)}&nologo=true&enhance=true"
            r = requests.get(url, timeout=90, headers={"User-Agent":"Mozilla/5.0"})
            if len(r.content) > 15000:
                img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((1920,1080))
                return img
        except:
            time.sleep(2)
    return None

def zoom_frames(img, num_frames=80):
    w,h = img.size
    frames=[]
    for i in range(num_frames):
        zoom = 1 + (i/num_frames)*0.25
        nw, nh = int(w*zoom), int(h*zoom)
        resized = img.resize((nw, nh), Image.LANCZOS)
        left = (nw - w)//2
        top = (nh - h)//2
        cropped = resized.crop((left, top, left+w, top+h))
        frames.append(np.array(cropped))
    return frames

if st.button("🔥 CREAR VIDEO 1080p CON AUDIO", use_container_width=True):
    imgs=[]
    bar = st.progress(0)
    for i in range(3):
        st.write(f"Generando escena {i+1}/3 en 1080p...")
        img = get_img(f"dominican man {prota}, {tema}, scene {i+1}, cinematic 8k ultra detailed, dramatic lighting")
        if img:
            imgs.append(img)
            st.image(img, caption=f"Escena {i+1} - 1920x1080", use_container_width=True)
        bar.progress((i+1)/3)

    if not imgs:
        st.error("Servidor ocupado, espera 30 seg")
    else:
        while len(imgs)<3: imgs.append(imgs[-1])

        # 1. Crear frames con zoom para 1080p
        st.write("Creando movimiento...")
        all_frames=[]
        for im in imgs:
            all_frames.extend(zoom_frames(im, 60))

        # 2. Crear audio con tu guion
        st.write("Generando audio...")
        tts_path = "/tmp/audio.mp3"
        try:
            tts = gTTS(text=f"{prota}. {tema}", lang='es', tld='com.mx') # voz latina
            tts.save(tts_path)
        except Exception as e:
            st.warning(f"Audio fallo, video sin audio: {e}")
            tts_path = None

        # 3. Crear video 1080p
        video_path = "/tmp/drama_1080.mp4"
        clip = ImageSequenceClip(all_frames, fps=24)
        
        if tts_path and os.path.exists(tts_path):
            audio = AudioFileClip(tts_path)
            # Si el audio es mas largo que el video, alargar video
            if audio.duration > clip.duration:
                clip = clip.loop(duration=audio.duration)
            else:
                audio = audio.subclip(0, clip.duration)
            final_clip = clip.set_audio(audio)
            final_clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac', logger=None)
        else:
            clip.write_videofile(video_path, fps=24, codec='libx264', logger=None)

        st.success("✅ ¡VIDEO 1080p CON AUDIO LISTO!")
        st.video(video_path)

        with open(video_path, "rb") as f:
            st.download_button("⬇️ DESCARGAR VIDEO 1080p HD", f, file_name="drama_rd_1080p.mp4", mime="video/mp4", use_container_width=True)
        
        st.balloons()
        st.info("💡 Tip: Súbelo a TikTok, ya está en 1920x1080 Full HD con audio")
