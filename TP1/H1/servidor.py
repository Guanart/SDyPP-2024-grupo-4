import asyncio
import json

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión establecida desde: {addr}")
    
    data = await reader.read(1024)
    if not data:
        writer.close()
        return
    
    received_data = json.loads(data.decode())
    print(received_data)

    if 'saludo' in received_data:
        response_data = {'mensaje_respuesta': "Hola, soy el servidor, recibí tu saludo"}
    else:
        response_data = {'error': 'Formato JSON inválido'}

    response_json = json.dumps(response_data)
    writer.write(response_json.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8000)
    print("Servidor escuchando en 127.0.0.1:8000 ...")
    async with server:
        await server.serve_forever()

asyncio.run(main())