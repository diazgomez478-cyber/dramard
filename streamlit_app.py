import streamlit as st, os, tempfile, asyncio, textwrap, requests
import numpy as np
import cv2
import imageio
import edge_tts
import imageio_ffmpeg
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="PELICULA 55s REAL", layout="centered")
st.title("🎬 PELÍCULA 55s - Gente caminando y dialogando")

idea = st.text_input("Trama:", "Luisa demanda a Hipolito por 100 millones")

# Dialogo de película
dialogos = [
    {"personaje": "Luisa", "voz": "es-DO-RamonaNeural", "texto": f"¡Hipólito, te demando por 100 millones! Me traicionaste.", "color": (0,0,180)},
    {"personaje": "Hipolito", "voz": "es-DO-EmilioNeural", "texto": "¡Luisa, tú estás loca! Yo no te debo nada, eso es mentira.", "color": (180,0,0)},
    {"personaje": "Juez", "voz": "es-US-JorgeNeural", "texto": f"Caso {idea}. ¡Orden en la corte! Se hará justicia. Luisa gana.", "color": (0,100,0)},
]

def get_real_image(prompt):
    try:
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&nologo=true"
        r = requests.get(url, timeout=30)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except:
        return np.full((720,1280,3), (20,20,20), dtype=np.uint8)

async def crear_audio(texto, voz, out_path):
    comm = edge_tts.Communicate(texto, voz)
    await comm.save(out_path)

if st.button("🎬 CREAR PELÍCULA 55s CON ACTUACIONES", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    final_video = os.path.join(tmp, "pelicula.mp4")
    audio_files = []

    with st.spinner("Creando película con actores caminando y dialogando... 60 seg"):
        # 1. Crear audios dialogados (2 voces conversando)
        for i, d in enumerate(dialogos):
            ap = os.path.join(tmp, f"voz_{i}.mp3")
            asyncio.run(crear_audio(d["texto"], d["voz"], ap))
            audio_files.append(ap)

        # 2. Crear video con gente caminando (efecto Ken Burns = simula caminata)
        prompts = [
            f"dominican woman walking angry into courthouse, movie scene, realistic, cinematic, 4k - {idea}",
            f"dominican man walking arguing in court, drama movie, realistic people talking, cinematic",
            f"dominican woman walking victorious out of court, happy, movie ending, realistic"
        ]

        clips = []
        for i, prompt in enumerate(prompts):
            st.write(f"🎥 Filmando escena {i+1}/3: {dialogos[i]['personaje']} caminando y hablando...")
            base_img = get_real_image(prompt)
            base_img = cv2.resize(base_img, (1400, 800)) # más grande para hacer zoom y simular caminata

            clip_path = os.path.join(tmp, f"escena_{i}.mp4")
            writer = imageio.get_writer(clip_path, fps=24, codec='libx264', macro_block_size=1)

            # Efecto película: zoom lento + movimiento = gente caminando
            for f in range(432): # 18s
                zoom = 1.0 + (f/432)*0.15 # zoom in lento
                h, w = base_img.shape[:2]
                nh, nw = int(720*zoom), int(1280*zoom)
                resized = cv2.resize(base_img, (nw, nh))
                # movimiento lateral simula caminata
                x_offset = int((f/432)*120)
                y_offset = int((f/432)*80)
                crop = resized[y_offset:y_offset+720, x_offset:x_offset+1280]
                if crop.shape[0]!=720 or crop.shape[1]!=1280:
                    crop = cv2.resize(crop, (1280,720))

                # Barras de cine + nombre personaje
                cv2.rectangle(crop, (0,0), (1280, 80), (0,0,0), -1)
                cv2.rectangle(crop, (0,640), (1280, 720), (0,0,0), -1)
                cv2.putText(crop, f"{dialogos[i]['personaje'].upper()} - {idea[:30]}", (20,50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,200,0), 2, cv2.LINE_AA)

                # Subtítulo diálogo
                lineas = textwrap.wrap(dialogos[i]['texto'], width=50)
                yy = 660
                for lin in lineas[:1]: # solo 1 linea subtitulo estilo peli
                    cv2.putText(crop, lin, (20,yy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    yy+=30

                writer.append_data(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
            writer.close()
            clips.append(clip_path)

        # 3. Unir video + audios dialogados
        lista_txt = os.path.join(tmp, "lista.txt")
        with open(lista_txt, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        video_unido = os.path.join(tmp, "unido.mp4")
        audio_concat = os.path.join(tmp, "dialogo_completo.mp3")
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

        # unir audios dialogo
        with open(os.path.join(tmp, "audios.txt"), "w") as f:
            for a in audio_files:
                f.write(f"file '{a}'\n")
        os.system(f'"{ffmpeg}" -y -f concat -safe 0 -i "{os.path.join(tmp, "audios.txt")}" -c copy "{audio_concat}"')

        # unir videos
        os.system(f'"{ffmpeg}" -y -f concat -safe 0 -i "{lista_txt}" -c copy "{video_unido}"')
        # pegar dialogo a película
        os.system(f'"{ffmpeg}" -y -i "{video_unido}" -i "{audio_concat}" -c:v copy -c:a aac -shortest "{final_video}"')

    if os.path.exists(final_video):
        vb = open(final_video, "rb").read()
        st.success("¡PELÍCULA CON ACTUACIONES LISTA!")
        st.video(vb)
        st.download_button("⬇️ DESCARGAR PELÍCULA 55s CON GENTE HABLANDO PARA YOUTUBE", vb, "pelicula_55s_gente_hablando.mp4", "video/mp4", type="primary", use_container_width=True)
        st.balloons()
        st.info("🎬 Ahora sí: Gente caminando (efecto zoom), hablando, dialogando, conversaciones reales, estilo película con barras de cine y subtítulos. 2 voces: Ramona y Emilio discutiendo.")

st.caption("Esto es lo máximo gratis sin pagar Sora/Veo. Para actores 100% moviéndose real necesitas Runway o Luma, pero esto ya camina y dialoga para YouTube.")
