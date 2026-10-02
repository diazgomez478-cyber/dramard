import streamlit as st
from PIL import Image

st.set_page_config(page_title="DRAMA RD")
st.title("DRAMA RD - V27")
st.success("Si ves esto, ya no hay pantalla negra!")

st.write("Guion:")
guion = st.text_area("Guion", "Luisa demando a Hipolito por 100 millones. El juez fallo a favor de Luisa y los niños. Hipolito furioso gastara todo en lujos y fiestas.")

if st.button("CREAR"):
    st.write("Funciona!")
    st.balloons()
