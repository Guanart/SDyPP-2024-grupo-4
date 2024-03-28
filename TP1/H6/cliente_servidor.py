import socket
import json
import signal
import sys

class servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Cierra el servidor con "CTRL+C"
    def shutdown(self, signum, frame):
        print("Apagando el servidor...")
        self.server_socket.close()
        sys.exit(0)

    def start(self):
        # Enlaza el socket a la dirección y puerto especificados
        self.server_socket.bind((self.host, self.port))

        # Escucha por conexiones entrantes
        self.server_socket.listen(1)
        print(f"Servidor escuchando en {self.host}:{self.port}...")

        # Asigna el método shutdown para manejar la señal SIGINT
        signal.signal(signal.SIGINT, self.shutdown)
        while True:
            # Acepta una conexión entrante
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde: {addr}")

            # Recibe datos del cliente
            data = client_socket.recv(1024)

            if not data:
                break

            # Decodifica los datos JSON recibidos
            received_data = json.loads(data.decode())

            # Procesa el saludo recibido y prepara la respuesta
            if 'saludo' in received_data:
                response_data = {'respuesta': "Hola desde el servidor!"}
            else:
                response_data = {'error': 'Formato JSON inválido'}

            # Convierte la respuesta a formato JSON
            response_json = json.dumps(response_data)

            # Envía la respuesta al cliente
            client_socket.sendall(response_json.encode())

            # Cierra la conexión con el cliente
            client_socket.close()

    def stop(self):
        # Cierra el socket del servidor
        self.server_socket.close()

if __name__ == "__main__":
    server = servidor('127.0.0.1', 8000)
    try:
        server.start()
    finally:
        server.stop()