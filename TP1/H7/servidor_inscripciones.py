#!/usr/bin/python3
import asyncio
import json
import time
import sys
import logging

class ServidorContactos:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.ventana_siguiente = []
        self.ventana_actual = []

    def setCliente(self, cliente):
        self.cliente = cliente
        self.cliente.setServidor(self)

    async def start(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Servidor de inscripciones escuchando en {self.host}:{self.port}...")
        logging.info(f"Servidor de inscripciones escuchando en {self.host}:{self.port}...")
        async with self.server:
            await self.start_window_timer()  

    async def start_window_timer(self):
        while True:
            current_second = time.localtime().tm_sec
            if current_second == 0:
                # Cada inicio de minuto, se mueven las inscripciones futuras a la ventana actual
                await self.registrar_json(self.ventana_siguiente) # Se agrega al histórico
                self.ventana_actual = self.ventana_siguiente
                self.ventana_siguiente = []
                print("Inició un nuevo minuto")
                logging.info("Inició un nuevo minuto")
                print(f"Ventana actual: {self.ventana_actual} ")
                logging.info(f"Ventana actual: {self.ventana_actual} ")
                print("------------------------------------------------")
                logging.info("------------------------------------------------")
                print("Se ha iniciado una nueva ventana de inscripciones.")
                logging.info("Se ha iniciado una nueva ventana de inscripciones.")
            await asyncio.sleep(1)  # Espera un segundo antes de revisar nuevamente

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Conexión establecida desde: {addr}")
        logging.info(f"Conexión establecida desde: {addr}")

        # Lee el buffer
        data = await reader.read(1024)
        if not data:
            writer.close()
            return

        received_data = json.loads(data.decode())

        if 'registrar_inscripcion' in received_data:
            response_data = {'Inscripcion': "Has sido inscripto para la siguiente ventana"}
            if any(item == received_data["registrar_inscripcion"] for item in self.ventana_siguiente):
                writer.close()
                return
            # agregar la inscripcion al registro de la ventana siguiente
            self.ventana_siguiente.append({"ip": addr[0], "port": received_data["registrar_inscripcion"]["port"]})
        elif "consultar_inscripcion" in received_data:
            # responder con el registro de la ventana actual
            response_data = {"inscriptos": self.ventana_actual }
        else:
            response_data = {'error': 'Formato JSON invalido'}

        response_json = json.dumps(response_data)
        writer.write(response_json.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    def stop(self):
        if self.server:
            self.server.close()

    async def registrar_json(self,ventana: list):
        if len(ventana)==0:
            return

        objetos_existentes = None
        try:
            with open("inscripciones.json", 'r') as archivo:
                objetos_existentes = json.load(archivo)
        except FileNotFoundError:
            logging.error("Archivo inscripciones.json no encontrado")
        except Exception as e:
            logging.error(e)

        if objetos_existentes is None:
            logging.info("El archivo está vacío. Creando inscripciones.json")
            objetos_existentes = []

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("inscripciones.json", 'w') as archivo:
            objetos_existentes.append({current_time : ventana})
            json.dump(objetos_existentes, archivo)

async def main():
    server = ServidorContactos('0.0.0.0', 8000)
    await server.start()

if __name__ == "__main__":
    logging.basicConfig(filename='servidor_inscripciones.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("\n--------------------------------------------------------------------------------")
    asyncio.run(main())