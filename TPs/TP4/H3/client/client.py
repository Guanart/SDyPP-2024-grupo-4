import requests

def configurar_ip():
    global server_ip
    server_ip = input("Ingrese la IP del servidor al que quiere acceder: ")

def enviar_imagen():
    global server_ip
    if not server_ip:
        print("Por favor, configure la dirección IP del servidor primero.")
        return
    url = "http://" + server_ip + ":80/sobel"
    path_imagen = input("Ingrese la ruta de la imagen: ")
    filas = input("Número de partes filas: ")
    columnas = input("Número de partes columnas: ")
    with open(path_imagen, 'rb') as img:
        files = {"imagen": img}
        data = {"filas": filas, "columnas": columnas}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            id = response.text
            print("Este es el ID de la imagen:", id)
        else:
            print(f"Error {response.status_code}: {response.text}")

def enviar_id():
    global server_ip
    if not server_ip:
        print("Por favor, configure la dirección IP del servidor primero.")
        return
    id = input("Ingrese el ID: ")
    url = 'http://' + server_ip + ':80/getImage?id=' + id;
    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if content_type == 'image/jpeg':
            with open('imagen_sobel.jpg', 'wb') as f:
                f.write(response.content)
            print("Imagen obtenida, guardada como imagen_sobel.jpg")
        else:
            print(response.text) 
    else:
        print(f"Error {response.status_code}: {response.text}")

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