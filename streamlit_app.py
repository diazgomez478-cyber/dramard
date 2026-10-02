import streamlit as st
import requests, urllib.parse, io, random
from PIL import Image
from gtts import gTTS

st.set_page_config(page_title="Creador de Dramas 60s", page_icon="🎬", layout="centered")
st.title("🎬 Creador de Dramas de 60s")
st.write("Genera videos estilo Shorts/Reels sobre programación y dramas de la vida real directamente desde tu móvil.")

idea_rapida = st.selectbox("Elige una idea base para tu video:", (
    "Personalizado (Escribir mi propio prompt)",
    "El error en producción un viernes a las 5 PM",
    "La guerra de los Pull Requests (Code Review)",
    "El misterio del commit anónimo a las 3 AM",
    "Luisa demanda a Hipolito por 100 millones"
))

prompt_por_defecto = ""
audio_texto = ""

if "viernes" in idea_rapida:
    prompt_por_defecto = "A stressed software engineer staring at a computer screen with code and error messages, office setting, cinematic lighting, 9:16 vertical aspect ratio"
    audio_texto = "El error en produccion un viernes a las cinco de la tarde. El ingeniero esta estresado y el servidor no responde. Todos se fueron a casa y el solo se quedo arreglando un bug que rompio todo el sistema. Son las ocho de la noche, tiene hambre, frio y el jefe llamando cada cinco minutos preguntando si ya esta listo."
elif "Pull Requests" in idea_rapida:
    prompt_por_defecto = "A frustrated programmer looking at a laptop reviewing code with glowing annotations, dramatic expression, vertical 9:16"
    audio_texto = "La guerra de los Pull Requests. El code review se vuelve intensamente dramatico. Llevas tres horas esperando aprobacion y tu compañero te deja veinte comentarios. Que cambies el nombre, que quites un espacio, que todo esta mal. Al final es solo una coma la que detiene el despliegue a produccion."
elif "commit" in idea_rapida:
    prompt_por_defecto = "A mysterious glowing computer monitor showing GitHub commits in a dark room, cinematic tech thriller, 9:16 vertical"
    audio_texto = "El misterio del commit anonimo a las tres de la mañana. Nadie sabe quien rompio la rama principal. El historial no muestra nombre, solo dice arreglo rapido. Y ahora toda la base de datos esta caida. Todos en la oficina se miran con sospecha, nadie quiere confesar que fue el despues de la fiesta."
elif "Luisa" in idea_rapida:
    prompt_por_defecto = "Dominican woman Luisa crying and shouting in a courtroom demanding 100 million pesos, Dominican actress, vertical 9:16 cinematic lighting, realistic face"
    audio_texto = "Luisa demanda a Hipolito por cien millones de pesos por abandono, traicion y maltrato psicologico. Durante diez años ella crio sola a sus tres hijos mientras el se gastaba todo en lujos, discotecas y mujeres. Pasaron hambre, frio y humillacion. Hoy por fin el juez la escucha y la justicia por fin llega para Luisa y sus niños. Esta es su venganza."

prompt_usuario = st.text_area("Prompt visual (en inglés para mejor resultado):", value=prompt_por_defecto, height=100)
guion_audio = st.text_area("Texto de la narración (Audio de la parodia):", value=audio_texto, height=150)

if st.button("🚀 Generar Contenido del Video", type="primary", use_container_width=True):
    if not prompt_usuario or not guion_audio:
        st.error("Por favor, completa tanto el prompt visual como el texto del audio.")
    else:
        with st.spinner("🎬 Generando escena y voz del drama..."):
            try:
                # AUDIO LARGO 30s QUE SI REPRODUCE
                tts = gTTS(text=guion_audio, lang='es', tld='com.mx', slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

                # IMAGEN QUE SI GENERA - ARREGLO DE TU ERROR
                seed = random.randint(1, 999999)
                url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_usuario + ' photorealistic, 4k') }?width=720&height=1280&seed={seed}&nologo=true&model=flux"
                r = requests.get(url_img, timeout=60)
                imagen = Image.open(io.BytesIO(r.content)).convert("RGB")

                st.success("✨ ¡Drama generado con éxito!")
                st.image(imagen, caption="Escena de la Parodia - 9:16", use_container_width=True)

                st.write("🎵 **Audio / Narración de la Parodia (30-35 seg):**")
                st.audio(audio_buffer, format="audio/mp3")
                
                st.info("💡 Ya tienes 30 seg. Si lo quieres de 60 seg, escribe el doble de texto en la narración.")
                
            except Exception as e:
                st.error(f"Hubo un inconveniente: {e}")
