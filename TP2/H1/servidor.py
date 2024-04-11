from flask import Flask, jsonify, request
import docker
import requests
import time

app = Flask(__name__)
client_docker = docker.from_env()

"""
Hit #1
Implemente un servidor que resuelva “tareas genéricas” o “pre-compiladas”. 
Para ello, hay un conjunto de acciones de diseño y arquitectura que deben respetarse:


SERVIDOR:
Desarrollar el servidor utilizando tecnología HTTP.
El servidor debe ser contenerizado y alojado en un host con Docker instalado.
Permanecerá receptivo a nuevas solicitudes del cliente, exponiendo métodos para interactuar.
Debe incluir un método llamado ejecutarTareaRemota() asociado a un endpoint (getRemoteTask()) 
para procesar tareas genéricas enviadas por el cliente.
Los parámetros de las tareas serán recibidos a través de solicitudes HTTP GET/POST, 
utilizando una estructura JSON.
Durante la ejecución, el servidor levantará temporalmente un "servicio tarea" como un contenedor
Docker.
Una vez en funcionamiento, se comunicará con el "servicio tarea" para ejecutar la tarea con los
parámetros proporcionados.
Esperará los resultados de la tarea y los enviará de vuelta al cliente.


SERVICIO TAREA:
Establecer un servicio de escucha utilizando un servidor web.
Implementar la tarea de procesamiento denominada ejecutarTarea().
Configurar el servicio para recibir los parámetros de entrada en formato JSON.
Empaquetar la solución como una imagen Docker para facilitar la distribución y el despliegue.
Publicar la solución en el registro de Docker Hub, ya sea público o privado, para que esté 
disponible para su uso y colaboración.


CLIENTE:
Utilizar una solicitud HTTP GET/POST para comunicarse con el servidor.
Enviar los parámetros necesarios para la tarea en formato JSON, incluyendo:
El cálculo a realizar.
Los parámetros específicos requeridos para la tarea.
Datos adicionales necesarios para el procesamiento.
La imagen Docker que contiene la solución de la tarea.
Credenciales de usuario y contraseña encriptadas en caso de que se trate de un registro 
privado en Docker Hub.
"""



"""
Tiene una operacion y los números que recibe, y concatena
Ejemplo:
suma: 3 + 4 + 1 = 8
resta 3 - 4 - 1 = -2

formato JSON tarea:
{
    operacion: suma
    argumentos: {
        3,
        4, 
        1
    }
}

respuesta:
{
    resultado: 8  --> (3 + 4 + 1)
}
"""

"""
ok
"""

@app.route("/getRemoteTask", methods=['GET', 'POST'])
def ejecutarTareaRemota():
    task_params = request.get_json()
    print(task_params)
    id_container = client_docker.containers.run("grupo4sdypp2024/tp2-task1", detach=True, ports={'8000/tcp': 8000})
    # container = client_docker.containers.get(id_container.id)
    # container.reload()
    # print(container.ports)
    time.sleep(10)
    response = requests.post('http://localhost:8000/ejecutarTarea', json=task_params)
    # container.stop()
    return response.json()
    
if __name__ == '__main__':
    app.run()