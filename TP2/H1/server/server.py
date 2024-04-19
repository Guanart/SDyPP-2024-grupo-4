from flask import Flask, request
import docker
import requests
import time

app = Flask(__name__)


@app.route("/getRemoteTask", methods=['GET', 'POST'])
def ejecutarTareaRemota():
    client_docker = docker.from_env()
    task_params = request.get_json()
    print(task_params)
    id_container = client_docker.containers.run(task_params['image'], detach=True, ports={'5000/tcp': 8022})
    container = client_docker.containers.get(id_container.id)

    time.sleep(3)
    while not container.status == 'running':
        print("Esperando a que el contenedor esté en ejecución...")
        time.sleep(3)  # Esperar 3 segundos antes de volver a verificar

    response = requests.post('http://host.docker.internal:8022/ejecutarTarea', json=task_params)
    container.stop()
    container.remove()
    return response.json()
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")

