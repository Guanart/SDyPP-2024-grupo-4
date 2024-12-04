from flask import jsonify
import requests
import json
import os
import ipaddress

tasks = {
    "suma": "grupo4sdypp2024/tp2-h1-task1",
    "resta": "grupo4sdypp2024/tp2-h1-task2",
    "multiplicacion": "grupo4sdypp2024/tp2-h1-task3"
}


# Menu de opciones
def menu(tareaActual):
    print(f"""
----------- Cliente -----------

Ingrese una opción:
    1. Resolver tarea
    2. Cambiar de tarea (Tarea actual: {tareaActual})
    3. Ingresar datos del servidor
    0. Salir

""")
    try:
            opcion = int(input("Ingrese un número entero: "))
            return opcion
    except ValueError:
        opcion=-1
        input("Por favor, ingrese un número entero válido. (presione ENTER)")
    if opcion<0 or opcion>3:
        opcion=-1
        input("Por favor, ingrese un número entero válido. (presione ENTER)")

def limpiar_consola():
    os.system("cls")



# Envio una tarea
def enviarTarea(host,port,tareaActual):
    if host=="" or port==0:
        input("Por favor, ingrese la IP y el puerto del servidor. (presione ENTER)")
        return
    url = "http://"+str(host)+":"+str(port)+"/getRemoteTask"

    limpiar_consola()
    print("""
----------- Enviar Tarea -----------
Ingrese el primer numero:
""")
    valido=False
    while (not valido):
        try:
                numero1 = int(input("Debe ser un número entero: "))
                valido=True
        except ValueError:
            input("Por favor, ingrese un número entero válido. (presione ENTER)")
            limpiar_consola()

    limpiar_consola()
    print("""
----------- Enviar Tarea -----------
Ingrese el segundo numero:
""")
    valido=False
    while (not valido):
        try:
                numero2 = int(input("Debe ser un número entero: "))
                valido=True
        except ValueError:
            input("Por favor, ingrese un número entero válido. (presione ENTER)")
            limpiar_consola()

    data = {
        "image": tasks[tareaActual],
        "number1": numero1,
        "number2": numero2
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    limpiar_consola()
    print("Esto tardará de 15 a 20 segundos...")
    response = requests.post(url, data=json_data, headers=headers)
    print(response)
    print(response.text)
    input("Presione ENTER para continuar.")



# Cambiar entre tareas
def cambiarTarea():
    limpiar_consola()
    tareaActual = "suma"
    print("""
----------- Cambiar Tarea -----------

1. Suma
2. Resta
3. Multiplicación

""")
    valido=False
    while (not valido):
        try:
            opcion = int(input("Debe ser un número entero: "))
            valido=True
        except ValueError:
            input("Por favor, ingrese un número entero válido. (presione ENTER)")
            limpiar_consola()
        if opcion<1 or opcion>3:
            input("Por favor, ingrese un número entero válido. (presione ENTER)")
            limpiar_consola()
    if opcion == 1:
        tareaActual="suma"
    elif opcion == 2:
        tareaActual="resta"
    elif opcion == 3:
        tareaActual="multiplicacion"
    return tareaActual



# se ingresa la ip y puerto del servidor
def ingresarHost():
    limpiar_consola()
    print("""
----------- Ingresar datos servidor -----------
""")
    valido=False
    while (not valido):
        try:
            host = input("Ingrese la IP del servidor: ")
            ipaddress.ip_address(host)
            valido=True
        except:
            input("Por favor, ingrese una IP válida. (presione ENTER)")
            limpiar_consola()
    
    limpiar_consola()
    print("""
----------- Ingresar datos servidor -----------
""")
    valido=False
    while (not valido):
        try:
            port = int(input("Ingrese el puerto de escucha del servidor: "))
            ipaddress.ip_address(host)
            valido=True
        except ValueError:
            input("Por favor, ingrese un entero válido. (presione ENTER)")
            limpiar_consola()
    return host, port



def cliente():
    salir=True
    tareaActual = "suma"
    host=""
    port=0
    while(salir):
        limpiar_consola()
        opcion = menu(tareaActual)
        if opcion == 0:
            salir=False
        elif opcion == 1:
            enviarTarea(host,port,tareaActual)
        elif opcion == 2:
            tareaActual=cambiarTarea()
        elif opcion == 3:
            host,port = ingresarHost()

if __name__ == '__main__':
    cliente()
