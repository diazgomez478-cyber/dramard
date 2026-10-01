import streamlit as st
st.title("🎬 DRAMA RD - Creador de Videos")
tema = st.text_input("Tema del drama","infidelidad")
prota = st.text_input("Protagonista","La Chapi")
if st.button("🔥 CREAR DRAMA"):
    st.balloons()
    st.write(f"TITULO: {tema}")
    st.write(f"Guion: {prota} me hizo un drama por {tema}. Comenten que hago? #dramard #viral")
