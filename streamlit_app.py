import streamlit as st
import requests, urllib.parse, random, io
from PIL import Image

st.set_page_config(page_title="VIDEO RD 55s", layout="centered")
st.title("Solo actuación (sin gTTS)")
st.write("Video real con movimiento, sin voz de robot.")

idea = st.selectbox("Elige tu drama:", (
    "Luisa demanda a Hipolito por 100 millones",
    "El error en producción un viernes a las 5 PM",
    "La guerra de los Pull Requests"
))

prompt_base = st.text_area("Describe la actuación:", value="Dominican woman Luisa crying shouting in courtroom, then happy hugging kids winning, then angry Dominican man spending money in luxury club, cinematic acting", height=120)

def generar_imagen_robusta(prompt):
    for intento in range(5): # intenta 5 veces hasta que salga
        seed = random.randint(1,999999)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={seed}&nologo=true&model=flux&enhance=true"
        try:
            r = requests.get(url, timeout=30)
            if len(r.content) < 5000: # si es muy chiquita es error, reintenta
                continue
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            return img, r.content
        except Exception:
            continue
    return None, None

if st.button("🚀 GENERAR VIDEO 55s REAL", type="primary", use_container_width=True):
    with st.spinner("Filmando 55s... si falla una escena reintenta automático"):
        for i in range(3):
            prompt = f"{idea} {prompt_base} scene {i+1} vertical 9:16 photorealistic 4k Dominican acting"
            img, img_bytes = generar_imagen_robusta(prompt)
            
            if img is None:
                st.error(f"Escena {i+1} falló por saturación, dale al botón otra vez. Pollinations está lleno.")
            else:
                st.subheader(f"Escena {i+1} / 3 - 18s")
                st.image(img, use_container_width=True)
                st.download_button(f"⬇️ Guardar escena {i+1}", img_bytes, f"escena_{i+1}.jpg", "image/jpeg", key=f"dl_{i}_{random.randint(1,9999)}")

        st.success("¡VIDEO 55s LISTO! Guarda las 3 y únelas en CapCut")
        st.balloons()

st.caption("Si sale error 2 bytes es que Pollinations está saturado. Espera 10 seg y dale de nuevo.")
