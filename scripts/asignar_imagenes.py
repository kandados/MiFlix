import os
from django.core.files import File
from MiFlixApp.models import Pelicula, Serie

def asignar_imagenes_peliculas(imagenes_dir):
    peliculas = Pelicula.objects.all()
    for pelicula in peliculas:
        # Construir el nombre de archivo basado en el título
        imagen_nombre = f"{pelicula.titulo.replace(' ', '_')}.jpg"
        imagen_path = os.path.join(imagenes_dir, imagen_nombre)

        if os.path.exists(imagen_path):
            with open(imagen_path, 'rb') as imagen_file:
                pelicula.image_cover.save(imagen_nombre, File(imagen_file))
                print(f"Imagen asignada para la película: {pelicula.titulo}")
        else:
            print(f"No se encontró imagen para la película: {pelicula.titulo}")

def asignar_imagenes_series(imagenes_dir):
    series = Serie.objects.all()
    for serie in series:
        # Construir el nombre de archivo basado en el título
        imagen_nombre = f"{serie.titulo.replace(' ', '_')}.jpg"
        imagen_path = os.path.join(imagenes_dir, imagen_nombre)

        if os.path.exists(imagen_path):
            with open(imagen_path, 'rb') as imagen_file:
                serie.image_cover.save(imagen_nombre, File(imagen_file))
                print(f"Imagen asignada para la serie: {serie.titulo}")
        else:
            print(f"No se encontró imagen para la serie: {serie.titulo}")

# Ejemplo de uso
asignar_imagenes_peliculas('media/movie_images')
asignar_imagenes_series('media/series_images')
