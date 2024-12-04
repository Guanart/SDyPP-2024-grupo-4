import sys
import numpy as np
import pika, cv2, threading, base64, time, redis
from flask import Flask, json, request 

def dividir_encolar(imagen, num_filas, num_columnas, id):
    # Guardo en Redis cuantas partes se necesitan de esta imagen (para el unificador)
    clave = id + "_filas"
    r.set(clave, num_filas)
    clave = id + "_columnas"
    r.set(clave, num_columnas)

    alto, ancho, _ = imagen.shape   # Obtener las dimensiones de la imagen
    alto_parte = alto // num_filas  # Obtener el alto de cada parte
    ancho_parte = ancho // num_columnas # Obtener el ancho de cada parte
    contador = 1    # Contador de partes
    # Iterar sobre cada parte de la imagen
    for fila in range(num_filas):
        for columna in range(num_columnas):
            # Calcular las coordenadas de inicio y fin de la parte
            inicio_y = fila * alto_parte
            fin_y = inicio_y + alto_parte
            inicio_x = columna * ancho_parte
            fin_x = inicio_x + ancho_parte

            # Recortar la parte de la imagen
            parte = imagen[inicio_y:fin_y, inicio_x:fin_x]

            # Codificar la parte de la imagen en memoria como JPG y luego Base64
            _, parte_encoded = cv2.imencode('.jpg', parte)
            parte_base64 = base64.b64encode(parte_encoded).decode('utf-8')

            # Se encola el mensaje a la cola "imagenes" de RabbitMQ
            nro = str(contador)
            mensaje = {"id": id, "nro": nro, "imagen_data": parte_base64}
            mensaje_json = json.dumps(mensaje)
            channel.basic_publish(exchange='', routing_key='imagenes', body=mensaje_json)
            print(f"Mensaje encolado: {id}_{contador}")
            
            # Incremento contador
            contador += 1

app = Flask(__name__)

@app.route('/particionar', methods=['POST'])
def recibir_imagen():
    imagen = request.files["imagen"]
    filas = int(request.form["filas"])
    columnas = int(request.form["columnas"])
    id = request.form["id"]

    img_np = np.frombuffer(imagen.read(), np.uint8)
    img_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    t = threading.Thread(target=dividir_encolar, kwargs={
            'imagen': img_cv2,
            'num_filas': filas,
            'num_columnas': columnas,
            'id': id
        })
    t.start()

    return "Imagen recibida", 200

if __name__ == '__main__':
    try:
        r = redis.Redis(host='redis', port=6379, decode_responses=True)
        print("Conectado a Redis")
    except Exception as e:
        print(f"No se pudo conectar a Redis: {e}")
        sys.exit(1) 
    connected = False
    while not connected:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=0))
            channel = connection.channel()
            channel.confirm_delivery()
            channel.queue_declare(queue='imagenes')
            connected = True
            print("Conectado a RabbitMQ!")
        except Exception as e:
            print(f"Error connectando a RabbitMQ: {e}")
            print("Reintentando en 5 segundos...")
            time.sleep(5)
    app.run(host='0.0.0.0', port=5001)