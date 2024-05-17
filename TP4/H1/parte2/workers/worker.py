import numpy as np
import pika, sys, os, json, base64, cv2, time
from redis import Redis

def main():
    """
    Función principal que se conecta a RabbitMQ, declara una cola y consume mensajes de la cola.

    Esta función establece una conexión con RabbitMQ, declara una cola llamada 'imagenes' y configura una función de
    devolución de llamada para manejar los mensajes entrantes. La función de callback recibe un mensaje,
    extrae los datos relevantes, decodifica una imagen en formato Base64, guarda la imagen en disco y la almacena en Redis.

    La función comienza a consumir mensajes de la cola 'imagenes' y espera mensajes indefinidamente hasta que se interrumpa
    presionando CTRL+C.
    """
    # Conexión con RabbitMQ
    time.sleep(10)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Cola <imagenes>
    channel.queue_declare(queue='imagenes')

    # Callback que se ejecuta cuando recibe mensaje
    def callback(ch, method, properties, body):
        mensaje = json.loads(body)
        print(f"WORKER RECIBIÓ: {mensaje}")

        # Obtener datos:
        id: str = mensaje.get("id")
        nro_parte: int = mensaje.get("nro")

        # Decodificar la imagen Base64 en datos binarios
        imagen_bytes = base64.b64decode(mensaje.get("image_data"))


        # APLICAR SOBEL:
        # Obtengo el formato de imagen de OpenCV en base a los bytes de la imagen (para poder operar el Sobel)
        imagen_opencv = cv2.imdecode(np.frombuffer(imagen_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(imagen_opencv, cv2.COLOR_BGR2GRAY)

        # Aplicar el filtro Sobel
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # Combinar los resultados de los filtros Sobel
        sobel_combined = cv2.magnitude(sobelx, sobely)

        # Normalizar los valores entre 0 y 255
        parte_sobel = np.uint8(255 * sobel_combined / np.max(sobel_combined))

        # Guardar imagen (con formato de OpenCV)
        # cv2.imwrite("parte" + str(nro_parte) + "_sobel.jpg", parte_sobel)

        # Guardar imagen
        """with open(f"./{mensaje.get('id')}_{mensaje.get('nro')}.jpg", 'wb') as f:
            f.write(imagen_bytes)"""
        
        # Obtener los bytes de la parte sobel
        _, parte_sobel_encoded = cv2.imencode('.jpg', parte_sobel)
        parte_sobel_bytes = parte_sobel_encoded.tobytes()


        # Guardar en redis: {clave: id+nro_parte, valor: imagen_bytes}
        clave = id + "_" + str(nro_parte)
        #redis.set(clave, imagen_bytes)     # Guardo la parte normal en Redis
        redis.set(clave, parte_sobel_bytes)   # Guardo la parte de sobel en Redis
        print(f"WORKER GUARDÓ EN REDIS: {clave}")

    # Suscribirse a la cola <imagenes>
    channel.basic_consume(queue='imagenes',
                        auto_ack=True,
                        on_message_callback=callback)

    print('Esperando por mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        redis = Redis(host='redis', port=6379, decode_responses=True)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)