import socket
import json
import signal
import sys

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setCliente(self, cliente):
        self.cliente = cliente
        self.cliente.setServidor(self)
        
    # Cierra el servidor con "CTRL+C"
    def shutdown(self, signum, frame):
        print("Apagando el servidor...")
        self.server_socket.close()
        sys.exit(0)

    def start(self):
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

            received_data = json.loads(data.decode())

            if 'saludo' in received_data:
                response_data = {'respuesta': f"Hola desde el servidor {self.host}:{self.port}!"}
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
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(server_address)
                message = {'saludo': f"Hola, soy el nodo {self.servidor.host}:{self.servidor.port}!"}
                message_json = json.dumps(message)
                client_socket.sendall(message_json.encode())
                response = client_socket.recv(1024)
                print(f"Respuesta del servidor {server_address}: {response.decode()}")
                client_socket.close()
            except Exception as e:
                print(f"Error al conectar con el servidor {server_address}: {e}")

    def registrarse(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(self.servidor_contactos_socket)
            message = {
                'registrar': {
                    'ip': self.servidor.host,
                    'puerto': self.servidor.port
                }
            }
            message_json = json.dumps(message)
            client_socket.sendall(message_json.encode())
            response = client_socket.recv(1024)
            print(f"Respuesta del servidor de contactos: {response.decode()}")
            client_socket.close()
        except Exception as e:
            print("Error al conectar con el servidor de contactos")

if __name__ == "__main__":

    # argumentos = sys.argv
    # if len(argumentos) != 3:
    #     print("Uso: python cliente_servidor.py <servidor_contactos_ip:servidor_contactos_puerto>")
    #     sys.exit(1)
    
    # argumentos = argumentos.split(":")

    # try:
    #     int(argumentos[1])
    # except:
    #     print("Uso: python cliente_servidor.py <servidor_contactos_ip:servidor_contactos_puerto>")
    #     print("- servidor_contactos_puerto debe ser un numero entero")

    server = Servidor('127.0.0.1', 8000)
    # cliente = Cliente(argumentos[0],int(argumentos[1]))
    cliente = Cliente("127.0.0.1", 8001)
    server.setCliente(cliente)
    cliente.registrarse()
    try:
        server.start()
    finally:
        server.stop()
