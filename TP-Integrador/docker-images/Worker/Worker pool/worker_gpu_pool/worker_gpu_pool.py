import os
import pika
import requests
import minero_gpu
import json
import time
import threading
import random

id = -1

#Enviar el resultado al coordinador para verificar que el resultado es correcto
def post_result(data):
    url = "http://localhost:5002/solved_task"
    try:
        response = requests.post(url, json=data)
        print("Post response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send POST request:", e)

# #Minero: Encargado de realizar el desafio
def minero(ch, method, properties, body):
    data = json.loads(body)
    print(f"Message received")
    start_time = time.time()
    print("Starting mining process...")

    # En nuestra versión llega esto en data:
    '''
    data = {
        "id": last_id,
        "transactions": transactions, 
        "prefix": prefix,
        "num_min": 0,
        "num_max": 99999999,
        "last_hash": last_element["hash"] if last_element else ""
    }
    '''

    
    resultado = minero_gpu.ejecutar_minero(data["num_min"], data["num_max"], data["prefix"], str(len(data['transactions'])) + data["last_hash"])
    processing_time = time.time() - start_time
    #print(f"Resultado: {resultado}")
    if (resultado):
        resultado = json.loads(resultado)
        data["hash"] = resultado['hash_md5_result']
        data["number"] = resultado["numero"]
        post_result(data)
        print(f"Resultado encontrado y posteado para el block con ID {data['id']} en {processing_time:.2f} segundos")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else :
        print(f"No se encontró un Hash con ese máximo de números")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Le indico que no pude, y que no reencole

def send_keep_alive():
    global id
    url = "http://localhost:5002/alive"
    data = {
        "id": id,
        "type": "gpu"
    }
    while True:
        try:
            print("Enviando keep-alive...")
            response = requests.post(url, json=data)
            print("Respuesta del worker-pool:", response.text)
            time.sleep(7)
        except requests.exceptions.RequestException as e:
            print("Falló al hacer POST al worker-pool:", e)

#Conexion con rabbit al topico y comienza a ser consumidor
def main():
    global id
    data = {
        "id": id,
        "type": "gpu"
    }
    url = "http://localhost:5002/alive"
    registered_coordinator = False
    while not registered_coordinator:
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Connected to worker-pool")
                print(response.text)
                registered_coordinator = True
                id = response.json()["id"]
            else:
                print("Error to connect to worker-pool")
                print(response.status_code + response.text)
                time.sleep(3)
        except requests.exceptions.RequestException as e:
            print("Failed to send POST request:", e)
    threading.Thread(target=send_keep_alive, daemon=True).start()
    
    # Configuración de RabbitMQ
    rabbitmq_host = os.environ.get("POOL_RABBITMQ_HOST")
    rabbitmq_port = os.environ.get("POOL_RABBITMQ_PORT")
    connected_rabbit = False
    while not connected_rabbit:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=pika.PlainCredentials('guest', 'guest'), heartbeat=0))
            channel = connection.channel()
            channel.exchange_declare(exchange='blockchain_challenge', exchange_type='topic', durable=True)
            result = channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange='blockchain_challenge', queue=queue_name, routing_key=f'{id}')
            connected_rabbit = True
            print("Ya se encuentra conectado a RabbitMQ!")
        except Exception as e:
            print(f"Error connectando a RabbitMQ: {e}")
            print("Reintentando en 3 segundos...")
            time.sleep(3)

    channel.basic_consume(queue=queue_name, on_message_callback=minero, auto_ack=False)
    print('Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumption stopped by user.")
        connection.close()
        print("Connection closed.")

if __name__ == '__main__':
    main()