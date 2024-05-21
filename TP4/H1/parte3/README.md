# H1 - PARTE 3
## El operador de Sobel de forma distribuida (recuperación en caso de falla de workers)

Las tareas siguen de forma distribuida mediante contenedores Docker (local), pero se agrega una configuración de Rabbit para que en caso de que un worker no pueda procesar la imagen, o no se reciba un ACK del worker en un tiempo determinado, la parte de la imagen se pueda reencolar.

Para utilizar esto, primero debe levantar los contenedores (debe tener el ```docker-compose.yml```):
```
docker compose up
```
Luego puede utilziar el ```client.py```. La imagen que envía debe ser .jpg.