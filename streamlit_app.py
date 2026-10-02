import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance
import imageio.v2 as imageio
import requests, io, random, urllib.parse

st.set_page_config(page_title="DRAMA RD V36")
st.title("DRAMA RD V36 MOVIL 30s")
st.success("30s por escena = 90s total - 9:16")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.")

PROMPTS = [
    "Dominican woman furious crying courtroom cinematic vertical",
    "Dominican mother hugging children happy courtroom cinematic",
    "Dominican man furious throwing money champagne penthouse night cinematic"
]

def get_vertical(prompt):
    try:
        seed = random.randint(1, 999999)
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) + "?width=360&height=640&seed=" + str(seed) + "&nologo=true&model=flux"
        r = requests.get(url, timeout=60)
        if len(r.content) > 4000:
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            img = img.resize((360, 640))
            return ImageEnhance.Contrast(img).enhance(1.15)
    except:
        pass
    return Image.new("RGB", (360, 640), (35, 35, 45))

def add_text(img, texto, escena, seg):
    W, H = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 38], fill=(0, 0, 0))
    d.rectangle([0, H-70, W, H], fill=(0, 0, 0))
    d.text((8, 8), "ESC " + str(escena) + " " + str(seg) + "s/30s", fill="gold")
    d.text((W//2, H-40), texto[:30].upper(), fill="white", anchor="mm")
    d.rectangle([0, H-4, int(W*seg/30), H], fill="gold")
    return img

if st.button("CREAR VIDEO 90s", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:3]
    while len(frases) < 3:
        frases.append(frases[-1])

    FPS = 8
    SEG = 30
    FRAMES = FPS * SEG
    out = "/tmp/drama_v36.mp4"

    st.write("Creando 90 segundos...")
    bar = st.progress(0)

    writer = imageio.get_writer(out, fps=FPS, macro_block_size=1)

    for i in range(3):
        base = get_vertical(PROMPTS[i])
        st.image(base, caption="Escena " + str(i+1), use_container_width=True)
        for f in range(FRAMES):
            seg = f // FPS
            frame = add_text(base.copy(), frases[i], i+1, seg)
            writer.append_data(frame)
        bar.progress((i+1)/3)

    writer.close()

    with open(out, "rb") as f:
        vb = f.read()

    st.success("VIDEO LISTO 90s")
    st.video(vb)
    st.download_button("DESCARGAR", vb, "drama_90s.mp4", "video/mp4", use_container_width=True)
    st.balloons()
