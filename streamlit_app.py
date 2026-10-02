import streamlit as st

st.set_page_config(page_title="Victor Karaoke - Dramas", page_icon="🎬")

st.title("🎬 Victor Karaoke | Dramas de 60s")
st.subheader("Guiones para YouTube Shorts y TikTok")

# Menú de selección para ver los guiones en el móvil
opcion = st.selectbox(
    "Elige un guion:",
    ("El Deploy del Pánico", "La venganza del Code Review", "El Commit Fantasma")
)

if opcion == "El Deploy del Pánico":
    st.markdown("""
    ### ⏱️ Duración: 60 segundos
    * **00:00 - 00:03 (GANCHO):** Primer plano de un programador sudando frente a una alerta roja en GitHub.
    * **00:03 - 00:20 (CONFLICTO):** Teclea rápido `git push origin main --force` por error.
    * **00:20 - 00:45 (EL CAOS):** El servidor principal de la empresa se cae.
    * **00:45 - 00:60 (DESENLACE):** Usa `git reflog`, salva el día y sale corriendo de la oficina.
    """)

elif opcion == "La venganza del Code Review":
    st.markdown("""
    ### ⏱️ Duración: 60 segundos
    * **00:00 - 00:03 (GANCHO):** Notificación de GitHub con 47 comentarios de revisión.
    * **00:03 - 00:45 (CONFLICTO):** Discusión mental sobre cambiar nombres de variables y refactorizar.
    * **00:45 - 00:60 (DESENLACE):** PR aprobado de mala gana y código funcionando de milagro.
    """)

else:
    st.markdown("""
    ### ⏱️ Duración: 60 segundos
    * **00:00 - 00:03 (GANCHO):** Commit anónimo a las 3:00 AM con mensaje "Arreglé el universo".
    * **00:03 - 00:45 (CONFLICTO):** El equipo investiga quién escribió ese código brillante.
    * **00:45 - 00:60 (DESENLACE):** Era el becario trabajando sonámbulo sobre el teclado.
    """)
