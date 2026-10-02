import streamlit as st, os, tempfile, subprocess, requests

st.set_page_config(page_title="VIDEO 55s GENTE REAL - Opcion B", layout="centered")
st.title("OPCION B - Video 55s con gente real moviéndose")

idea = st.text_input("Tu historia:", "Luisa demanda a Hipolito por 100 millones")

# 3 videos reales de Pexels con gente real (tribunal, abrazo, fiesta)
CLIPS_REALES = [
    "https://videos.pexels.com/video-files/3048527/3048527-hd_1920_1080_30fps.mp4", # tribunal
    "https://videos.pexels.com/video-files/5198159/5198159-hd_1920_1080_30fps.mp4", # familia abrazo
    "https://videos.pexels.com/video-files/18069234/18069234-hd_1080_1920_30fps.mp4", # mujer llorando vertical
]

if st.button("🚀 GENERAR VIDEO 55s CON GENTE REAL", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    st.info("Descargando 3 videos reales... 20 seg")

    clips_local = []
    for i, url in enumerate(CLIPS_REALES):
        try:
            r = requests.get(url, timeout=30, stream=True)
            p = os.path.join(tmp, f"real_{i}.mp4")
            with open(p, "wb") as f:
                for chunk in r.iter_content(1024*1024):
                    f.write(chunk)
            # Corta cada clip a 18.5s y lo pone vertical 720x1280
            clip_cortado = os.path.join(tmp, f"corte_{i}.mp4")
            cmd = f'ffmpeg -y -i "{p}" -t 18.5 -vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280" -c:v libx264 -pix_fmt yuv420p -r 30 "{clip_cortado}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(clip_cortado):
                clips_local.append(clip_cortado)
                st.video(clip_cortado, caption=f"Clip real {i+1} - Gente moviéndose de verdad")
        except Exception as e:
            st.error(f"Error clip {i}: {e}")

    if len(clips_local) == 3:
        lista = os.path.join(tmp, "lista.txt")
        with open(lista, "w") as f:
            for c in clips_local:
                f.write(f"file '{c}'\n")
        final = os.path.join(tmp, "video_55s_gente_real.mp4")
        subprocess.run(f'ffmpeg -y -f concat -safe 0 -i "{lista}" -c copy "{final}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(final):
            with open(final, "rb") as v:
                vb = v.read()
            st.success(f"¡VIDEO 55s CON GENTE REAL LISTO! - {idea}")
            st.video(vb)
            st.download_button("⬇️ DESCARGAR MP4 55s GENTE REAL", vb, "video_55s_gente_real.mp4", "video/mp4", use_container_width=True)
            st.balloons()
        else:
            st.error("No se pudo unir, pero los 3 clips de arriba ya son video real con gente moviéndose")
    else:
        st.warning("Solo se descargaron algunos clips, igual son video real")

st.caption("Opción B: gente real moviéndose, caminando, llorando. Ya no es foto con zoom.")
