import streamlit as st, urllib.parse, random, requests, io, time
from PIL import Image
import numpy as np

st.set_page_config(page_title="DRAMA RD FINAL", page_icon="🎬")
st.title("🎬 DRAMA RD - FINAL")
st.caption("🇩🇴 Sin errores - Victor el natural")

tema = st.text_input("Tema", "Trump el terror de la casa blanca")
prota = st.text_input("Prota", "Victor el natural")

if st.button("🔥 CREAR VIDEO"):
    imgs=[]
    for i in range(3):
        st.write(f"Creando escena {i+1}/3...")
        try:
            prompt=f"cinematic photo dominican man {prota} {tema}"
            url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=512&height=768&seed={random.randint(1,99999)}&nologo=true"
            r=requests.get(url,timeout=60)
            img=Image.open(io.BytesIO(r.content)).convert("RGB")
            st.image(img, caption=f"Escena {i+1}")
            imgs.append(img)
        except:
            time.sleep(2)
    if imgs:
        import imageio.v2 as imageio
        path="/tmp/final.mp4"
        frames=[]
        for im in imgs:
            arr=np.array(im.resize((512,768)))
            for _ in range(20):
                frames.append(arr)
        imageio.mimsave(path, frames, fps=10)
        st.success("VIDEO LISTO!")
        st.video(path)
        with open(path,"rb") as f:
            st.download_button("⬇️ DESCARGAR", f, file_name="drama.mp4", mime="video/mp4")
        st.balloons()
