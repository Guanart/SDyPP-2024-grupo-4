# SDyPP-2024-grupo-4
## HIT 6

El servidor_contactos corre en un container Docker, y el cliente_servidor en otro.
Los cliente_servidor reciben por argumentos la IP y el puerto donde escucha el servidor_contactos, además, inician la escucha en un puerto aleatorio.

Los cliente_servidor se conectan al servidor_contactos y le indican en que puerto e IP están escuchando.  Cada vez que el servidor_contactos recibe un nuevo contacto, lo agrega a su lista, y a todos los contactos registrados les notifica la nueva lista.

Los mensajes se envían en formato JSON, se serializa al enviar y se deserializa al recibir. 

Ya que el ejercicio se encuentra hecho en una red de Docker, se necesita probar de forma local, las instrucciones son las siguientes:

1. Ejecutar ```docker build -t grupo4sdypp2024/tp1-h6-servidor_contactos -f servidor_contactos.dockerfile .``` y ```docker build -t grupo4sdypp2024/tp1-h6-cliente_servidor -f cliente_servidor.``` para crear las imágenes, o descargarlas de Docker Hub mediante los comandos ```docker pull grupo4sdypp2024/tp1-h6-servidor_contactos``` y ```docker pull grupo4sdypp2024/tp1-h6-cliente_servidor```.
2. Ejecutar ```docker compose up```, de esta manera docker ejecuta el archivo ```docker-compose.yml```, en este se generan tres cliente-servidor y un servidor de contactos.
