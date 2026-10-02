// Playlist de drama - 3 escenas
reproductor.setOnEndOfMedia(() -> {
    System.out.println("Escena 1 termino, pasamos a escena 2");
    // aqui cargas el siguiente video de Luisa con los niños
});

reproductor.setStopTime(Duration.seconds(60)); // cada escena dura 1 min exacto
reproductor.play();
