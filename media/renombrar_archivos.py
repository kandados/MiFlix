import os

def renombrar_archivos(carpeta):
    # Verifica que la carpeta exista
    if not os.path.exists(carpeta):
        print(f"La carpeta '{carpeta}' no existe.")
        return

    # Recorre todos los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        # Verifica si es un archivo
        ruta_completa = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_completa):
            # Reemplaza los espacios por guiones bajos
            nuevo_nombre = archivo.replace(" ", "_")
            ruta_nueva = os.path.join(carpeta, nuevo_nombre)
            # Renombra el archivo
            os.rename(ruta_completa, ruta_nueva)
            print(f"Renombrado: '{archivo}' -> '{nuevo_nombre}'")
        else:
            print(f"Ignorado (no es un archivo): {archivo}")

# Especifica la carpeta con los archivos
carpeta = input("Introduce la ruta de la carpeta con los archivos a renombrar: ").strip()
renombrar_archivos(carpeta)
