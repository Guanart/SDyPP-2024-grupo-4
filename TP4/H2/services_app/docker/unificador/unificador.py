import numpy as np
from flask import Flask, request, send_file
import redis, cv2, os

app = Flask(__name__)

def buscar_partes(num_partes: int, id: str) -> list:
    """
    Busca las partes de una imagen en Redis y las decodifica en imágenes de OpenCV.

    Args:
        num_partes (int): El número total de partes de la imagen.
        id (str): El identificador único de la imagen.

    Returns:
        list: Una lista de imágenes de OpenCV que representan las partes de la imagen.
    """
    r = redis.Redis(host='redis', port=6379, password=redis_password)
    partes = []
    for i in range(num_partes):
        # Obtener la parte de Redis como bytes
        clave = id + "_" + str(i)
        parte_bytes = r.get(clave)

        # Verificar si la parte está en Redis
        if parte_bytes is not None:
            # Decodificar los bytes en una imagen de OpenCV
            parte_opencv = cv2.imdecode(np.frombuffer(parte_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            partes.append(parte_opencv)
        else:
            print(f"La parte {i} no se encuentra en Redis.")
    return partes

def reconstruir_imagen(partes: list, num_filas: int, num_columnas: int) -> np.ndarray:
    """
    Reconstruye una imagen a partir de sus partes.

    Args:
        partes (list): Una lista de imágenes de OpenCV que representan las partes de la imagen.
        num_filas (int): El número de filas en las que se dividieron las partes.
        num_columnas (int): El número de columnas en las que se dividieron las partes.

    Returns:
        np.ndarray: La imagen reconstruida como una matriz NumPy.
    """
    alto_parte, ancho_parte, _ = partes[0].shape
    alto_imagen = alto_parte * num_filas
    ancho_imagen = ancho_parte * num_columnas
    imagen_reconstruida = np.zeros((alto_imagen, ancho_imagen, 3), dtype=np.uint8)
    contador = 0
    for fila in range(num_filas):
        for columna in range(num_columnas):
            inicio_y = fila * alto_parte
            fin_y = inicio_y + alto_parte
            inicio_x = columna * ancho_parte
            fin_x = inicio_x + ancho_parte
            imagen_reconstruida[inicio_y:fin_y, inicio_x:fin_x] = partes[contador]
            contador += 1
    return imagen_reconstruida

@app.route('/getImage')
def get_image():
    id = request.args.get('id')
    partes = buscar_partes(filas * columnas, id)
    if len(partes) != (filas * columnas):
        print("Todavía no están terminadas todas las partes")
        return "Todavía no está lista la imagen", 500
    else:
        imagen_reconstruida = reconstruir_imagen(partes, filas, columnas)
        filename = id + ".jpg"
        cv2.imwrite(filename, imagen_reconstruida)
        print(f"Imagen reconstruida guardada.")
        return send_file(filename, mimetype='image/jpeg')

if __name__ == '__main__':
    filas: int = 2
    columnas: int = 2
    redis_password = os.getenv('REDIS_PASSWORD')
    app.run(host='0.0.0.0', port=5002)