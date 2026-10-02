import streamlit as st
import requests, urllib.parse, random, io
from PIL import Image

st.title("DRAMA RD - VIDEO 90s")
drama = st.selectbox("Elige drama", ["Luisa vs Hipolito 100 millones", "Madre gana juicio", "Venganza en la corte"])

if st.button("CREAR VIDEO 90s"):
    for i in range(3):
        st.subheader(f"Escena {i+1} - 30s")
        prompt = f"dominican drama acting {drama} scene {i+1}, cinematic"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=720&height=1280&seed={random.randint(1,999999)}&nologo=true"
        r = requests.get(url, timeout=30)
        img = Image.open(io.BytesIO(r.content))
        st.image(img, use_container_width=True)
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(drama)}&tl=es&client=tw-ob")
    st.balloons()
