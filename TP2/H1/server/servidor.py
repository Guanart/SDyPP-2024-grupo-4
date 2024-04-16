from flask import Flask, jsonify, request
import docker
import requests
import time

app = Flask(__name__)
client_docker = docker.from_env()

@app.route("/getRemoteTask", methods=['GET', 'POST'])
def ejecutarTareaRemota():
    task_params = request.get_json()
    print(task_params)
    id_container = client_docker.containers.run(task_params['image'], detach=True, ports={'8000/tcp': 8000})
    container = client_docker.containers.get(id_container.id)
    response = requests.post('http://localhost:8000/ejecutarTarea', json=task_params)
    container.stop()
    container.remove()
    return response.json()
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
