"""

Que hace este script:
    Tratamiento del archivo KML, el cual contiene las lineas de colectivo para
    la ciudad de Tandil, Buenos Aires, Argentina.
    Este script procesa el archivo KML, extrae las coordenadas de las líneas
    de colectivo y las convierte a un formato adecuado para su visualización
    en un mapa interactivo posteriormente.
    Las coordenadas se almacenan en la 

Como lo hace:
    Extrae por separado cada campo dentro de cada tag 'placemark'
    Extrae el nombre de la línea, el color y las coordenadas
    Elimina tags, espacios y caracteres innecesarios
    Convierte las coordenadas a un formato de lista de tuplas

"""

import xml.etree.ElementTree as ET

# Función para procesar el archivo KML y extraer las líneas de colectivo
def procesar_kml(archivo_kml, solo_lineas=True):
    """
    Procesa un archivo KML y extrae las líneas de colectivo y coordenadas.
    
    Args:
        archivo_kml (str): Ruta al archivo KML a procesar.
        solo_lineas (bool): Si True, filtra solo las líneas de colectivo. Caso contrario,
                            extrae también las locaciones destacadas guardadas en el KML.

    Returns:
        list: Lista de diccionarios con la información de cada línea de colectivo.
    """
    tree = ET.parse(archivo_kml)
    root = tree.getroot()

    # namespace del KML (para que detecte los tags)
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    lineas = []
    
    for placemark in root.findall('.//kml:Placemark', ns):
        # Extraer el nombre de la linea
        nombre = placemark.find('kml:name', ns).text.strip()
        
        # Extraer las coordenadas (puntos por donde pasa la linea)
        coordenadas_str = placemark.find('.//kml:coordinates', ns).text.strip()
        
        # Convertir coordenadas a lista de tuplas
        coordenadas = [
            list(map(float, coord.split(','))) for coord in coordenadas_str.split()
        ] # Se utiliza list en lugar de tuple para facilitar el paso a JSON (no soporta tuplas)
        
        # Elimina el valor 0 de la coordenada Z (altitud) e invertimos latitud y longitud
        # ya que KML usa (lon, lat, alt) y queremos (lat, lon)
        coordenadas = [(lat, lon) for lon, lat, _ in coordenadas]
        
        lineas.append({
            'linea': nombre,
            'coordenadas': coordenadas
        })
    
    # Si solo queremos las líneas de colectivo, filtramos las que no son
    if solo_lineas:
        lineas = [linea for linea in lineas if 'línea' in linea['linea'].lower()]
    
    return lineas

# Testing unit
if __name__ == "__main__":
    archivo_kml = 'gobierno-abierto-tandil-recorridos-transporte-urbano-1.kml'
    lineas_colectivo = procesar_kml(archivo_kml)
    
    # Imprimir las lineas de colectivo procesadas
    for linea in lineas_colectivo:
        print(f"Línea: {linea['linea']}, Coordenadas: {linea['coordenadas'][:3]}...")