import numpy as np
import pika, sys, os, json, base64, cv2, time
import redis

def main():
    # Callback que se ejecuta cuando recibe mensaje
    def callback(ch, method, properties, body):
        try:
            mensaje = json.loads(body)

            # Obtener datos:
            id = mensaje.get("id")
            nro_parte = mensaje.get("nro")
            print(f"Mensaje consumido: {id}_{nro_parte}")

            # Decodificar la imagen Base64 en datos binarios
            imagen_bytes = base64.b64decode(mensaje.get("imagen_data"))

            # Obtengo el formato de imagen de OpenCV en base a los bytes de la imagen (para poder operar el Sobel)
            imagen_opencv = cv2.imdecode(np.frombuffer(imagen_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

            # SOBEL:
            gray = cv2.cvtColor(imagen_opencv, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel_combined = cv2.magnitude(sobelx, sobely)
            parte_sobel = np.uint8(255 * sobel_combined / np.max(sobel_combined))

            # Obtener los bytes de la parte sobel
            _, parte_sobel_encoded = cv2.imencode('.jpg', parte_sobel)
            parte_sobel_bytes = parte_sobel_encoded.tobytes()

            # Guardar en redis: {clave: id+nro_parte, valor: imagen_bytes}
            clave = id + "_" + str(nro_parte)
            r.set(clave, parte_sobel_bytes)
            print(f"Parte guardada en redis: {clave}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error procesando mensaje:", e)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    # Suscribirse a la cola <imagenes>
    channel.basic_consume(queue='imagenes',
                        auto_ack=False,
                        on_message_callback=callback)

    print('Esperando por mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    connected = False
    while not connected:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='imagenes')
            connected = True
        except Exception as e:
            print(f"Error connectando a RabbitMQ: {e}")
            print("Reintentando en 5 segundos...")
            time.sleep(5)
    try:
        r = redis.Redis(host='redis', port=6379, decode_responses=True)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as e:
        print(str(e))