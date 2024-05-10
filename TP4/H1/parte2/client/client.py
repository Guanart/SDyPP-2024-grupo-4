import requests
import pathlib

url = "http://localhost:5000/sobel"


archivo_imagen = str(pathlib.Path(__file__).parent.resolve()) + '/gato.jpg'

# Abrir el archivo de la imagen en modo binario
with open(archivo_imagen, 'rb') as archivo:
    # Leer el contenido del archivo
    imagen = archivo.read()

    # Establecer los encabezados con el tipo de contenido correcto
    headers = {"Content-Type": "image/jpeg"}

    # Hacer la solicitud POST enviando la imagen en el cuerpo
    response = requests.post(url, data=imagen, headers=headers)

if response.status_code == 200:
    id = response.text
    print("ID:", id)
else:
    print("Error " + str(response.status_code) + ": " + response.text)
