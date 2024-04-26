# SDyPP-2024-grupo-4
## HIT 4

El cliente_servidor recibe por argumentos la IP y el puerto en el que debe escuchar el servidor, y la IP y el puerto del servidor al que se debe conectar.

La máquina virtual de Google ejecuta el comando: ```docker compose up```, ejecutando el archivo ```docker-compose.yml``` de esta carpeta. De esta manera ambos contenedores se encuentran en la misma red, por lo que los dos cliente_servidor se pueden comunicar.

Para ver la ejecución, acceda a los logs de los containers con el comando ```sudo docker logs <id_container_h4>```
