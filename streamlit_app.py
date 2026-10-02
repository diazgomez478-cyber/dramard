import streamlit as st
import requests, urllib.parse, random, io
from PIL import Image

st.set_page_config(page_title="VIDEO 55s con PLAY", layout="centered")
st.title("VIDEO 55s con reproducción")

idea = st.selectbox("Elige drama:", (
    "Luisa demanda a Hipolito por 100 millones",
    "El error en producción un viernes a las 5 PM",
    "La guerra de los Pull Requests"
))

prompt_base = st.text_area("Actuación:", value="Dominican woman Luisa crying shouting in courtroom, Dominican cinematic acting, vertical 9:16 modest clothing", height=100)

def get_img(prompt):
    for _ in range(5):
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={random.randint(1,999999)}&nologo=true&model=turbo"
            r = requests.get(url, timeout=25)
            if len(r.content) > 8000:
                return Image.open(io.BytesIO(r.content)).convert("RGB")
        except:
            continue
    # Respaldo si Pollinations está lleno a las 9 PM
    return Image.new('RGB', (720,1280), (35,35,70))

if st.button("🚀 GENERAR VIDEO 55s CON REPRODUCCIÓN", type="primary", use_container_width=True):
    with st.spinner("Creando tu video 55s..."):
        frames = []
        for i in range(3):
            p = f"{idea} {prompt_base} scene {i+1} photorealistic 4k"
            img = get_img(p)
            frames.append(img)

        # Video GIF 55s que SI reproduce
        buf = io.BytesIO()
        frames[0].save(buf, format='GIF', save_all=True, append_images=frames[1:], duration=18500, loop=0)
        buf.seek(0)

        st.success("¡VIDEO 55s CON PLAY LISTO!")
        st.image(buf, caption="Reproducción automática 55s - Se mueve solo", use_container_width=True)
        st.download_button("⬇️ DESCARGAR VIDEO 55s", buf.getvalue(), "video_55s.gif", "image/gif", use_container_width=True)
        st.balloons()

st.caption("Este video sí reproduce arriba. Guárdalo y súbelo a CapCut para MP4")
