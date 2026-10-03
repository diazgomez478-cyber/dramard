import streamlit as st
import time, jwt, requests

st.title("Genera dramas de 55s estilo película")

AK = st.text_input("Introduce tu Access Key (AK):", type="password")
SK = st.text_input("Introduce tu Secret Key (SK):", type="password")

formato = st.selectbox("Selecciona el formato:", ["Short de YouTube / Reel (Vertical 9:16)", "YouTube Horizontal 16:9"])
prompt = st.text_area("Prompt:", "contrast studio lighting, world maps background with glowing red and blue lines, ultra realistic 4k, 24fps atmosphere.")

if st.button("🚀 Iniciar Generación de Video Real"):
    if not AK or not SK:
        st.error("Pega las 2 claves, no 1 sola")
    else:
        # Genera el token de 3 partes que pide Kling
        payload = {"iss": AK, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5}
        token = jwt.encode(payload, SK, algorithm="HS256")
        
        st.info("Enviando escena al servidor de Kling AI...")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        # URL CORRECTA DE SINGAPUR
        url = "https://api-singapore.klingai.com/v1/videos/text2video"
        
        st.write(f"Token generado (primeras letras): {token[:20]}...")
        # Aquí va tu request real
