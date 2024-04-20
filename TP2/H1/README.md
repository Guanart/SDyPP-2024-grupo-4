# Hit 1 - Práctica
## Cliente
```cliente.py``` es un programa que presenta un menú para la conexión hacia un determinado host. Se deben ingresar los datos del host (IP y puerto) y luego el tipo de tarea a realizar (suma, resta o multiplicación), una vez ingresados esos parámetros, es posible hacer el envío de la tarea.

## Servidor
```servidor.py``` corre en el host como un contenedor docker, lo primero que hace al crearse es descargarse de Docker Hub las imágenes de las distintas tareas genéricas.

Cuando recibe una tarea mediante el método POST en el endpoint ```/getRemoteTask```, crea un contenedor de la tarea que se pasó por el JSON de argumentos, y envía los datos a la misma mediante el endpoint ```/ejecutarTarea```.

## Tarea
Las distintas task tienen el código necesario para resolver las tareas. Se ejecutan en contenedores Docker.