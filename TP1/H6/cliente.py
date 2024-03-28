import socket
import json

def send_greetings_to_servers(servers, greeting):
    for server_address in servers:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(server_address)
            message = {'saludo': greeting}
            message_json = json.dumps(message)
            client_socket.sendall(message_json.encode())
            response = client_socket.recv(1024)
            print(f"Respuesta del servidor {server_address}: {response.decode()}")
            client_socket.close()
        except Exception as e:
            print(f"Error al conectar con el servidor {server_address}: {e}")

if __name__ == "__main__":
    # Lista de servidores a los que se enviará el saludo
    servers_list = [('127.0.0.1', 8000), ('127.0.0.1', 8001)]  # Agrega más servidores si es necesario

    # Saludo que se enviará a los servidores
    greeting = "¡Hola desde el cliente!"

    send_greetings_to_servers(servers_list, greeting)