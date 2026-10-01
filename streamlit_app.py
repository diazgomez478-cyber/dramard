import streamlit as st, urllib.parse, random, requests, io, time
from PIL import Image
import imageio.v2 as imageio
import numpy as np

st.set_page_config(page_title="DRAMA RD", page_icon="🎬")
st.title("🎬 DRAMA RD - PLAY REAL")
st.caption("Victor - Este video SI reproduce")

tema = st.text_input("Tema", "Trump el terror de la casa blanca")
prota = st.text_input("Prota", "Victor el natural")

def get_img(p):
    for _ in range(5):
        try:
            seed = random.randint(1,999999)
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=512&height=768&seed={seed}&nologo=true&enhance=true"
            r = requests.get(url, timeout=90, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200 and len(r.content)>8000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((512,768))
        except: time.sleep(2)
    return None

if st.button("🔥 CREAR VIDEO CON PLAY", use_container_width=True):
    imgs=[]
    for i in range(3):
        st.write(f"Creando escena {i+1}/3...")
        img = get_img(f"dominican man {prota}, {tema}, dramatic scene {i+1}, cinematic")
        if img:
            imgs.append(img)
            st.image(img, caption=f"Escena {i+1} lista")

    if len(imgs)==0:
        st.error("Pollinations ocupado, espera 30 seg y dale de nuevo")
    else:
        while len(imgs)<3: imgs.append(imgs[-1])
        
        mp4_path="/tmp/drama.mp4"
        # 30 frames por imagen = video de 6 segundos
        frames=[]
        for im in imgs:
            arr=np.array(im)
            for _ in range(20): frames.append(arr)
            
        imageio.mimsave(mp4_path, frames, fps=8, macro_block_size=1)
        
        st.success("✅ ¡VIDEO LISTO!")
        st.video(mp4_path) # <--- ESTE SI TIENE BOTON DE PLAY
        
        with open(mp4_path,"rb") as f:
            st.download_button("⬇️ DESCARGAR VIDEO MP4 QUE REPRODUCE", f, file_name="drama_rd.mp4", mime="video/mp4", use_container_width=True)
        st.balloons()
