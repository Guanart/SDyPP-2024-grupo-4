# SDyPP-2024-grupo-4
## HIT 5

El cliente_servidor recibe por argumentos la IP y el puerto en el que debe escuchar el servidor, y la IP y el puerto del servidor al que se debe conectar.

Los mensajes se envían en formato JSON, se serializa al enviar y se deserializa al recibir. 

La máquina virtual de Google ejecuta el comando: ```docker compose up```, ejecutando el archivo ```docker-compose.yml``` de esta carpeta. De esta manera ambos contenedores se encuentran en la misma red, por lo que los dos cliente_servidor se pueden comunicar.


