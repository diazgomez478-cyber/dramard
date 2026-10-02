import streamlit as st, os, tempfile
from PIL import Image, ImageDraw
import imageio
import numpy as np

st.set_page_config(page_title="VIDEO 55s YOUTUBE FIX", layout="centered")
st.title("VIDEO 55s FIX - Ya reproduce")

idea = st.text_input("Tu historia:", "Luisa demanda a Hipolito por 100 millones")

if st.button("🚀 CREAR VIDEO 55s DESCARGABLE PARA YOUTUBE", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    final_path = os.path.join(tmp, "video_55s_youtube.mp4")

    with st.spinner("Creando MP4 H264 compatible con YouTube..."):
        # Writer H264 que sí reproduce en celulares y YouTube
        writer = imageio.get_writer(final_path, fps=30, codec='libx264', macro_block_size=1, quality=8)

        escenas = [
            f"{idea}\n\nESCENA 1/3\nLa Demanda - 0 a 18s",
            f"{idea}\n\nESCENA 2/3\nEl Juicio - 18 a 37s",
            f"{idea}\n\nESCENA 3/3\nLa Victoria - 37 a 55s"
        ]
        colores = [(30,40,90), (90,30,40), (30,90,40)]

        for i, texto in enumerate(escenas):
            img = Image.new('RGB', (1280,720), colores[i])
            d = ImageDraw.Draw(img)
            d.rectangle([50, 150, 1230, 550], fill=(0,0,0))
            d.text((80, 180), texto, fill=(255,255,255), spacing=15)
            frame = np.array(img)
            for _ in range(555): # 18.5s * 30fps
                writer.append_data(frame)

        writer.close()

    if os.path.exists(final_path):
        with open(final_path, "rb") as f:
            vb = f.read()
        st.success("¡VIDEO MP4 H264 CREADO! Este sí reproduce")
        st.video(vb)
        st.download_button(
            "⬇️ DESCARGAR MP4 PARA YOUTUBE (55s) - Ahora sí reproduce",
            vb,
            "video_55s_youtube_H264.mp4",
            "video/mp4",
            type="primary",
            use_container_width=True
        )
        st.balloons()
        st.write(f"Tamaño: {len(vb)/1024/1024:.1f} MB - Listo para YouTube Studio")
    else:
        st.error("Error")

st.caption("FIX: Cambié de mp4v a libx264 H264, ahora el reproductor ya no sale en 0:00")
