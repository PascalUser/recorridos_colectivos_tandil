"""

Que hace este script:
    Genera un archivo JSON a partir de un archivo KML que contiene las líneas de colectivo
    de la ciudad de Tandil, Buenos Aires, Argentina. 
    Se utiliza el script tratar_kml.py para procesar el archivo KML y extraer la información
    necesaria, que luego se guarda en un archivo JSON.
    
Como lo hace:
    Utiliza la función procesar_kml del script tratar_kml.py para extraer las líneas de colectivo
    y sus coordenadas del archivo KML.
    Utiliza la biblioteca json para guardar la información extraída en un archivo JSON.
"""

import json
from tratar_kml import procesar_kml
path_salida = "lineas_colectivo_tandil.json"

def normalizar_nombre(lineas_dict):
    """
    Normaliza el nombre de la línea de colectivo para que sea más legible.
    
    Args:
        lineas_dict (dict): Diccionario que contiene la información de la línea.
        
    Returns:
        str: Diccionario con el nombre normalizado.
    """
    
    # Convertir a minúsculas y reemplazar espacios por guiones bajos
    lineas_dict['linea'] = lineas_dict['linea'].lower().replace(" ", "_")

    # Eliminar caracteres especiales (el acento)
    lineas_dict['linea'] = lineas_dict['linea'].replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

    return lineas_dict

def generar_json():
    lineas_colectivo = procesar_kml("gobierno-abierto-tandil-recorridos-transporte-urbano-1.kml")
    
    for linea in lineas_colectivo:
        # Normalizar el nombre de la línea
        linea_normalizada = normalizar_nombre(linea)
        # Actualizar el diccionario con el nombre normalizado
        linea.update(linea_normalizada)

    json_data = {}

    for linea in lineas_colectivo:
        nombre = linea['linea']  # ya normalizado, por ejemplo "linea_500"
        coordenadas = linea['coordenadas']

        json_data[nombre] = coordenadas

    # Guardar como JSON
    with open(path_salida, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Archivo JSON generado correctamente en: {path_salida}")


if __name__ == "__main__":
    generar_json()
    print("Archivo JSON generado exitosamente.")
    
    # Testing unit
    # Escribir todas las lineas presentes en el JSON
    with open(path_salida, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Líneas de colectivo encontradas:")
        for linea in data.keys():
            print(linea)