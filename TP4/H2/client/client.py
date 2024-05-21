import requests

def configurar_ip():
    server_ip = input("Ingrese la IP del servidor al que quiere acceder: ")

def enviar_imagen():
    if not server_ip:
        print("Por favor, configure la dirección IP del servidor primero.")
        return
    path_imagen = input("Ingrese la ruta de la imagen: ")
    with open(path_imagen, 'rb') as archivo:
        imagen = archivo.read()
        url = 'http://' + server_ip + ':5000/sobel'
        response = requests.post(url, data=imagen, headers={"Content-Type": "image/jpeg"})
        if response.status_code == 200:
            id = response.text
            print("Este es el ID de la imagen:", id)
        else:
            print("Error " + str(response.status_code) + ": " + response.text)

def enviar_id():
    if not server_ip:
        print("Por favor, configure la dirección IP del servidor primero.")
        return
    id = input("Ingrese el ID: ")
    url = 'http://' + server_ip + ':5000/getImage?id=' + id;
    response = requests.get(url)
    if response.status_code == 200:
        with open('imagen_sobel.jpg', 'wb') as f:
            f.write(response.content)
        print("Imagen obtenida, guardada como imagen_sobel.jpg")
    else:
        print("Error " + str(response.status_code) + ": " + response.text)

def mostrar_menu():
    print("Bienvenido al menú:")
    while True:
        print("-- OPCIONES --")
        print("1. Configurar IP del servidor")
        print("2. Enviar una imagen")
        print("3. Enviar un ID para conseguir la imagen con sobel")
        print("0. Salir")
        opcion = input("Ingrese el número de la opción: ")

        if opcion == "1":
            configurar_ip()
        elif opcion == "2":
            enviar_imagen()
        elif opcion == "3":
            enviar_id()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

if __name__ == '__main__':
    server_ip = ""
    mostrar_menu()