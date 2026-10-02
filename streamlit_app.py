import streamlit as st

st.set_page_config(page_title="Generador de Videos para YouTube", page_icon="🎬", layout="centered")

st.title("🎬 Creador de Dramas de 60s")
st.write("Genera videos estilo YouTube Shorts sobre GitHub y programación directamente desde tu móvil.")

# Selección rápida de guiones o ideas
idea_rapida = st.selectbox(
    "Elige una idea base para tu video:",
    (
        "Personalizado (Escribir mi propio prompt)",
        "El error en producción un viernes a las 5 PM",
        "La guerra de los Pull Requests (Code Review)",
        "El misterio del commit anónimo a las 3 AM"
    )
)

# Definir el prompt según la selección
prompt_por_defecto = ""
if "viernes" in idea_rapida:
    prompt_por_defecto = "A stressed software engineer staring at a computer screen with code and error messages, office setting, cinematic lighting, dramatic tension"
elif "Pull Requests" in idea_rapida:
    prompt_por_defecto = "A frustrated programmer looking at a laptop screen reviewing code with glowing annotations, office background, dramatic expression"
elif "commit" in idea_rapida:
    prompt_por_defecto = "A mysterious glowing computer monitor showing GitHub code commits in a dark room, cinematic tech thriller atmosphere"

# Campo de texto para el prompt (optimizado para pantalla táctil)
prompt_usuario = st.text_area(
    "Prompt para el video (en inglés para mejor resultado):", 
    value=prompt_por_defecto, 
    height=100
)

# Botón de generación
if st.button("🚀 Generar Video", type="primary", use_container_width=True):
    if not prompt_usuario.strip():
        st.warning("Por favor escribe o selecciona un prompt válido.")
    else:
        with st.spinner("Generando tu video para YouTube Shorts... Esto puede tomar un momento."):
            # Aquí se conecta con el motor de generación de video
            # (Nota: Asegúrate de tener configurado tu backend o entorno de llamadas a la herramienta de video)
            try:
                # Simulación de llamada exitosa / Integración de generación
                st.success("¡Tu video está listo!")
                st.balloons()
                
                # Espacio para mostrar el video generado
                # st.video("url_del_video_generado")
                
            except Exception as e:
                st.error(f"No se pudo generar el video. Intenta de nuevo. Error: {e}")

st.markdown("---")
st.markdown("💡 *Tip: Recuerda que los Shorts de YouTube funcionan mejor si duran 60 segundos y tienen un gancho fuerte al inicio.*")
