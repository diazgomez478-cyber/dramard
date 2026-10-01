
import streamlit as st
import urllib.parse, time

st.set_page_config(page_title="DRMA AI Video", page_icon="🎬")
st.title("🎬 DRAMA RD - AI Video Studio")
st.caption("🇩🇴 Igual que PixVerse pero Dominicano - 1, 3 y 5 Min")

tema = st.text_input("Tema", "infidelidad")
prota = st.text_input("Protagonista", "La Chapi")
duracion = st.selectbox("Duración", ["1 MINUTO", "3 MINUTOS", "5 MINUTOS"])

if st.button("🔥 CREAR DRAMA + VIDEO"):
    num = 3 if "1" in duracion else 5 if "3" in duracion else 7
    st.success(f"Generando {duracion} con {num} escenas")
    for i in range(1, num+1):
        prompt = f"dominican drama {tema} {prota} scene {i} cinematic 4k"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={i}{int(time.time())}"
        st.image(url, caption=f"Escena {i}: {prota}")
    st.balloons()
