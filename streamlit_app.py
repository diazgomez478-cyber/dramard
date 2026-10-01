import streamlit as st, urllib.parse, random, requests, io, time
from PIL import Image

st.set_page_config(page_title="DRAMA RD", page_icon="🎬")
st.title("🎬 DRAMA RD - V6")
st.caption("🇩🇴 Victor el natural - No falla")

tema = st.text_input("Tema", "Trump el terror de la casa blanca")
prota = st.text_input("Prota", "Victor el natural")

def crear_imagen(prompt, intento=0):
    try:
        seed = random.randint(1,999999)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=512&height=768&seed={seed}&nologo=true&nofeed=true"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=90)
        if r.status_code == 200 and len(r.content) > 5000:
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            return img.resize((512,768))
    except Exception as e:
        print(f"Error: {e}")
    return None

if st.button("🔥 CREAR VIDEO", use_container_width=True):
    imgs=[]
    progress = st.progress(0)
    for i in range(3):
        st.write(f"Creando escena {i+1}/3...")
        img = None
        for intento in range(3): # 3 intentos por escena
            p = f"dominican man {prota}, {tema}, scene {i+1}, cinematic dramatic lighting, 8k"
            img = crear_imagen(p, intento)
            if img:
                break
            time.sleep(2)

        if img:
            st.image(img, caption=f"Escena {i+1} OK")
            imgs.append(img)
        else:
            st.warning(f"Escena {i+1} falló, usando anterior")
            if imgs: imgs.append(imgs[-1]) # duplica la anterior si falla

        progress.progress((i+1)/3)

    if len(imgs) >= 1:
        # Asegurar 3 imagenes
        while len(imgs) < 3:
            imgs.append(imgs[0])

        gif_path="/tmp/drama.gif"
        imgs[0].save(gif_path, save_all=True, append_images=imgs[1:], duration=1200, loop=0)
        st.success("✅ ¡VIDEO CREADO! ¡Este SI abre!")
        st.image(gif_path)
        with open(gif_path,"rb") as f:
            st.download_button("⬇️ DESCARGAR VIDEO", f, file_name="drama_rd.gif", mime="image/gif", use_container_width=True)
        st.balloons()
    else:
        st.error("Pollinations está saturado, dale a CREAR VIDEO de nuevo en 30 seg")
