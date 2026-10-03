import os

def crear_repositorio_guion():
    # Crear estructura de carpetas si es necesario
    os.makedirs("contenido", exist_ok=True)
    
    guion_content = """# 🎬 Guion de YouTube: La Era de Trump y los Contrapesos de Poder

## 📌 Información del Proyecto
* **Canal:** [Tu Nombre de Canal de YouTube]
* **Formato:** Video Horizontal (16:9) / Ensayo Visual
* **Duración Estimada:** 1:30 - 2:00 minutos
* **Licencia:** MIT

---

## 🎭 Escena 1: El Límite del Poder

| Tiempo | Componente Visual (B-Roll / Gráficos) | Audio (Voz en Off / Presentador) | Efectos de Sonido (SFX) |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:15** | **[Gancho]** Plano medio del presentador mirando fijamente a cámara. Fondo con iluminación sutil azul y roja. | "Imagínate esto: un presidente acorralado políticamente, tensiones globales al límite y una crisis internacional en marcha. De repente, el líder de la potencia más grande del mundo decide firmar un decreto para cancelar las próximas elecciones presidenciales y quedarse en el poder. **¿Es esto legalmente posible?**" | *Música de tensión baja de fondo.* |
| **0:15 - 0:25** | Corte rápido. Texto dinámico en pantalla: **¿CONTROL TOTAL?** | "Hoy vamos a derribar mitos y ver qué dice realmente la ley sobre el control absoluto en la era moderna. Quédate, porque la respuesta de la Constitución te va a sorprender." | *SFX: Swoosh de transición.* |
| **0:25 - 0:55** | B-Roll de filas de votantes, imágenes del Capitolio de EE. UU. e infografía animada sobre la ley de 1845. | "Muchos piensan que en momentos de extrema tensión, un presidente puede usar un 'estado de emergencia' para suspender la democracia. Pero en los Estados Unidos, el sistema se diseñó precisamente para evitar que una sola persona tenga ese nivel de control. Primero: el presidente **no** tiene la facultad de cambiar la fecha de las elecciones. Esa autoridad le pertenece exclusivamente al Congreso." | *La música sube a un ritmo más dinámico de investigación.* |
| **0:55 - 1:20** | Animación digital de un calendario digital deteniéndose de golpe en la fecha **"20 de ENERO"**. | "Y aquí viene el contrapeso definitivo: la **Enmienda 20 de la Constitución** es implacable. Dice que el mandato presidencial termina el 20 de enero al mediodía. Sí o sí. Si no hay elecciones por una crisis extrema, el poder pasa automáticamente a la línea de sucesión legislativa. El mandatario actual quedaría fuera de juego de todos modos." | *SFX: Reloj digital haciendo tic-tac.* |
| **1:20 - 1:45** | **[Cierre]** Vuelve el presentador a plano medio. Aparecen recuadros en los laterales para recomendar videos anteriores. | "El diseño del poder obliga a que, tarde o temprano, incluso los líderes más fuertes tengan que negociar si pierden las cámaras legislativas. Si te apasiona el ajedrez político mundial, dale un buen botón de **Like**, suscríbete y activa la campanita. Dime en los comentarios: ¿Crees que estos contrapesos son suficientes? ¡Te leo abajo!" | *Música épica de cierre en aumento.* *SFX: Campanita de notificación.* |

---

## 🚀 Instrucciones de Producción para el Editor
1. **Ritmo de Corte:** Mantener cortes rápidos cada 4-5 segundos durante la sección de B-Roll para maximizar la retención.
2. **Paleta de Colores:** Utilizar esquemas de color contrastantes (azul oscuro `#0d1b2a` y acentos rojos `#e63946`) para los textos en pantalla.
3. **Audio:** Mantener la voz del locutor a -6dB y la música de fondo a -22dB durante la locución.
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(guion_content.strip())
    print("[OK] Archivo README.md generado exitosamente para tu repositorio de GitHub.")

if __name__ == "__main__":
    crear_repositorio_guion()
