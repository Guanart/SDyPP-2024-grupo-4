# H1 - PARTE 1
## El operador de Sobel

El archivo ```sobel.py``` utiliza la librería OpenCV (cv2 en python) para poder aplicar el filtro sobel.

Primero ejecute el script ```init.services.sh``` para levantar el RabbitMQ y el Redis.

Luego, para utilizar el operador de Sobel, se debe ejecutar el siguiente comando:
```
python sobel.py {nombre_imagen.jpg}
```
La imagen debe ser .jpg o .jpeg. Cuando se termine de procesar se guardará una nueva imagen con el operador de Sobel aplicado.
