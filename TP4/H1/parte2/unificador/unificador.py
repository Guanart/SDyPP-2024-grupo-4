import numpy as np
import redis, cv2

def buscar_partes(num_partes, id):
    r = redis.Redis(host='localhost', port=6379)
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

if __name__ == '__main__':
    id = "892d05b5-7110-4b2b-9432-7da4637ab6fa"; # Hardcodeado para probar
    filas = 2
    columnas = 2
    partes = buscar_partes(filas*columnas, id)
    if len(partes) != (filas*columnas):
        print("Todavía no están terminadas todas las partes")
    else:
        imagen_reconstruida = reconstruir_imagen(partes, filas, columnas)
        cv2.imwrite("imagen_reconstruida.jpg", imagen_reconstruida)
        print(f"Imagen reconstruida guardada.")