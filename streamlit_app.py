import streamlit as st, os, tempfile, textwrap
from PIL import Image, ImageDraw, ImageFont
import imageio
import numpy as np

st.set_page_config(page_title="VIDEO 55s CON ESCENA", layout="centered")
st.title("VIDEO 55s - Con escena visible")

idea = st.text_input("Tu historia:", "Luisa demanda a Hipolito por 100 millones")

if st.button("🚀 CREAR VIDEO 55s CON ESCENA", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    final_path = os.path.join(tmp, "video_con_escena.mp4")

    with st.spinner("Creando 3 escenas visibles..."):
        writer = imageio.get_writer(final_path, fps=24, codec='libx264', macro_block_size=1)

        # 3 escenas distintas, no negras
        escenas_data = [
            {"titulo": "ESCENA 1: LA DEMANDA", "color": (180, 30, 30), "texto": idea},
            {"titulo": "ESCENA 2: EL JUICIO", "color": (30, 30, 180), "texto": idea},
            {"titulo": "ESCENA 3: LA VICTORIA", "color": (30, 120, 30), "texto": idea},
        ]

        for idx, esc in enumerate(escenas_data):
            # Fondo de color fuerte, no negro
            img = Image.new('RGB', (1280,720), esc["color"])
            d = ImageDraw.Draw(img)

            # Cuadro blanco grande para contraste
            d.rectangle([30, 30, 1250, 690], fill=(255,255,255))
            d.rectangle([40, 40, 1240, 150], fill=esc["color"])

            # TITULO GRANDE ARRIBA - SIEMPRE SE VE
            try:
                font_titulo = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)
            except:
                font_titulo = ImageFont.load_default()
            
            # Dibujo el titulo en blanco sobre color
            d.text((60, 55), esc["titulo"], fill=(255,255,255), font=font_titulo)

            # Texto de la historia partido y GRANDE, negro sobre blanco
            texto_corto = esc["texto"][:120]  # solo 120 caracteres para que se lea
            lineas = textwrap.wrap(texto_corto, width=35)
            y = 200
            for linea in lineas:
                try:
                    font_texto = ImageFont.truetype("DejaVuSans.ttf", 42)
                except:
                    font_texto = ImageFont.load_default()
                d.text((60, y), linea, fill=(0,0,0), font=font_texto)
                y += 60

            # Numero de escena abajo
            d.text((60, 620), f"{idx+1}/3 - 18.5 segundos", fill=(100,100,100), font=font_titulo)

            frame = np.array(img)
            for _ in range(444): # 18.5s * 24fps
                writer.append_data(frame)

        writer.close()

    if os.path.exists(final_path):
        with open(final_path, "rb") as f:
            vb = f.read()
        st.success("¡VIDEO CON 3 ESCENAS VISIBLES CREADO!")
        st.video(vb)
        st.download_button(
            "⬇️ DESCARGAR MP4 CON ESCENAS PARA YOUTUBE",
            vb,
            "video_55s_con_escenas.mp4",
            "video/mp4",
            type="primary",
            use_container_width=True
        )
        st.balloons()
        st.info(f"Ahora sí: fondo de color, cuadro blanco y texto negro grande. Tamaño: {len(vb)/1024/1024:.2f} MB")

st.caption("FIX: Ya no es fondo negro. Ahora es color + cuadro blanco + texto negro gigante. Si se ve.")
