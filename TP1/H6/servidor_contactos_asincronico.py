import asyncio
import json
import signal


class ServidorContactos:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.contactos = []
        self.server = None

    def setCliente(self, cliente):
        self.cliente = cliente
        self.cliente.setServidor(self)

    async def start(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Servidor de contactos escuchando en {self.host}:{self.port}...")
        async with self.server:
            await self.server.serve_forever()


    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Conexión establecida desde: {addr}")

        data = await reader.read(1024)
        if not data:
            writer.close()
            return

        received_data = json.loads(data.decode())

        if 'registrar' in received_data:
            response_data = {'message': "El nodo se registro como contacto correctamente"}
            self.contactos.append(received_data["registrar"])
            self.cliente.setContactos(self.contactos)
            await self.cliente.enviar_contactos()
        else:
            response_data = {'error': 'Formato JSON invalido'}

        response_json = json.dumps(response_data)
        writer.write(response_json.encode())
        #writer.drain()
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    def stop(self):
        if self.server:
            self.server.close()

class ClienteContactos:
    def __init__(self):
        self.contactos = []

    def setServidor(self, servidor: ServidorContactos):
        self.servidor = servidor

    def setContactos(self, contactos: list):
        self.contactos = contactos

    async def enviar_contactos(self):
        print(self.contactos)
        for contacto in self.contactos:
            try:
                reader, writer = await asyncio.open_connection(contacto["ip"], contacto["port"])

                message = {'contactos': self.contactos}
                message_json = json.dumps(message)
                writer.write(message_json.encode())
                await writer.drain()
                
                data = await reader.read(1024)
                response = data.decode()
                print(f"Respuesta: {response}")
                
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(e)

async def main():
    server = ServidorContactos('127.0.0.1', 8000)
    cliente = ClienteContactos()
    server.setCliente(cliente)
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())