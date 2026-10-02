import streamlit as st, os, tempfile, asyncio, requests, textwrap
import numpy as np
import cv2
import imageio
import imageio_ffmpeg
import edge_tts
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="LA ERA DE TRUMP - 55s", layout="centered")
st.title("🎬 LA ERA DE TRUMP - Película 55s")

# TU TEXTO COMPLETO COMO GUIÓN
TEXTO_TRUMP = """La Era de Trump. Trump un líder político que al comienzo pensaban que no llegaba ni a la primera vuelta ha dejado al mundo patas arriba.
Control, migración, aranceles, Israel, Irán, estrecho de Ormuz.
En los primeros 2 años que esta por culminar, por el congreso y el senado, Trump se ha llenado de orgullo y en sí mismo creerse el más superior del mundo.
Trump perderá la cámara de representante y la cámara del senado donde tendrá que luchar para poder mantenerse en el puesto como presidente.
Trump sería capaz de tirar una ley para que las elecciones sean canceladas si se ve acorralado.
Los 2 últimos años de Trump serán 2 años de dolor y sufrimiento no solo para Estados Unidos sino para el mundo entero. Un desafío de autoridad y de quien tiene el control.
Trump es la chispa de encender el fuego. Ha tenido la oportunidad de ser un buen líder pero su orgullo y ego lo ha cegado.
Israel un país que ha dado por la paz y luchas pero los oponentes prefieren guerra y muerte de millones de inocentes.
Los malos hacen creer que Israel es violento. Al contrario Israel es amigo del mundo.
Trump un amigo de Israel, un buen aliado, pero Israel no te confíes en Trump."""

idea = st.text_area("Guión La Era de Trump:", TEXTO_TRUMP, height=200)

VOCES = {"Narrador": "es-DO-RamonaNeural", "Analista": "es-DO-EmilioNeural"}

def get_img(prompt):
    try:
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&nologo=true&model=flux"
        r = requests.get(url, timeout=25)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except:
        return np.full((720,1280,3), (20,20,20), dtype=np.uint8)

async def crear_voz(texto, voz, path):
    comm = edge_tts.Communicate(texto, voz, rate="-8%", volume="+10%")
    await comm.save(path)

if st.button("🎬 CREAR PELÍCULA LA ERA DE TRUMP 55s", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    final_video = os.path.join(tmp, "era_trump.mp4")

    guion = [
        {"quien": "Narrador", "texto": "La Era de Trump. Un líder que pensaban no llegaba ni a la primera vuelta, ha dejado al mundo patas arriba. Control, migración, aranceles, Israel, Irán y el estrecho de Ormuz.", "prompt": "Donald Trump walking white house dramatic, political movie, realistic, 4k cinematic"},
        {"quien": "Analista", "texto": "En sus primeros dos años, por el congreso y el senado, Trump se ha llenado de orgullo, creyéndose el más superior del mundo. Perderá la cámara y tendrá que luchar para mantenerse.", "prompt": "US congress senate drama, politicians arguing walking, realistic movie 4k"},
        {"quien": "Narrador", "texto": "Sería capaz de tirar una ley para cancelar elecciones si se ve acorralado. Los últimos dos años serán dolor y sufrimiento para Estados Unidos y el mundo. Es la chispa que enciende el fuego.", "prompt": "world on fire protest drama, Trump authority challenge, cinematic realistic 4k"},
        {"quien": "Analista", "texto": f"Israel es un país que ha dado por la paz, pero lo hacen ver violento. Al contrario, es amigo del mundo. {idea[:100]}. Trump es aliado de Israel, pero Israel no te confíes en Trump.", "prompt": "Israel US alliance drama, Jerusalem flag, political tension realistic movie 4k"}
    ]

    with st.spinner("Filmando La Era de Trump... SIN gTTS, voz real..."):
        audios = []
        for i, esc in enumerate(guion):
            ap = os.path.join(tmp, f"voz_{i}.mp3")
            st.write(f"🎙️ {esc['quien']} narrando...")
            asyncio.run(crear_voz(esc["texto"], VOCES[esc["quien"]], ap))
            audios.append(ap)

        clips = []
        for i, esc in enumerate(guion):
            st.write(f"🎥 Escena {i+1}/4: {esc['quien']}...")
            base = get_img(esc["prompt"])
            base = cv2.resize(base, (1400, 800))
            cp = os.path.join(tmp, f"esc_{i}.mp4")
            writer = imageio.get_writer(cp, fps=24, codec='libx264', macro_block_size=1)

            for f in range(350): # 14.5s x 4 = 58s
                zoom = 1.0 + (f/350)*0.15
                rz = cv2.resize(base, (int(1280*zoom), int(720*zoom)))
                x = int((f/350)*120)
                crop = rz[0:720, x:x+1280]
                if crop.shape[1]!=1280:
                    crop = cv2.resize(crop, (1280,720))

                cv2.rectangle(crop, (0,0), (1280,75), (0,0,0), -1)
                cv2.rectangle(crop, (0,620), (1280,720), (0,0,0), -1)
                cv2.putText(crop, f"LA ERA DE TRUMP - {esc['quien'].upper()}", (20,50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255,50,50), 2, cv2.LINE_AA)
                lineas = textwrap.wrap(esc["texto"], 55)
                cv2.putText(crop, lineas[0][:62], (20,650), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2, cv2.LINE_AA)
                if len(lineas)>1:
                    cv2.putText(crop, lineas[1][:62], (20,680), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2, cv2.LINE_AA)

                writer.append_data(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
            writer.close()
            clips.append(cp)

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        with open(os.path.join(tmp, "lista.txt"), "w") as f:
            for c in clips: f.write(f"file '{c}'\n")
        unido = os.path.join(tmp, "unido.mp4")
        os.system(f'"{ffmpeg}" -y -f concat -safe 0 -i "{os.path.join(tmp, "lista.txt")}" -c copy "{unido}"')

        with open(os.path.join(tmp, "audios.txt"), "w") as fw:
            for a in audios: fw.write(f"file '{a}'\n")
        audio_concat = os.path.join(tmp, "voz_final.mp3")
        os.system(f'"{ffmpeg}" -y -f concat -safe 0 -i "{os.path.join(tmp, "audios.txt")}" -c copy "{audio_concat}"')
        os.system(f'"{ffmpeg}" -y -i "{unido}" -i "{audio_concat}" -c:v copy -c:a aac -shortest "{final_video}"')

    if os.path.exists(final_video):
        vb = open(final_video, "rb").read()
        st.success("¡LA ERA DE TRUMP LISTA - 55s!")
        st.video(vb)
        st.audio(open(audio_concat, "rb").read())
        st.download_button("⬇️ DESCARGAR LA ERA DE TRUMP PARA YOUTUBE", vb, "la_era_de_trump_55s.mp4", "video/mp4", type="primary", use_container_width=True)
        st.balloons()

st.caption("Código convertido: Tu texto de Trump en película 55s, con voces dominicanas reales, caminando, hablando, SIN gTTS.")
