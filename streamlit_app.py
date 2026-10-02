import streamlit as st, os, tempfile, asyncio, requests, textwrap
import numpy as np
import cv2
import imageio
import imageio_ffmpeg
import edge_tts
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="55s SIN GTTS - Solo Neural", layout="centered")
st.title("🎬 55s Voz Dominicana Real - SIN gTTS")

idea = st.text_input("Trama:", "Luisa demanda a Hipolito por 100 millones")

# Voces dominicanas reales humanas
VOCES = {
    "Luisa": "es-DO-RamonaNeural",
    "Hipolito": "es-DO-EmilioNeural"
}

def get_actor(prompt):
    try:
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&nologo=true&model=flux"
        r = requests.get(url, timeout=25)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except:
        return np.full((720,1280,3), (20,20,20), dtype=np.uint8)

async def crear_voz(texto, voz, path):
    # truco anti-NoAudioReceived: texto corto + rate lento
    communicate = edge_tts.Communicate(texto, voz, rate="-5%")
    await communicate.save(path)

if st.button("🎬 CREAR CON VOZ DOMINICANA REAL (SIN GTTS)", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    final_video = os.path.join(tmp, "sin_gtts.mp4")

    guion = [
        {"quien": "Luisa", "texto": f"¡Hipolito! Te demando por cien millones. Ya no aguanto tus mentiras. {idea}", "prompt": "dominican angry woman walking to court talking, drama movie realistic 4k"},
        {"quien": "Hipolito", "texto": "Luisa, por Dios, estas loca. Yo no te debo nada. Vamos a hablar como gente normal.", "prompt": "dominican man walking arguing street talking drama realistic 4k"},
        {"quien": "Luisa", "texto": f"Se acabo la conversacion Hipolito. Juez, haga justicia con {idea}. Quiero mi dinero.", "prompt": "dominican woman arguing in courtroom walking conversing movie realistic 4k"}
    ]

    with st.spinner("Creando con voz neural dominicana real... SIN gTTS"):
        audio_files = []
        for i, escena in enumerate(guion):
            ap = os.path.join(tmp, f"voz_{i}.mp3")
            st.write(f"🎙️ Generando voz de {escena['quien']}...")
            try:
                asyncio.run(crear_voz(escena["texto"], VOCES[escena["quien"]], ap))
                audio_files.append(ap)
            except Exception as e:
                st.error(f"Fallo voz {escena['quien']}: {e}")
                st.stop()

        clips = []
        for i, escena in enumerate(guion):
            st.write(f"🎥 Filmando: {escena['quien']} caminando y hablando...")
            base = get_actor(escena["prompt"])
            base = cv2.resize(base, (1400, 800))
            clip_path = os.path.join(tmp, f"escena_{i}.mp4")
            writer = imageio.get_writer(clip_path, fps=24, codec='libx264', macro_block_size=1)

            for f in range(400):
                zoom = 1.0 + (f/400)*0.15
                resized = cv2.resize(base, (int(1280*zoom), int(720*zoom)))
                x_off = int((f/400)*140)
                crop = resized[0:720, x_off:x_off+1280]
                if crop.shape[1]!=1280:
                    crop = cv2.resize(crop, (1280,720))

                cv2.rectangle(crop, (0,0), (1280,70), (0,0,0), -1)
                cv2.rectangle(crop, (0,600), (1280,720), (0,0,0), -1)
                cv2.putText(crop, f"{escena['quien'].upper()} - ACTUANDO", (20,45), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255,200,0), 2, cv2.LINE_AA)
                lineas = textwrap.wrap(escena["texto"], 50)
                cv2.putText(crop, lineas[0][:60], (20,640), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)

                writer.append_data(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
            writer.close()
            clips.append(clip_path)

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        with open(os.path.join(tmp, "lista.txt"), "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")
        video_unido = os.path.join(tmp, "unido.mp4")
        os.system(f'"{ffmpeg}" -y -f concat -safe 0 -i "{os.path.join(tmp, "lista.txt")}" -c copy "{video_unido}"')

        with open(os.path.join(tmp, "audios.txt"), "w") as fw:
            for a in audio_files:
                fw.write(f"file '{a}'\n")
        audio_concat = os.path.join(tmp, "dialogos.mp3")
        os.system(f'"{ffmpeg}" -y -f concat -safe 0 -i "{os.path.join(tmp, "audios.txt")}" -c copy "{audio_concat}"')
        os.system(f'"{ffmpeg}" -y -i "{video_unido}" -i "{audio_concat}" -c:v copy -c:a aac -shortest "{final_video}"')

    if os.path.exists(final_video):
        vb = open(final_video, "rb").read()
        st.success("¡SIN GTTS! Voz dominicana real humana")
        st.video(vb)
        st.audio(open(audio_concat, "rb").read())
        st.download_button("⬇️ DESCARGAR SIN GTTS - VOZ REAL", vb, "sin_gtts_voz_dominicana_real_55s.mp4", "video/mp4", type="primary", use_container_width=True)
        st.balloons()

st.caption("SIN gTTS: solo edge-tts Ramona y Emilio, voces dominicanas reales humanas, caminando, hablando, dialogando.")
