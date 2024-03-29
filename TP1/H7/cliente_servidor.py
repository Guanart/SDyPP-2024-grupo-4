import json
import signal
import sys
import random
import asyncio

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.cliente = None
        self.server = None

    def setCliente(self, cliente):
        self.cliente = cliente
        self.cliente.setServidor(self)
    
    async def start(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"SERVIDOR: Servidor escuchando en {self.host}:{self.port}...")
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"SERVIDOR: Conexión establecida desde: {addr}")
        print()

        data = await reader.read(1024)

        if not data:
            writer.close()
            return

        received_data = json.loads(data.decode())

        if 'saludo' in received_data:
            response_data = {'respuesta': f"Hola desde el servidor {self.host}:{self.port}!"}
        else:
            response_data = {'error': 'Formato JSON inválido'}

        response_json = json.dumps(response_data)
        writer.write(response_json.encode())
        await writer.drain()
        writer.close()

    def stop(self):
        if self.server:
            self.server.close()

#-------------------------------------------------------------------

class Cliente:

    def __init__(self, servidor_contactos_ip: str, servidor_contactos_puerto: int):
        self.servidor_contactos_socket = (servidor_contactos_ip, servidor_contactos_puerto)

    def setServidor(self, servidor: Servidor):
        self.servidor = servidor

    async def registrarse(self):
        try:
            reader, writer = await asyncio.open_connection(*self.servidor_contactos_socket)
            message = {
                'registrar_inscripcion': {
                    'ip': self.servidor.host,
                    'port': self.servidor.port
                }
            }
            message_json = json.dumps(message)
            writer.write(message_json.encode())
            await writer.drain()

            data = await reader.read(1024)
            response = data.decode()
            print(f"CLIENTE: Respuesta del servidor de inscripciones: {response}")
            
            writer.close()
            await writer.wait_closed()
            
            # Cada 30 seg consulta las inscripciones:
            while True:
                await asyncio.sleep(30) 
                await self.consultar()

        except Exception as e:
            print("CLIENTE: Error al conectar con el servidor de inscripciones")
            print(e)

    async def consultar(self):
        try:
            reader, writer = await asyncio.open_connection(*self.servidor_contactos_socket)
            message = {
                'consultar_inscripcion': "inscriptos actuales"
            }
            message_json = json.dumps(message)
            writer.write(message_json.encode())
            await writer.drain()
            print("CLIENTE: Consultando los inscriptos")
            
            data = await reader.read(1024)
            response = data.decode()
            print()
            print(f"CLIENTE: Inscripciones actuales: {json.loads(response)["inscriptos"]}")
            

            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print("CLIENTE: Error al conectar con el servidor de inscripciones")
            print(e)

async def main():
    
    argumentos = sys.argv
    if len(argumentos) != 2:
        print("Uso: python cliente_servidor.py <servidor_contactos_ip:servidor_contactos_puerto>")
        sys.exit(1)
    argumentos = argumentos[1].split(":")
    
    server = Servidor('127.0.0.1', random.randint(1024, 65535))
    cliente = Cliente(argumentos[0], int(argumentos[1]))
    server.setCliente(cliente)

    server_task = asyncio.create_task(server.start())
    cliente_task = asyncio.create_task(cliente.registrarse())

    await asyncio.gather(server_task, cliente_task)

if __name__ == "__main__":
    asyncio.run(main())