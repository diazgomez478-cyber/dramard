import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance
import imageio.v2 as imageio
import requests, io, random, urllib.parse, time
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD V32")
st.title("DRAMA RD - V32 ESTABLE")
st.success("Ahora si aguanta 1,2,3 minutos sin crashear!")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.", height=100)

duracion_min = st.selectbox("¿Cuantos minutos?", [1, 2, 3], index=0)
st.info(f"Vas a crear video de {duracion_min} minuto(s) = {duracion_min*60} segundos")

PROMPTS = [
    "Dominican woman furious crying courtroom close up cinematic movie",
    "Dominican mother hugging two children happy courtroom cinematic",
    "Dominican man furious throwing money champagne penthouse night cinematic"
]

def get_img(prompt):
    try:
        seed = random.randint(1,999999)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=640&height=360&seed={seed}&nologo=true&model=flux"
        r = requests.get(url, timeout=60)
        if len(r.content) > 8000:
            img = Image.open(io.BytesIO(r.content)).convert("RGB").resize((640,360))
            return ImageEnhance.Contrast(img).enhance(1.15)
    except:
        pass
    return Image.new('RGB',(640,360),(30,30,40))

def add_text(img, txt, escena, sec_actual, sec_total):
    W,H = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,35], fill=(0,0,0))
    d.rectangle([0,H-50,W,H], fill=(0,0,0))
    d.text((10,5), f"DRAMA RD {sec_actual}s/{sec_total}s ESC{escena}", fill="gold")
    d.text((W//2, H-25), txt[:50].upper(), fill="white", anchor="mm")
    # barra progreso
    prog = int(W * sec_actual / sec_total) if sec_total>0 else 0
    d.rectangle([0,H-5,W,H], fill=(50,50,50))
    d.rectangle([0,H-5,prog,H], fill=(255,215,0))
    return img

if st.button(f"🎬 CREAR VIDEO DE {duracion_min} MIN", type="primary", use_container_width=True):
    frases = [f.strip() for f in guion.split(".") if f.strip()][:3]
    while len(frases) < 3:
        frases.append(frases[-1])

    FPS = 12 # menos fps = menos memoria
    TOTAL_SEG = duracion_min * 60
    FRAMES_ESCENA = (TOTAL_SEG * FPS) // 3
    out_path = f"/tmp/drama_{duracion_min}min.mp4"

    st.write(f"Filmando {TOTAL_SEG} segundos...")
    prog_bar = st.progress(0)

    # ESCRITURA DIRECTA - no guarda en memoria
    writer = imageio.get_writer(out_path, fps=FPS, macro_block_size=1)

    for i in range(3):
        img_base = get_img(PROMPTS[i])
        st.image(img_base, caption=f"Escena {i+1}", use_container_width=True)
        for f_idx in range(FRAMES_ESCENA):
            sec_actual = (i*FRAMES_ESCENA + f_idx)//FPS
            frame_img = add_text(img_base.copy(), frases[i], i+1, sec_actual, TOTAL_SEG)
            writer.append_data(frame_img)
        prog_bar.progress((i+1)/3)

    writer.close()
    st.success(f"Video de {duracion_min} min creado!")

    try:
        ap="/tmp/audio.mp3"
        gTTS(text=(". ".join(frases)+" ")*duracion_min, lang='es', tld='com.mx').save(ap)
        st.audio(ap)
    except:
        pass

    with open(out_path,"rb") as f:
        vb=f.read()
    st.video(vb)
    st.download_button(f"⬇️ DESCARGAR {duracion_min} MIN", vb, f"drama_{duracion_min}min.mp4", "video/mp4", use_container_width=True)
    st.balloons()
