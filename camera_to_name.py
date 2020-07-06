"""
Añade el modelo de cámara y la fecha de la imagen a las fotos que se
encuentren en el directorio pasado como argumento.

Modo de uso:
python camera_to_name.py path
"""


import sys
import os
import re
from subprocess import Popen, PIPE, STDOUT
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Herramienta instalada en el sistema para la lectura de metadatos.
# https://exiftool.org
exif_tool_path = 'exiftool'

def check_exiftool():
    """
    Comprueba que esté instalada la utilidad exiftool.
    """
    try:
        Popen([exif_tool_path, '--help'], stdout=PIPE, stderr=PIPE)
    except OSError:
        msg = "Es necesario tener instalado exiftool para poder ejecutar este script"
        sys.exit(msg)
    return

def get_camara_fecha(imagen):
    """
    Devuelve el modelo de cámara y la fecha original
    """
    camara, fecha = '', ''
    
    process = Popen(
            [exif_tool_path, imagen],
            stdout=PIPE,
            stderr=STDOUT,
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
    patron = re.compile(r'(\d{4,6})(.jpg)')
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
    """
    Muestra las imagenes que se pueden renombrar y el nombre que les asignará,
    y pregunta si procede con el renombrado, en cuyo caso renombrará todas las
    imágenes que se puedean renombrar. En el caso de que existan imágenes que 
    no pueda renombrar, se mostrarán, avisando de que no se pueden renombrar.
    """
    os.chdir(directorio)
    archivos = os.listdir()
    imagenes = []
    for archivo in archivos:
        if archivo.lower().endswith('.jpg'):
            imagenes.append(archivo)

    renombrables = {}
    sin_renombrar = []
    for imagen in imagenes:
        camara, fecha = get_camara_fecha(imagen)
        if camara == '' or fecha == '':
            sin_renombrar.append(imagen)
        else:
            numeracion = get_numeracion(imagen)
            nuevo_nombre_imagen = fecha + '_' + camara + '_' + numeracion + '.jpg'
            renombrables[imagen] = nuevo_nombre_imagen

    if sin_renombrar:
        print('\nNo se puede renombrar:')
        for imagen in sin_renombrar:
            print('\t{}'.format(imagen))

    print("\nFotos a renombrar:")
    for img in renombrables:
        print('\t{} ->\t{}'.format(img, renombrables[img]))

    renombrar = input("\nRenombrar? (S/N): ")
    print()
    if renombrar == 'S' or renombrar == 's':
        for img in renombrables:
            shutil.move(img, renombrables[img])
            print("Renombrado {} a {}".format(img, nuevo_nombre_imagen))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise IndexError("Modo de uso: python main.py path")
    else:
        check_exiftool()
        directorio = os.path.abspath(sys.argv[1])
        print("Directorio: {}".format(directorio))
        renombra(directorio)
