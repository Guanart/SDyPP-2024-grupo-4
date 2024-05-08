import pika, sys, os, json, base64, redis

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

        # Obtener datos:
        id = mensaje.get("id") # Str
        nro_parte = mensaje.get("nro") # Int

        # Decodificar la imagen Base64 en datos binarios
        imagen_bytes = base64.b64decode(mensaje.get("image_data"))

        # Guardar imagen
        with open(f"./{mensaje.get("id")}_{mensaje.get("nro")}.jpg", 'wb') as f:
            f.write(imagen_bytes)

        # Guardar en redis: {clave: id+_nro, valor: imagen_bytes}
        clave = id + "_" + str(nro_parte)
        r.set(clave, imagen_bytes)

    # Suscribirse a la cola <imagenes>
    channel.basic_consume(queue='imagenes',
                        auto_ack=True,
                        on_message_callback=callback)

    print('Esperando por mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


# Levantar Redis en docker:
# docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

# Levantar RabbitMQ en docker:
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

""" Conectarse de forma segura a Redis:
r = redis.Redis(
    host="my-redis.cloud.redislabs.com", port=6379,
    username="default", # use your Redis user. More info https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/
    password="secret", # use your Redis password
    ssl=True,
    ssl_certfile="./redis_user.crt",
    ssl_keyfile="./redis_user_private.key",
    ssl_ca_certs="./redis_ca.pem",
)
"""