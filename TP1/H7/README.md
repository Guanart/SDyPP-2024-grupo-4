# SDyPP-2024-grupo-4
## HIT 6

El servidor_inscripciones corre en un container Docker, y el cliente_servidor en otro.
Los cliente_servidor reciben por argumentos la IP y el puerto donde escucha el servidor_inscripciones, además, inician la escucha en un puerto aleatorio.

Al ejecutarse, el módulo de cliente de los cliente_servidor se conectan al servidor_inscripciones y le indican en que puerto e IP están escuchando (se registran). Además, cada 30 segundos realizan una consulta hacia el servidor, para conocer las inscripciones de la ventana actual.
El servidor_inscripciones tiene una ventana de tiempo fija de un minuto, cada vez que se cumple un minuto, los registros que le llegaron los pasa a la "ventana actual", y las incripciones que se hagan en el nuevo minuto, quedarán en la "ventana siguiente". Además, en el archivo inscripciones.json se mantiene el registro histórico de todas las incripciones.

Los mensajes se envían en formato JSON, se serializa al enviar y se deserializa al recibir. 

La máquina virtual de Google ejecuta el comando: ```docker compose up```, ejecutando el archivo ```docker-compose.yml``` de esta carpeta. De esta manera todos los contenedores se encuentran en la misma red, por lo que los cliente_servidor se pueden comunicar hacia el servidor_inscripciones.

Para ver el flujo del programa, acceda a los logs de los containers con el comando ```sudo docker logs <id_container_h7>```
