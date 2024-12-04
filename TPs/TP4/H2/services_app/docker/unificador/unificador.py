import numpy as np
from flask import Flask, request, send_file
import redis, cv2, sys, io, os

app = Flask(__name__)

def buscar_partes(num_partes, id):
    partes = []
    for i in range(num_partes):
        # Obtener la parte de Redis como bytes
        clave = id + "_" + str(i+1)
        parte_bytes = r.get(clave)

        # Verificar si la parte está en Redis
        if parte_bytes is not None:
            # Decodificar los bytes en una imagen de OpenCV
            parte_opencv = cv2.imdecode(np.frombuffer(parte_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            partes.append(parte_opencv)
        else:
            print(f"La parte {i+1} no se encuentra en Redis.")
    return partes

def reconstruir_imagen(partes, num_filas, num_columnas):
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

def eliminar_partes(num_partes, id):
    r.delete(id+"_filas")
    r.delete(id+"_columnas")
    for i in range(num_partes):
        clave = id + "_" + str(i+1)
        r.delete(clave)

@app.route('/getImage')
def get_image():
    id = request.args.get("id")
    filas = int(r.get(id+"_filas").decode('utf-8'))
    columnas = int(r.get(id+"_columnas").decode('utf-8'))
    partes = buscar_partes(filas * columnas, id)
    if len(partes) != (filas * columnas):
        print("Todavía no están terminadas todas las partes")
        return "Todavía no está lista la imagen", 200
    else:
        eliminar_partes(filas * columnas, id)
        imagen_reconstruida = reconstruir_imagen(partes, filas, columnas)
        _, imagen_bytes = cv2.imencode('.jpg', imagen_reconstruida)
        return send_file(io.BytesIO(imagen_bytes.tobytes()), mimetype='image/jpeg')

if __name__ == '__main__':
    try:
        redis_password = os.getenv('REDIS_PASSWORD')
        r = redis.StrictRedis(host='redis', port=6379, password=redis_password)
        print("Conectado a Redis")
    except Exception as e:
        print(f"No se pudo conectar a Redis: {e}")
        sys.exit(1) 
    app.run(host='0.0.0.0', port=5002)