import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.util.Duration;
import java.io.File;

// 1. Cargar video
String ruta = new File("tu_video.mp4").toURI().toString();
Media media = new Media(ruta);
MediaPlayer reproductor = new MediaPlayer(media);
MediaView vista = new MediaView(reproductor);

// 2. Poner la vista en tu Scene (ejemplo: root.getChildren().add(vista);)

// 3. Reproducir
reproductor.play();

// 4. CONTROL DE TIEMPO - Detener a 1 minuto
reproductor.currentTimeProperty().addListener((obs, viejo, nuevo) -> {
    if (nuevo.greaterThanOrEqualTo(Duration.seconds(60))) {
        reproductor.stop();
        System.out.println("Video detenido a 1 minuto");
    }
});
