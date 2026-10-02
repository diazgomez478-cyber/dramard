import streamlit as st, requests, io, random, urllib.parse, os, time, subprocess
from PIL import Image, ImageDraw
import numpy as np, textwrap
import imageio.v2 as imageio
from gtts import gTTS

st.set_page_config(page_title="DRAMA RD FINAL", page_icon="🎬")
st.title("🎬 DRAMA RD - FINAL CON AUDIO PEGADO")
st.caption("Un solo MP4 con voz incluida - listo para TikTok")

guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso decidio gastar todo en lujos y fiestas.")

def get_img(p):
    for _ in range(3):
        try:
            seed=random.randint(1,9999999)
            url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=512&height=512&seed={seed}&nologo=true&model=flux"
            r=requests.get(url,timeout=90,headers={"User-Agent":"Mozilla/5.0"})
            if len(r.content)>8000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720))
        except: time.sleep(1)
    return Image.new('RGB',(1280,720),(35,25,15))

def subtitle(img, txt):
    d=ImageDraw.Draw(img)
    W,H=img.size
    d.rectangle([0,H-160,W,H],fill=(0,0,0))
    for i,line in enumerate(textwrap.wrap(txt.upper(),45)[:2]):
        d.text((W//2,H-125+i*38),line,fill="white",anchor="mm",stroke_width=3,stroke_fill="black")
    return img

def zoom(img,n=40):
    frames=[]
    for i in range(n):
        z=1+(i/n)*0.25
        nw,nh=int(1280*z),int(720*z)
        rz=img.resize((nw,nh),Image.LANCZOS)
        frames.append(np.array(rz.crop((int((nw-1280)/2),0,int((nw-1280)/2)+1280,720))))
    return frames

if st.button("🔥 CREAR VIDEO FINAL CON AUDIO",use_container_width=True):
    frases=[f.strip() for f in guion.split(".") if f.strip()][:4]
    prompts=["judge courtroom angry","dominican woman crying with children","rich dominican man angry suit","man luxury party money champagne"]

    all_frames=[]
    for i,fr in enumerate(frases):
        st.write(f"Escena {i+1}...")
        img=get_img(prompts[i%4]+", cinematic photorealistic 8k dramatic lighting")
        img=subtitle(img,fr)
        st.image(img,use_container_width=True)
        all_frames.extend(zoom(img,45))

    # 1. Video sin audio
    temp_video="/tmp/temp.mp4"
    imageio.mimsave(temp_video,all_frames,fps=12,macro_block_size=1)

    # 2. Audio
    audio_path="/tmp/audio.mp3"
    gTTS(text=". ".join(frases)[:600],lang='es',tld='com.mx').save(audio_path)

    # 3. PEGAR AUDIO + VIDEO (un solo MP4)
    final_video="/tmp/drama_final_con_audio.mp4"
    try:
        # Usa ffmpeg que viene con imageio-ffmpeg
        cmd=f'ffmpeg -y -i {temp_video} -i {audio_path} -c:v copy -c:a aac -shortest {final_video}'
        subprocess.run(cmd,shell=True,capture_output=True)
    except:
        final_video=temp_video

    st.success("✅ VIDEO CON AUDIO PEGADO LISTO")
    st.video(final_video)

    with open(final_video,"rb") as f:
        st.download_button("⬇️ DESCARGAR VIDEO FINAL (CON AUDIO)",f,"drama_rd_final.mp4","video/mp4",use_container_width=True)
    
    st.balloons()
