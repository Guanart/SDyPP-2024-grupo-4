import numpy as np
import pika, cv2, threading, base64
from flask import Flask, json, request 

def dividir_imagen(imagen, num_filas, num_columnas, id):
    """
    Divide una imagen en partes más pequeñas y las encola en una cola RabbitMQ.

    Args:
        imagen (numpy.ndarray): La imagen a dividir.
        num_filas (int): El número de filas en las que se dividirá la imagen.
        num_columnas (int): El número de columnas en las que se dividirá la imagen.
        id (str): El identificador de la imagen.

    Returns:
        None
    """
    alto, ancho, _ = imagen.shape   # Obtener las dimensiones de la imagen
    alto_parte = alto // num_filas  # Obtener el alto de cada parte
    ancho_parte = ancho // num_columnas # Obtener el ancho de cada parte
    contador = 0    # Contador de partes
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
            mensaje = {'id': id, 'nro': contador, 'image_data': parte_base64}
            mensaje_json = json.dumps(mensaje)
            channel.basic_publish(exchange='', routing_key='imagenes', body=mensaje_json)
            print(f"Mensaje encolado: {mensaje}")
            
            # Incremento contador
            contador += 1
    connection.close()

app = Flask(__name__)

@app.route('/particionar', methods=['POST'])
def recibir_imagen():
    """
    Endpoint para recibir una imagen y dividirla en 4 partes.

    Returns:
        str: Un mensaje de éxito si la imagen se recibe correctamente.
        int: Código de estado HTTP 200 si es exitoso.
        str: Un mensaje de error si ocurre una excepción.
        int: Código de estado HTTP 500 si ocurre una excepción.
    """
    try:
        # Obtener la imagen del cuerpo de la solicitud
        imagen = request.files["imagen"]
        id = request.form["id"]

        """# Guardar la imagen -> se debería guardar en la carpeta /tmp cuando dockericemos
        with open("./imagen_" + id + "_particionador" + ".jpg", 'wb') as f:
            f.write(imagen.read())"""
        
        # Iniciar el proceso de división de la imagen en 4 partes en un hilo separado
        #archivo_imagen = cv2.imread("imagen_" + id + "_particionador" + ".jpg")
        
        img_np = np.frombuffer(imagen.read(), np.uint8)
        img_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        t = threading.Thread(target=dividir_imagen, kwargs={
                'imagen': img_cv2,
                'num_filas': 2,
                'num_columnas': 2,
                'id': id
            }
        )
        t.start()

        return "Imagen recibida", 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='imagenes')
    app.run(port=5001)
