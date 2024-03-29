import socket
import json
import signal
import sys

class ServidorContactos:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.contactos = []

    def setCliente(self, cliente):
        self.cliente = cliente
        self.cliente.setServidor(self)
        
    def start(self):
        self.server_socket.bind(("", self.port))
        self.server_socket.listen(1)
        print(f"Servidor de contactos escuchando en {self.host}:{self.port}...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde: {addr}")
            data = client_socket.recv(1024)

            if not data:
                break

            received_data = json.loads(data.decode())

            if 'registrar' in received_data:
                response_data = {'message': "El nodo se registro como contacto correctamente"}
                self.contactos.append(received_data["registrar"])
                self.cliente.setContactos(self.contactos)
                self.cliente.enviar_contactos()
            else:
                
                response_data = {'error': 'Formato JSON invalido'}

            response_json = json.dumps(response_data)
            client_socket.sendall(response_json.encode())
            client_socket.close()

    def stop(self):
        self.server_socket.close()

class ClienteContactos:
    def __init__(self):
        self.contactos = []

    def setServidor(self, servidor: ServidorContactos):
        self.servidor = servidor

    def setContactos(self, contactos: list):
        self.contactos = contactos

    def enviar_contactos(self):
        print(self.contactos)
        for contacto in self.contactos:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                contacto_tupla = (contacto["ip"], contacto["port"])
                client_socket.connect(contacto_tupla)
                message = self.contactos
                message_json = json.dumps({'contactos' : message})
                client_socket.sendall(message_json.encode())
                response = client_socket.recv(1024)
                print(f"Respuesta: {response.decode()}")
                client_socket.close()
            except Exception as e:
                print(e) #Este es

# Cierra el servidor con "CTRL+C"
def handler(num, frame):
    print("Se ha desconectado el nodo")
    server.stop()
    #sys.exit(0)
    return default_handler(num, frame)


if __name__ == "__main__":
    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, handler)

    server = ServidorContactos('127.0.0.1', 8000)
    cliente = ClienteContactos()
    server.setCliente(cliente)
    try:
        server.start()
    finally:
        server.stop()
