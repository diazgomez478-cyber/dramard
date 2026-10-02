import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance
import imageio.v2 as imageio
import requests, io, random, urllib.parse

st.set_page_config(page_title="DRAMA RD V34")
st.title("DRAMA RD - V34 - 30s POR ESCENA")
st.success("3 escenas x 30s = 90s total")

guion = st.text_area("Guion (3 frases)", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.", height=90)

PROMPTS = [
    "Dominican woman 30 years furious crying angry courtroom close up cinematic",
    "Dominican mother happy hugging two children courtroom victory cinematic warm light",
    "Dominican man 40 years furious throwing money champagne luxury penthouse night"
]

def get_img(prompt):
    try:
        seed = random.randint(1,999999)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=640&height=360&seed={seed}&nologo=true&model=flux"
        r = requests.get(url, timeout=60)
        if len(r.content) > 5000:
            img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((640,360))
            return ImageEnhance.Contrast(img).enhance(1.2)
    except:
        pass
    return Image.new('RGB',(640,360),(40,40,50))

def add_bar(img, texto, escena, seg_escena):
    W,H = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,32], fill=(0,0,0))
    d.rectangle([0,H-45,W,H], fill=(0,0,0))
    d.text((8,6), f"ESC {escena} | {seg_escena}s / 30s", fill="gold")
    d.text((W//2, H-22), texto[:50].upper(), fill="white", anchor="mm")
    # barra progreso de la escena
    d.rectangle([0, H-5, int(W * seg_escena / 30), H], fill="gold")
    return img

if st.button("🎬 CREAR VIDEO 30s x ESCENA", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:3]
    while len(frases) < 3:
        frases.append(frases[-1])

    FPS = 10 # 10 fps x 30s = 300 frames por escena (no crashea)
    SEG_POR_ESCENA = 30
    FRAMES_POR_ESCENA = FPS * SEG_POR_ESCENA
    out = "/tmp/drama_30s_escena.mp4"

    st.write("🎥 Filmando 90 segundos totales...")
    prog = st.progress(0)

    writer = imageio.get_writer(out, fps=FPS, macro_block_size=1)

    for i in range(3):
        st.write(f"Escena {i+1}/3 - 30 segundos")
        base = get_img(PROMPTS[i])
        st.image(base, caption=f"Escena {i+1} -
