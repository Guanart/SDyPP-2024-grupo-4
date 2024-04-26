# SDyPP-2024-grupo-4
## HIT 6

El servidor_contactos corre en un container Docker, y el cliente_servidor en otro.
Los cliente_servidor reciben por argumentos la IP y el puerto donde escucha el servidor_contactos, además, inician la escucha en un puerto aleatorio.

Los cliente_servidor se conectan al servidor_contactos y le indican en que puerto e IP están escuchando.  Cada vez que el servidor_contactos recibe un nuevo contacto, lo agrega a su lista, y a todos los contactos registrados les notifica la nueva lista.

Los mensajes se envían en formato JSON, se serializa al enviar y se deserializa al recibir. 

La máquina virtual de Google ejecuta el comando: ```docker compose up```, ejecutando el archivo ```docker-compose.yml``` de esta carpeta. De esta manera todos los contenedores se encuentran en la misma red, por lo que los cliente_servidor se pueden comunicar hacia el servidor_contactos.

Para ver el flujo del programa, acceda a los logs de los containers con el comando ```sudo docker logs <id_container_h6>```
