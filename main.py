import sys
import os
import re
import subprocess
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

exif_tool_path = 'exiftool'
# image_path = './images/2020-05-19__145947.JPG'

def get_camara_fecha(imagen):
    """
    Devuelve el modelo de cámara y la fecha original
    """
    camara, fecha = '', ''
    
    process = subprocess.Popen(
            [exif_tool_path, imagen],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)

    for tag in process.stdout:
        line = tag.strip().split(':', 1)
        if line[0].strip() == 'Camera Model Name':
            camara = line[-1].strip()
            camara = camara.replace(' ', '_')
        if line[0].strip() == r'Date/Time Original':
            fecha = line[-1].strip()
            fecha = fecha[:10].replace(':', '-')

    return camara, fecha

def get_numeracion(imagen):
    """
    Devuelve la numeración de la foto
    """
    imagen = imagen.lower()
    patron = re.compile(r'(\d{4,6})(.JPG|.jpg)')
    numeracion = patron.search(imagen)
    if numeracion is not None:
        return numeracion.group(1)
    else:
        return '000001'

def get_path():
    """
    Devuelve la ruta de la imagen
    """
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
            initialdir='./',
            filetypes=(("Image File", "*.jpg"),),
            title="Selecciona el fichero JPG")
    return file_path

def renombra(directorio):
    os.chdir(directorio)
    archivos = os.listdir()
    # print(archivos)
    imagenes = []
    for archivo in archivos:
        if archivo.lower().endswith('.jpg'):
            imagenes.append(archivo)

    sin_renombrar = []
    for imagen in imagenes:
        camara, fecha = get_camara_fecha(imagen)
        if camara == '' and fecha == '':
            sin_renombrar.append(imagen)
            imagenes.remove(imagen)
        else:
            numeracion = get_numeracion(imagen)
            nuevo_nombre_imagen = fecha + '_' + camara + '_' + numeracion + '.jpg'
            print(f'{imagen} -> {nuevo_nombre_imagen}')

    if sin_renombrar:
        print('\nNo se han podido renombrar:')
        for imagen in sin_renombrar:
            print(f'\t{imagen}')

    renombrar = input("\nRenombrar? (S/N): ")
    print()
    if renombrar == 'S' or renombrar == 's':
        for imagen in imagenes:
            camara, fecha = get_camara_fecha(imagen)
            numeracion = get_numeracion(imagen)
            nuevo_nombre_imagen = fecha + '_' + camara + '_' + numeracion + '.jpg'
            shutil.move(imagen, nuevo_nombre_imagen)
            print(f"Renombrado {imagen} a {nuevo_nombre_imagen}")


if __name__ == "__main__":
    directorio = os.path.abspath(sys.argv[1])
    print(f"Directorio: {directorio}")
    renombra(directorio)
