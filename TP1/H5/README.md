# SDyPP-2024-grupo-4
## HIT 5

(Es el mismo que el H4, ya que en H4 ya habíamos utilizado el formato JSON)

El cliente_servidor recibe por argumentos la IP y el puerto en el que debe escuchar el servidor, y la IP y el puerto del servidor al que se debe conectar.

Ya que el ejercicio se encuentra hecho en una red de Docker, se necesita probar de forma local, las instrucciones son las siguientes:

1. Ejecutar ```docker build -t grupo4sdypp2024/tp1-h5 .``` para crear la imagen, o descargarla de Docker Hub mediante el comando ```docker pull grupo4sdypp2024/tp1-h5```.
2. Ejecutar ```docker compose up```, de esta manera docker ejecuta el archivo ```docker-compose.yml```, en este se generan dos cliente-servidor que se saludan mutuamente y devuelven el saludo.