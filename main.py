import subprocess
import re
from datetime import datetime

exif_tool_path = 'exiftool'
image_path = './images/2020-05-19__145947.JPG'
camara = None
fecha = None

def metadatos(imagen):
    """Devuelve el modelo de cámara y la fecha original
    """
    process = subprocess.Popen(
            [exif_tool_path, imagen],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)

    for tag in process.stdout:
        line = tag.strip().split(':', 1)
        if line[0].strip() == 'Camera Model Name':
            camara = line[-1].strip()
        if line[0].strip() == r'Date/Time Original':
            fecha = line[-1].strip()
            fecha = fecha[:10].replace(':', '-')

    # print(f'Camara: {camara}')
    # print(f"Fecha: {fecha}")
    return camara, fecha

def renombra(imagen):
    imagen = imagen.lower()
    patron1 = re.compile(
            r'''                # busca ./images/2020-05-19__145947.jpg
            ^(.*/)              # ruta
            (\d{4}-\d{2}-\d{2}) # fecha
            (__)                # guiones
            (\d{4,6}?)$         # contador
            (.jpg)              # extension
            ''', re.VERBOSE)

    patron2 = re.compile(
            r'''                # busca ./images/2014.12.19 - X-E2 - 0007.jpg
            ^(.*/)              # ruta ./images/
            (\d{4}\.\d{2}\.\d{2}) # fecha 2014.12.19
            (\s-.*-\s)          # camara ' - X-E2 - '
            (\d{4,6}?)          # contador
            (.jpg)              # extension
            ''', re.VERBOSE)

    return nombre_sin_ext

if __name__ == "__main__":
    print(metadatos(image_path))
    print(renombra(image_path))
