import socket
import json
import logging

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
        logging.info(f"Servidor de contactos escuchando en {self.host}:{self.port}...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde: {addr}")
            logging.info(f"Conexión establecida desde: {addr}")
            data = client_socket.recv(1024)

            if not data:
                break

            received_data = json.loads(data.decode())

            if 'registrar' in received_data:
                self.contactos.append({"ip": addr[0], "port": received_data["registrar"]["port"]})
                self.cliente.setContactos(self.contactos)
                response_data = {'message': "El nodo se registro como contacto correctamente"}
            else:
                response_data = {'error': 'Formato JSON invalido'}

            response_json = json.dumps(response_data)
            client_socket.sendall(response_json.encode())
            client_socket.close()

            if 'registrar' in received_data:
                self.cliente.enviar_contactos()

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
        logging.info(self.contactos)
        for contacto in self.contactos:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                contacto_tupla = (contacto["ip"], contacto["port"])
                logging.info(f"Enviando lista de contactos a {contacto_tupla}...")
                client_socket.connect(contacto_tupla)
                message = self.contactos
                message_json = json.dumps({'contactos' : message})
                client_socket.sendall(message_json.encode())
                response = client_socket.recv(1024)
                print(f"Respuesta: {response.decode()}")
                logging.info(f"Respuesta: {response.decode()}")
                client_socket.close()
            except Exception as e:
                print(e)
                logging.error(e)

if __name__ == "__main__":
    logging.info("\n--------------------------------------------------------------------------------")
    logging.basicConfig(filename='servidor_contactos.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    server = ServidorContactos('0.0.0.0', 8000)
    cliente = ClienteContactos()
    server.setCliente(cliente)
    try:
        server.start()
    finally:
        server.stop()
