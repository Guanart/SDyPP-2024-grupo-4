import requests

def enviar_imagen():
    url = "http://localhost:5000/sobel"
    path_imagen = input("Ingrese la ruta de la imagen: ")
    filas = input("Número de partes filas: ")
    columnas = input("Número de partes columnas: ")
    with open(path_imagen, 'rb') as img:
        files = {"imagen": img}
        data = {"filas": filas, "columnas": columnas}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            id = response.text
            print(f"Este es el ID de la imagen: {id}")
        else:
            print(f"Error {response.status_code}: {response.text}")


def enviar_id():
    id = input("Ingrese el ID: ")
    url = "http://localhost:5000/getImage?id=" + id;
    response = requests.get(url)
    if response.status_code == 200:
        with open('imagen_sobel.jpg', 'wb') as f:
            f.write(response.content)
        print("Imagen obtenida, guardada como imagen_sobel.jpg")
    else:
        print(f"Error {response.status_code}: {response.text}")


if __name__ == '__main__':
    print("Seleccione una opción:")
    print("1. Enviar una imagen y numero de partes en filas y columnas")
    print("2. Enviar un ID para conseguir la imagen con sobel")
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        enviar_imagen()
    elif opcion == "2":
        enviar_id()
    else:
        print("Opción no válida")

def mostrar_menu():
    print("Bienvenido al menú:")
    while True:
        print("-- OPCIONES --")
        print("1. Enviar una imagen")
        print("2. Enviar un ID para conseguir la imagen con sobel")
        print("0. Salir")
        opcion = input("Ingrese el número de la opción: ")
        if opcion == "1":
            enviar_imagen()
        elif opcion == "2":
            enviar_id()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

if __name__ == '__main__':
    mostrar_menu()