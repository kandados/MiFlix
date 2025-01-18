import csv
from MiFlixApp.models import Pelicula, Serie

def cargar_peliculas():
    try:
        with open('scripts/peliculas.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    pelicula = Pelicula.objects.create(
                        titulo=row.get("titulo", "").strip(),
                        sinopsis=row.get("sinopsis", "").strip(),
                        estreno=int(row["estreno"]) if row.get("estreno") else None,
                        genero=row.get("genero", "").strip(),
                        director=row.get("director", "").strip(),
                        protagonistas=row.get("protagonistas", "").strip(),
                        duracion=int(row["duracion"]) if row.get("duracion") else None,
                        calificacion_usuario=float(row["calificacion_usuario"]) if row.get("calificacion_usuario") else None,
                        vistas_totales=int(row["vistas_totales"]) if row.get("vistas_totales") else 0,
                        image_cover=row.get("image_cover", "").strip(),
                    )
                    print(f"Pelicula '{pelicula.titulo}' creada.")
                except Exception as e:
                    print(f"Error al crear pelicula: {e}, datos: {row}")
    except FileNotFoundError:
        print("Archivo 'peliculas.csv' no encontrado.")

def cargar_series():
    try:
        with open('scripts/series.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    serie = Serie.objects.create(
                        titulo=row.get("titulo", "").strip(),
                        sinopsis=row.get("sinopsis", "").strip(),
                        estreno=int(row["estreno"]) if row.get("estreno") else None,
                        genero=row.get("genero", "").strip(),
                        director=row.get("director", "").strip(),
                        protagonistas=row.get("protagonistas", "").strip(),
                        temporadas_totales=int(row["temporadas_totales"]) if row.get("temporadas_totales") else None,
                        capitulos_totales=int(row["capitulos_totales"]) if row.get("capitulos_totales") else None,
                        duracion_media_capitulo=int(row["duracion_media_capitulo"]) if row.get("duracion_media_capitulo") else None,
                        calificacion_usuario=float(row["calificacion_usuario"]) if row.get("calificacion_usuario") else None,
                        vistas_totales=int(row["vistas_totales"]) if row.get("vistas_totales") else 0,
                        image_cover=row.get("image_cover", "").strip(),
                    )
                    print(f"Serie '{serie.titulo}' creada.")
                except Exception as e:
                    print(f"Error al crear serie: {e}, datos: {row}")
    except FileNotFoundError:
        print("Archivo 'series.csv' no encontrado.")

# Ejecutar funciones
cargar_peliculas()
cargar_series()
