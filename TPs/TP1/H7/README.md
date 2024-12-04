# SDyPP-2024-grupo-4
## HIT 7

El servidor_inscripciones corre en un container Docker, y el cliente_servidor en otro.
Los cliente_servidor reciben por argumentos la IP y el puerto donde escucha el servidor_inscripciones, además, inician la escucha en un puerto aleatorio.

Al ejecutarse, el módulo de cliente de los cliente_servidor se conectan al servidor_inscripciones y le indican en que puerto e IP están escuchando (se registran). Además, cada 30 segundos realizan una consulta hacia el servidor, para conocer las inscripciones de la ventana actual.

El servidor_inscripciones tiene una ventana de tiempo fija de un minuto, cada vez que se cumple un minuto, los registros que le llegaron los pasa a la "ventana actual", y las incripciones que se hagan en el nuevo minuto, quedarán en la "ventana siguiente". Además, en el archivo inscripciones.json se mantiene el registro histórico de todas las incripciones.

Los mensajes se envían en formato JSON, se serializa al enviar y se deserializa al recibir. 

Ya que el ejercicio se encuentra hecho en una red de Docker, se necesita probar de forma local, las instrucciones son las siguientes:

1. Ejecutar ```docker build -t grupo4sdypp2024/tp1-h7-servidor_inscripciones -f servidor_inscripciones.dockerfile.``` y ```docker build -t grupo4sdypp2024/tp1-h7-cliente_servidor -f cliente_servidor.dockerfile .``` para crear las imágenes, o descargarlas de Docker Hub mediante los comandos ```docker pull grupo4sdypp2024/tp1-h7-servidor_inscripciones``` y ```docker pull grupo4sdypp2024/tp1-h7-cliente_servidor```.
2. Ejecutar ```docker compose up```, de esta manera docker ejecuta el archivo ```docker-compose.yml```, en este se generan dos cliente-servidor y un servidor de inscripciones. Al momento de la ejecución, los clientes se van a registrar, y el servidor de inscripciones los va a registrar, luego los clientes van a poder conocer cuales fueron los incriptos (cuando haya pasado a una nueva ventana).
