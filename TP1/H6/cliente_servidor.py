import socket
import json
import sys
import random
import threading
import logging

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setCliente(self, cliente):
        self.cliente = cliente
        self.cliente.setServidor(self)
        
    def start(self):
        self.server_socket.bind(("", self.port))
        self    .server_socket.listen(1)
        print(f"Servidor escuchando en {self.host}:{self.port}...")
        logging.info(f"Servidor escuchando en {self.host}:{self.port}...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde: {addr}")
            logging.info(f"Conexión establecida desde: {addr}")

            # Recibe datos del cliente
            data = client_socket.recv(1024)

            if not data:
                break

            received_data = json.loads(data.decode())

            if 'saludo' in received_data:
                response_data = {'respuesta': f"Hola desde el servidor {self.host}:{self.port}!"}
            elif 'contactos' in received_data:
                response_data = {'confirmacion': "Contactos recibidos"}
                logging.info(f"Contactos recibidos: {received_data["contactos"]}")
                t_mandar_saludo = threading.Thread(target=self.cliente.mandar_saludo, args=(received_data["contactos"],))
                t_mandar_saludo.start()
                # t_mandar_saludo.join()
            else:
                response_data = {'error': 'Formato JSON inválido'}

            response_json = json.dumps(response_data)
            client_socket.sendall(response_json.encode())
            client_socket.close()

    def stop(self):
        self.server_socket.close()

class Cliente:
    def __init__(self, servidor_contactos_ip: str, servidor_contactos_puerto: int):
        self.servidor_contactos_socket = (servidor_contactos_ip, servidor_contactos_puerto)

    def setServidor(self, servidor: Servidor):
        self.servidor = servidor

    def mandar_saludo(self, servers):
        for server_address in servers:
            if (server_address["ip"]==self.servidor.host and server_address["port"]==self.servidor.port):
                # Esto no anda, la idea es que el nodo conozca su propia IP en la red, y no se autoenvíe un mensaje (la IP de la interfaz docker)
                continue
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tupla_conexion=(server_address["ip"], server_address["port"])
                logging.info(f"Enviando saludo a {tupla_conexion}...")
                client_socket.connect(tupla_conexion)
                message = {'saludo': f"Hola, soy el nodo {self.servidor.host}:{self.servidor.port}!"}
                message_json = json.dumps(message)
                client_socket.sendall(message_json.encode())
                response = client_socket.recv(1024)
                print(f"Respuesta del servidor {server_address}: {response.decode()}")
                logging.info(f"Respuesta del servidor {server_address}: {response.decode()}")
                client_socket.close()
            except Exception as e:
                print(f"Error al conectar con el servidor {server_address}: {e}")
                logging.error(f"Error al conectar con el servidor {server_address}: {e}")

    def registrarse(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(self.servidor_contactos_socket)
            message = {
                'registrar': {
                    'port': self.servidor.port
                }
            }
            message_json = json.dumps(message)
            client_socket.sendall(message_json.encode())
            response = client_socket.recv(1024)
            print(f"Respuesta del servidor de contactos: {response.decode()}")
            logging.info(f"Respuesta del servidor de contactos: {response.decode()}")
            client_socket.close()
        except Exception as e:
            print("Error al conectar con el servidor de contactos")
            logging.info("Error al conectar con el servidor de contactos")
            print(e)
            logging.error(e)

if __name__ == "__main__":
    logging.basicConfig(filename='cliente_servidor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    argumentos = sys.argv
    if len(argumentos) != 2:
        print("Uso: python cliente_servidor.py <servidor_contactos_ip:servidor_contactos_puerto>")
        logging.info("Uso: python cliente_servidor.py <servidor_contactos_ip:servidor_contactos_puerto>")
        sys.exit(1)
    
    argumentos = argumentos[1].split(":")

    server = Servidor('0.0.0.0', random.randint(1024,65535))
    cliente = Cliente(argumentos[0],int(argumentos[1]))
    server.setCliente(cliente)
    try:
        logging.info("--------------------------------------------------------------------------------\n")
        # Crear hilos para ejecutar el servidor y el cliente en paralelo
        t_servidor = threading.Thread(target=server.start)
        t_cliente = threading.Thread(target=cliente.registrarse)
        # Iniciar los hilos
        t_servidor.start()
        t_cliente.start()
        t_servidor.join()
        t_cliente.join()
    finally:
        server.stop()
