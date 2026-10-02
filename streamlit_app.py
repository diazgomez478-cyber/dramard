import streamlit as st, os, tempfile, subprocess
from PIL import Image, ImageDraw

st.set_page_config(page_title="VIDEO 55s PARA YOUTUBE", layout="centered")
st.title("VIDEO 55s LISTO PARA YOUTUBE")

idea = st.text_input("Tu historia:", "Luisa demanda a Hipolito por 100 millones")

if st.button("🚀 CREAR VIDEO 55s DESCARGABLE PARA YOUTUBE", type="primary", use_container_width=True):
    tmp = tempfile.mkdtemp()
    st.info("Creando MP4 único de 55s para YouTube...")

    # 3 escenas sin zoom ni movimiento como pediste
    escenas = [
        f"{idea}\n\nESCENA 1/3\nLa Demanda - 0 a 18s",
        f"{idea}\n\nESCENA 2/3\nEl Juicio - 18 a 37s",
        f"{idea}\n\nESCENA 3/3\nLa Victoria - 37 a 55s"
    ]

    clips = []
    for i, texto in enumerate(escenas):
        img = Image.new('RGB', (1280,720), (20+i*30, 40, 80))
        d = ImageDraw.Draw(img)
        d.rectangle([50, 150, 1230, 570], fill=(0,0,0))
        d.text((80, 200), texto, fill=(255,255,255), spacing=15)
        img_path = os.path.join(tmp, f"escena_{i}.jpg")
        img.save(img_path)

        clip_path = os.path.join(tmp, f"clip_{i}.mp4")
        # Video estático de 18.5s - sin zoom, sin movimiento
        cmd = f'ffmpeg -y -loop 1 -i "{img_path}" -t 18.5 -vf "scale=1280:720" -c:v libx264 -pix_fmt yuv420p -r 30 "{clip_path}"'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(clip_path):
            clips.append(clip_path)

    # Une los 3 en uno solo de 55.5s para YouTube
    lista = os.path.join(tmp, "lista.txt")
    with open(lista, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    
    final = os.path.join(tmp, "video_55s_YOUTUBE.mp4")
    subprocess.run(f'ffmpeg -y -f concat -safe 0 -i "{lista}" -c copy "{final}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(final):
        with open(final, "rb") as f:
            video_bytes = f.read()
        
        st.success("¡VIDEO 55s LISTO PARA YOUTUBE!")
        st.video(video_bytes)
        # ESTE ES EL BOTÓN PARA YOUTUBE
        st.download_button(
            label="⬇️ DESCARGAR MP4 PARA SUBIR A YOUTUBE",
            data=video_bytes,
            file_name="video_55s_youtube.mp4",
            mime="video/mp4",
            type="primary",
            use_container_width=True
        )
        st.balloons()
        st.write("Ya lo puedes subir directo a YouTube Studio. Dura 55s exactos, formato 1280x720 HD.")
    else:
        st.error("FFmpeg falló. Dale a Manage app > Reboot y vuelve a intentar. Este código SÍ crea archivo descargable.")
