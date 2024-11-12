import os
import csv
from django.core.management.base import BaseCommand
from django.core.files import File
from contenido.models import Contenido
from django.conf import settings

class Command(BaseCommand):
    help = "Carga películas desde un archivo CSV y guarda las imágenes"

    def handle(self, *args, **kwargs):
        # Ruta al archivo CSV
        ruta_csv = os.path.join(settings.BASE_DIR, 'detalles_peliculas.csv')
        ruta_imagenes = os.path.join(settings.BASE_DIR, 'carteles')

        with open(ruta_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Crear un nuevo objeto de Contenido
                contenido, creado = Contenido.objects.get_or_create(
                    titulo=row['Titulo'],
                    defaults={
                        'genero': row['Genero'],
                        'duracion': int(row['Duracion']) if row['Duracion'].isdigit() else None,
                        'director': row['Director'],
                        'protagonistas': row['Actores Principales'],
                        'estreno': row['Año de estreno'],
                        'sinopsis': row['Sinopsis']
                    }
                )

                if creado:
                    # Cargar la imagen del cartel
                    nombre_imagen = f"{row['Titulo']}.jpg"  # Ajusta según el nombre de los archivos de imagen
                    ruta_imagen = os.path.join(ruta_imagenes, nombre_imagen)
                    if os.path.exists(ruta_imagen):
                        with open(ruta_imagen, 'rb') as img_file:
                            contenido.imagen_cartel.save(nombre_imagen, File(img_file), save=True)

                    print(f"La Película '{contenido.titulo}' ha sido guardada en la base de datos.")
                else:
                    print(f"La Película '{contenido.titulo}' ya existe en la base de datos.")
