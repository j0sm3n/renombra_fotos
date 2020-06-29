import subprocess
import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import os

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


# if __name__ == "__main__":
#     camara, fecha = get_camara_fecha(image_path)
#     numeracion = get_numeracion(image_path)
#     nombre_fichero = fecha + '_' + camara + '_' + numeracion + '.jpg'
#     print(nombre_fichero)

# fullpath = get_path()
# dirpath = os.path.dirname(fullpath)
# os.chdir(dirpath)
os.chdir('./images')
archivos = os.listdir()
# print(archivos)
imagenes = []
sin_renombrar = []
for archivo in archivos:
    if archivo.lower().endswith('.jpg'):
        imagenes.append(archivo)
print(imagenes)
print()
for imagen in imagenes:
    camara, fecha = get_camara_fecha(imagen)
    if camara == '' and fecha == '':
        sin_renombrar.append(imagen)
    else:
        numeracion = get_numeracion(imagen)
        nuevo_nombre_imagen = fecha + '_' + camara + '_' + numeracion + '.jpg'
        print(f'{imagen} -> {nuevo_nombre_imagen}')

print('\nNo se ha renombrado:')
for imagen in sin_renombrar:
    print(f'\t{imagen}')