import streamlit as st

# Configuración estética para simular un entorno de producción cinematográfica
st.set_page_config(page_title="Cinematic Video Presenter", page_icon="🎬", layout="centered")

st.title("🎬 Presentación Cinemática: La Era de Trump")
st.subheader("Configuración de Video Presentación Estilo Película (55 Segundos)")

st.info("Formato sugerido: Vertical 9:16 (Shorts/Reels) o Cine Documental. Ajustes listos para Teleprompter Móvil.")

# --- SECCIÓN 1: INTRO / EL ENIGMA (0:00 - 0:15) ---
with st.expander("🎥 SECUENCIA 1: El Enigma del Poder (0:00 - 0:15)", expanded=True):
    st.markdown("### **Aspecto Visual (Prompt de Video)**")
    st.code("A dark, atmospheric cinematic shot of the Oval Office, dramatic high-contrast lighting, shadows engulfing the room, slow camera zoom towards an empty leather chair, 4k, movie trailer style.", language="text")
    
    st.markdown("### **Audio y Locución (Voz de Tráiler)**")
    st.warning("🎙️ *[Voz grave y pausada]*: Imagínate esto: un presidente acorralado políticamente, tensiones globales al límite y una crisis internacional en marcha. De repente, el líder de la potencia más grande del mundo decide firmar un decreto para cancelar las próximas elecciones presidenciales y quedarse en el poder. **¿Es esto legalmente posible?**")
    
    st.markdown("### **Efectos de Sonido (SFX)**")
    st.text("🎵 [Fondo]: Sonido sutil de bajas frecuencias (Bass Drop) y un reloj de fondo haciendo eco.")

# --- SECCIÓN 2: EL DESARROLLO / LA CHISPA (0:15 - 0:35) ---
with st.expander("⚡ SECUENCIA 2: La Chispa y los Contrapesos (0:15 - 0:35)", expanded=False):
    st.markdown("### **Aspecto Visual (Prompt de Video)**")
    st.code("Fast cinematic cuts of the US Capitol, glowing digital data streams, overlays of the American Constitution text fading in and out, intense political thriller aesthetic.", language="text")
    
    st.markdown("### **Audio y Locución**")
    st.warning("🎙️ *[Aumenta el ritmo]*: Muchos piensan que en momentos de extrema tensión, un presidente puede usar un 'estado de emergencia' para suspender la democracia. Pero la ley es implacable. El presidente NO tiene la facultad de mover las fechas; ese control le pertenece estrictamente al Congreso desde hace casi dos siglos.")
    
    st.markdown("### **Efectos de Sonido (SFX)**")
    st.text("🎵 [Fondo]: Transición rápida con sonido de 'Swoosh' metálico. La música sube con percusiones de acción.")

# --- SECCIÓN 3: EL CLÍMAX / MEDIO ORIENTE (0:35 - 0:55) ---
with st.expander("🔥 SECUENCIA 3: El Desafío Global (0:35 - 0:55)", expanded=False):
    st.markdown("### **Aspecto Visual (Prompt de Video)**")
    st.code("Cinematic low-angle shot of oil tankers navigating the Strait of Hormuz at sunset, military radar graphics overlaid on screen, highly realistic, war movie tension.", language="text")
    
    st.markdown("### **Audio y Locución**")
    st.warning("🎙️ *[Clímax dramático]*: Control, migración, aranceles... y el tablero más caliente del mundo: el Estrecho de Ormuz. Israel y Rusia observan a un líder impulsado por el orgullo. Los próximos dos años serán un desafío de autoridad pura. ¿Quién tiene realmente el control del fuego?")
    
    st.markdown("### **Efectos de Sonido (SFX)**")
    st.text("🎵 [Fondo]: Gran crescendo musical con violines intensos que cortan en seco al final.")

# --- PANEL DE ACCIÓN Y DESCARGA DE RECURSOS ---
st.markdown("---")
st.write("### 🎛️ Panel de Control de Producción")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎬 Previsualizar Escena Completa", use_container_width=True):
        st.success("Sincronizando prompts cinematográficos con la línea de tiempo de 55 segundos...")
with col2:
    # Simulación de exportación de metadatos o guion para herramientas de video IA
    data_guion = "Guion de película: La Era de Trump (55s)"
    st.download_button(
        label="📥 Descargar Guion para Editor",
        data=data_guion,
        file_name="trailer_trump_55s.txt",
        mime="text/plain",
        use_container_width=True
    )
