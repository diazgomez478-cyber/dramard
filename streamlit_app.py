import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance
import requests
import io
import random
import urllib.parse
import numpy as np
import imageio.v2 as imageio

st.set_page_config(page_title="DRAMA RD FINAL", layout="centered")
st.title("📱 DRAMA RD - FINAL")
st.success("30 segundos por escena - 90 segundos total - Vertical 9:16")

guion = st.text_area(
    "Escribe tu guion (3 frases separadas por punto)", 
    "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.",
    height=100
)

PROMPTS = [
    "Dominican woman 30 years old furious crying angry courtroom close up vertical cinematic movie lighting",
    "Dominican mother 30 years old happy hugging two children courtroom victory warm light vertical cinematic",
    "Dominican man 40 years old furious angry throwing money champagne luxury penthouse night vertical cinematic villain"
]

def get_vertical_image(prompt):
    try:
        seed = random.randint(1, 999999)
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) + "?width=360&height=640&seed=" + str(seed) + "&nologo=true&model=flux"
        r = requests.get(url, timeout=90)
        if len(r.content) > 4000:
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            img = img.resize((360, 640))
            img = ImageEnhance.Contrast(img).enhance(1.15)
            img = ImageEnhance.Color(img).enhance(1.1)
            return img
    except Exception as e:
        st.warning("Reintentando imagen...")
    return Image.new("RGB", (360, 640), (40, 40, 55))

def add_text_and_convert(img, texto, escena_num, seg_en_escena):
    W, H = img.size
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 38], fill=(0, 0, 0))
    draw.rectangle([0, H-70, W, H], fill=(0, 0, 0))
    draw.text((8, 8), "ESC " + str(escena_num) + " - " + str(seg_en_escena) + "s / 30s", fill=(255, 215, 0))
    draw.text((W//2, H-42), texto[:32].upper(), fill="white", anchor="mm")
    draw.text((W//2, H-20), texto[32:64].upper(), fill="white", anchor="mm")
    progress_width = int(W * seg_en_escena / 30)
    draw.rectangle([0, H-5, progress_width, H], fill=(255, 215, 0))
    return np.array(img)

if st.button("🎬 CREAR VIDEO 90 SEGUNDOS - 30s x ESCENA", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()]
    while len(frases) < 3:
        frases.append(frases[-1] if frases else "Drama en RD")
    frases = frases[:3]

    FPS = 8
    SEG_POR_ESCENA = 30
    FRAMES_POR_ESCENA = FPS * SEG_POR_ESCENA
    OUTPUT_PATH = "/tmp/drama_final_90s.mp4"

    st.info("Filmando 90 segundos - 3 escenas de 30s cada una...")
    progress_bar = st.progress(0)
    status_text = st.empty()

    writer = imageio.get_writer(OUTPUT_PATH, fps=FPS, macro_block_size=1)

    for escena_idx in range(3):
        status_text.write("Generando escena " + str(escena_idx+1) + "/3 - " + frases[escena_idx][:40] + "...")
        base_image = get_vertical_image(PROMPTS[escena_idx])
        st.image(base_image, caption="Escena " + str(escena_idx+1) + " - " + frases[escena_idx][:50], use_container_width=True)

        for frame_idx in range(FRAMES_POR_ESCENA):
            seg_actual = frame_idx // FPS
            frame_array = add_text_and_convert(base_image.copy(), frases[escena_idx], escena_idx+1, seg_actual)
            writer.append_data(frame_array)

        progress_bar.progress((escena_idx + 1) / 3)

    writer.close()
    status_text.write("¡Video terminado!")

    with open(OUTPUT_PATH, "rb") as f:
        video_bytes = f.read()

    st.success("✅ VIDEO LISTO - 90 SEGUNDOS - 30s POR ESCENA - VERTICAL 9:16")
    st.video(video_bytes)
    st.download_button(
        "⬇️ DESCARGAR VIDEO PARA TIKTOK 90s",
        video_bytes,
        "drama_rd_90s_30s_por_escena.mp4",
        "video/mp4",
        use_container_width=True
    )
    st.balloons()
