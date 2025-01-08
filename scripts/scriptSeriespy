import requests
from PIL import Image
from io import BytesIO
import os
import csv

# Configuración de la API de TMDb
API_KEY = '9c5f70e89b5b072544cb1b99d5f89096'  # Reemplaza con tu clave de API de TMDb
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'  # Tamaño de imagen (w500 es buena resolución)

# Lista de series iniciales
series = [
    "Friends",
    "The Simpsons",
    "Sherlock",
    "The Crown",
    "House of the Dragon",
    "Better Call Saul",
    "The Last of Us",
    "Loki",
    "WandaVision",
    "Dark",
    "The Boys",
    "Chernobyl",
    "The Wire",
    "True Detective",
    "Dexter",
    "Narcos",
    "Mindhunter",
    "Luther",
    "The Shield",
    "Daredevil",
    "Jessica Jones",
    "Luke Cage",
    "Iron Fist",
    "The Defenders",
    "Agents of S.H.I.E.L.D.",
    "The Falcon and the Winter Soldier",
    "Hawkeye",
    "Avatar: The Last Airbender",
    "The Legend of Korra",
    "Rick and Morty",
    "BoJack Horseman",
    "Big Mouth",
    "Adventure Time",
    "Futurama",
    "Gravity Falls",
    "Invincible",
    "Arcane",
    "Shadow and Bone",
    "His Dark Materials",
    "The Sandman",
    "Carnival Row",
    "The Wheel of Time",
    "Good Omens",
    "Locke & Key"

]

# Crear carpetas para almacenar los carteles y tráileres
if not os.path.exists("carteles_series"):
    os.makedirs("carteles_series")

if not os.path.exists("trailers_series"):
    os.makedirs("trailers_series")

# Crear el archivo CSV para almacenar los detalles de las series
with open("detalles_series.csv", mode="w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["Titulo", "Genero", "Episodios Totales", "Temporadas Totales", "Año de estreno", "Calificación",
                  "Director", "Sinopsis", "Protagonistas", "Trailer"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Escribir los encabezados del archivo CSV

    def obtener_id_serie(titulo):
        """Obtiene el ID de la serie en TMDb para un título dado."""
        url = f"{BASE_URL}/search/tv"
        params = {
            'api_key': API_KEY,
            'query': titulo,
            'language': 'es-ES'  # Solicitar los resultados en español
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data['results']:
            return data['results'][0]['id']
        else:
            print(f"No se encontró la serie: {titulo}")
            return None

    def descargar_cartel_serie(id_serie, titulo):
        """Descarga el cartel de una serie por su ID y lo guarda."""
        url = f"{BASE_URL}/tv/{id_serie}"
        params = {
            'api_key': API_KEY,
            'language': 'es-ES'
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            poster_url = IMAGE_BASE_URL + data['poster_path']
            response = requests.get(poster_url)

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(f"carteles_series/{titulo}.jpg")
                print(f"Cartel descargado para '{titulo}'")
            else:
                print(f"No se pudo descargar el cartel de '{titulo}'")
        else:
            print(f"No hay cartel disponible para '{titulo}'")

    def descargar_trailer_serie(id_serie, titulo):
        """Descarga el tráiler de una serie por su ID."""
        url = f"{BASE_URL}/tv/{id_serie}/videos"
        params = {
            'api_key': API_KEY,
            'language': 'es-ES'  # Solicitar los videos en español
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Buscar un tráiler oficial en los resultados
        trailer_url = None
        for video in data.get('results', []):
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                break

        if trailer_url:
            with open(f"trailers_series/{titulo}.txt", "w", encoding="utf-8") as trailer_file:
                trailer_file.write(trailer_url)
            print(f"Tráiler guardado para '{titulo}': {trailer_url}")
            return trailer_url
        else:
            print(f"No se encontró tráiler para '{titulo}'")
            return None

    def obtener_detalles_serie(id_serie, titulo):
        """Obtiene detalles adicionales de la serie y los guarda en el archivo CSV."""
        url = f"{BASE_URL}/tv/{id_serie}"
        params = {
            'api_key': API_KEY,
            'language': 'es-ES',
            'append_to_response': 'credits'
        }
        response = requests.get(url, params=params)
        data = response.json()

        titulo = data.get('name', 'Desconocido')
        ano_estreno = data.get('first_air_date', 'Desconocido').split("-")[0]
        temporadas_totales = data.get('number_of_seasons', 'Desconocido')
        episodios_totales = data.get('number_of_episodes', 'Desconocido')
        sinopsis = data.get('overview', 'Sin sinopsis disponible')
        calificacion = data.get('vote_average', 'N/A')
        genero = data['genres'][0]['name'] if data.get('genres') else 'Desconocido'

        director = "Desconocido"
        for person in data.get('credits', {}).get('crew', []):
            if person['job'] == 'Director':
                director = person['name']
                break

        protagonistas = [actor['name'] for actor in data.get('credits', {}).get('cast', [])[:5]]
        trailer_url = descargar_trailer_serie(id_serie, titulo)

        writer.writerow({
            "Titulo": titulo,
            "Genero": genero,
            "Episodios Totales": episodios_totales,
            "Temporadas Totales": temporadas_totales,
            "Año de estreno": ano_estreno,
            "Calificación": calificacion,
            "Director": director,
            "Sinopsis": sinopsis,
            "Protagonistas": ', '.join(protagonistas),
            "Trailer": trailer_url or "No disponible"
        })
        print(f"Detalles guardados para '{titulo}'")

    for titulo in series:
        id_serie = obtener_id_serie(titulo)
        if id_serie:
            descargar_cartel_serie(id_serie, titulo)
            obtener_detalles_serie(id_serie, titulo)
