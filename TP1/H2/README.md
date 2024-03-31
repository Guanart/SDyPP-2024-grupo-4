# SDyPP-2024-grupo-4
## HIT 2

El archivo servidor.js se ejecuta en el puerto 8002 de un container de Docker.
La máquina virtual de Google ejecuta el comando: ```docker run -p 8002:8002```.

Desde otra máquina se debe ejecutar el comando: ```node cliente.js``` para poner en ejecución el cliente, que envía un saludo al servidor, y recibe una respuesta del mismo.

El cliente tiene un sistema que le permite intentar reconectarse al servidor 3 veces si este cierra la conexión, por ejempl al terminarse abruptamente.
