import streamlit as st

st.set_page_config(page_title="DRAMA RD - Tienda Oficial", page_icon="🔥", layout="wide")

st.markdown("""
<style>
.main {background-color: #0e1117;}
h1 {color: #ff4b4b; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("🔥 DRAMA RD - Tienda Oficial 🔥")
st.markdown("### Bienvenido a la tienda #1 de Dramas en RD")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://images.unsplash.com/photo-1540221652346-e5dd6b50f3e7?w=500", caption="Drama Clásico")
    st.subheader("Pack Dramas 2024")
    st.write("💰 Precio: RD$ 500")
    if st.button("Comprar Pack 1", key="1"):
        st.success("¡Agregado al carrito! Escríbenos al WhatsApp")

with col2:
    st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=500", caption="Drama Premium")
    st.subheader("Pack Dramas Premium")
    st.write("💰 Precio: RD$ 800")
    if st.button("Comprar Pack 2", key="2"):
        st.success("¡Agregado al carrito! Escríbenos al WhatsApp")

with col3:
    st.image("https://images.unsplash.com/photo-1445205170230-053b83016050?w=500", caption="Drama VIP")
    st.subheader("Pack Dramas VIP")
    st.write("💰 Precio: RD$ 1200")
    if st.button("Comprar Pack 3", key="3"):
        st.success("¡Agregado al carrito! Escríbenos al WhatsApp")

st.divider()
st.markdown("### 📲 Contacto y Pedidos")
st.write("**WhatsApp:** +1 (829) XXX-XXXX")
st.write("**Instagram:** @dramard_oficial")
st.write("**Envíos a todo RD 🇩🇴**")

st.link_button("💬 Pedir por WhatsApp", "https://wa.me/1829XXXXXXX")
