import streamlit as st, requests, urllib.parse, random, io, os, subprocess, tempfile
from PIL import Image

st.set_page_config(page_title="VIDEO MP4 REAL 55s", layout="centered")
st.title("VIDEO MP4 REAL - Ya no son fotos")

idea = st.selectbox("Elige drama:", (
    "Luisa demanda a Hipolito por 100 millones",
    "El error en produccion un viernes a las 5 PM",
    "La guerra de los Pull Requests"
))

def get_img(prompt):
    for _ in range(8):
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={random.randint(1,999999)}&nologo=true&model=turbo"
            r = requests.get(url, timeout=30)
            if len(r.content) > 10000:
                return Image.open(io.BytesIO(r.content)).convert("RGB")
        except: pass
    return None

if st.button("🚀 GENERAR VIDEO MP4 REAL 55s", type="primary", use_container_width=True):
    with st.spinner("Generando MP4 real con movimiento... 45 seg"):
        tmp = tempfile.mkdtemp()
        clips = []
        for i in range(3):
            prompt = f"{idea} Dominican cinematic acting scene {i+1} photorealistic modest clothing vertical 9:16 4k"
            img = get_img(prompt)
            if not img: 
                st.error("Pollinations lleno a las 9:15 PM, dale de nuevo en 20 seg"); st.stop()
            path = os.path.join(tmp, f"img{i}.jpg")
            img.save(path)
            # Convierte cada foto en clip MP4 de 18.5s con movimiento zoom
            clip_path = os.path.join(tmp, f"clip{i}.mp4")
            # efecto ken burns con ffmpeg
            cmd = f'ffmpeg -y -loop 1 -i "{path}" -vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,zoompan=z=\'min(zoom+0.0015,1.5)\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':fps=30" -t 18.5 -c:v libx264 -pix_fmt yuv420p -r 30 "{clip_path}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            clips.append(clip_path)
            st.image(img, caption=f"Escena {i+1} convertida a video", use_container_width=True)

        # Une los 3 clips en uno de 55.5s
        list_file = os.path.join(tmp, "list.txt")
        with open(list_file, "w") as f:
            for c in clips: f.write(f"file '{c}'\n")
        final = os.path.join(tmp, "final_55s.mp4")
        subprocess.run(f'ffmpeg -y -f concat -safe 0 -i "{list_file}" -c copy "{final}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(final, "rb") as f:
            video_bytes = f.read()

        st.success("¡VIDEO MP4 REAL 55s LISTO! Ya no son fotos")
        st.video(video_bytes)
        st.download_button("⬇️ DESCARGAR MP4 55s REAL", video_bytes, "video_55s_REAL.mp4", "video/mp4", use_container_width=True)
        st.balloons()

st.caption("Este ya es MP4 con movimiento, no GIF. Se reproduce en cualquier celular.")
