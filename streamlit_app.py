import streamlit as st, urllib.parse, random, requests, io
from PIL import Image

st.set_page_config(page_title="DRAMA RD", page_icon="🎬")
st.title("🎬 DRAMA RD - VIDEO QUE SI ABRE")
st.caption("🇩🇴 Victor el natural")

tema = st.text_input("Tema", "Trump el terror de la casa blanca")
prota = st.text_input("Prota", "Victor el natural")

if st.button("🔥 CREAR VIDEO"):
    imgs=[]
    for i in range(3):
        st.write(f"Creando escena {i+1}/3...")
        try:
            url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(f'dominican man {prota} {tema} cinematic') }?width=512&height=768&seed={random.randint(1,99999)}&nologo=true"
            r=requests.get(url,timeout=60)
            img=Image.open(io.BytesIO(r.content)).convert("RGB").resize((512,768))
            st.image(img, caption=f"Escena {i+1}")
            imgs.append(img)
        except Exception as e:
            st.write(f"Error escena {i+1}: {e}")

    if imgs:
        # CREAR GIF - ESTE SI ABRE SIEMPRE EN EL CELULAR
        gif_path="/tmp/drama.gif"
        imgs[0].save(gif_path, save_all=True, append_images=imgs[1:], duration=1500, loop=0)
        st.success("✅ ¡VIDEO CREADO! ¡Este SI abre!")
        st.image(gif_path, caption="Tu video drama - Si no reproduce dale a descargar")

        with open(gif_path,"rb") as f:
            st.download_button("⬇️ DESCARGAR VIDEO (GIF)", f, file_name="drama_rd.gif", mime="image/gif", use_container_width=True)

        # Intentar MP4 tambien
        try:
            import imageio.v2 as imageio, numpy as np
            mp4_path="/tmp/drama.mp4"
            frames=[]
            for im in imgs:
                arr=np.array(im)
                for _ in range(15): frames.append(arr)
            imageio.mimsave(mp4_path, frames, fps=10)
            st.video(mp4_path)
            with open(mp4_path,"rb") as f:
                st.download_button("⬇️ DESCARGAR MP4", f, file_name="drama_rd.mp4", mime="video/mp4")
        except:
            st.info("MP4 no disponible, pero el GIF de arriba ES tu video. Descárgalo y súbelo a CapCut.")
        st.balloons()
