import asyncio
import json

async def mandar_saludo():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8000)

        message = {'saludo': 'Hola'}
        message_json = json.dumps(message)
        writer.write(message_json.encode())
        await writer.drain()

        data = await reader.read(1024)
        response = data.decode()
        print(f'Respuesta del servidor: {response}')

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print("Error al conectar con el servidor")
        print(e)

asyncio.run(mandar_saludo())
