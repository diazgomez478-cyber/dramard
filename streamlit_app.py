import streamlit as st, os, tempfile
from PIL import Image, ImageDraw
import cv2
import numpy as np

st.set_page_config(page_title="VIDEO 55s YOUTUBE SIN FFMPEG", layout="centered")
st.title("VIDEO 55s LISTO PARA YOUTUBE - Sin FFmpeg")

idea = st.text_input("Tu historia:", "Luisa demanda a Hipolito por 100 millones")

if st.button("🚀 CREAR VIDEO 55s DESCARGABLE PARA YOUTUBE", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    final_path = os.path.join(tmp, "video_55s_youtube.mp4")

    with st.spinner("Creando MP4 de 55s sin ffmpeg... 30 seg"):
        # Creador de MP4 interno (no necesita ffmpeg del sistema)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(final_path, fourcc, 30.0, (1280, 720))

        escenas = [
            (f"{idea}\n\nESCENA 1/3\nLa Demanda", (30,40,90)),
            (f"{idea}\n\nESCENA 2/3\nEl Juicio", (90,30,40)),
            (f"{idea}\n\nESCENA 3/3\nLa Victoria", (30,90,40)),
        ]

        for texto, color in escenas:
            img = Image.new('RGB', (1280,720), color)
            d = ImageDraw.Draw(img)
            d.rectangle([50, 150, 1230, 550], fill=(0,0,0))
            d.text((80, 180), texto, fill=(255,255,255), spacing=15)
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            # 18.5s x 30fps = 555 frames por escena = 55.5s total
            for _ in range(555):
                out.write(frame)

        out.release()

    if os.path.exists(final_path):
        with open(final_path, "rb") as f:
            vb = f.read()
        st.success("¡VIDEO MP4 55s CREADO! Ya puedes subirlo a YouTube")
        st.video(vb)
        st.download_button(
            "⬇️ DESCARGAR MP4 PARA YOUTUBE (55s)",
            vb,
            "video_55s_youtube.mp4",
            "video/mp4",
            type="primary",
            use_container_width=True
        )
        st.balloons()
    else:
        st.error("No se creó el video")

st.caption("Este no usa ffmpeg, por eso no te da 'FFmpeg falló'. Es MP4 real para YouTube.")
