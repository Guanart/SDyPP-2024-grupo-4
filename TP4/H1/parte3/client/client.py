import requests
import pathlib

archivo_imagen = str(pathlib.Path(__file__).parent.resolve()) + '/gato.jpg'

def enviar_imagen():
    path_imagen = input("Ingrese la ruta de la imagen: ")
    with open(path_imagen, 'rb') as archivo:
        imagen = archivo.read()
        response = requests.post("http://localhost:5000/sobel", data=imagen, headers={"Content-Type": "image/jpeg"})
        if response.status_code == 200:
            id = response.text
            print("Este es el ID de la imagen:", id)
        else:
            print("Error " + str(response.status_code) + ": " + response.text)

def enviar_id():
    id = input("Ingrese el ID: ")
    url = 'http://localhost:5000/getImage?id=' + id;
    response = requests.get(url)
    if response.status_code == 200:
        with open('imagen_sobel.jpg', 'wb') as f:
            f.write(response.content)
        print("Imagen obtenida, guardada como imagen_sobel.jpg")
    else:
        print("Error " + str(response.status_code) + ": " + response.text)

if __name__ == '__main__':
    print("Seleccione una opción:")
    print("1. Enviar una imagen")
    print("2. Enviar un ID para conseguir la imagen con sobel")
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        enviar_imagen()
    elif opcion == "2":
        enviar_id()
    else:
        print("Opción no válida")
