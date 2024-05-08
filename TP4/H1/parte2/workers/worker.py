import pika, sys, os, json, base64

def main():
    # Conexión con RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Cola <imagenes>
    channel.queue_declare(queue='imagenes')

    # Callback que se ejecuta cuando recibe mensaje
    def callback(ch, method, properties, body):
        mensaje = json.loads(body)
        print(f"WORKER RECIBIÓ: {mensaje}")

        # Decodificar la imagen Base64 en datos binarios
        imagen_bytes = base64.b64decode(mensaje.get("image_data"))

        # Guardar imagen 
        with open(f"./{mensaje.get("id")}_{mensaje.get("nro")}.jpg", 'wb') as f:
            f.write(imagen_bytes)

    # Suscribirse a la cola <imagenes>
    channel.basic_consume(queue='imagenes',
                        auto_ack=True,
                        on_message_callback=callback)

    print('Esperando por mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)