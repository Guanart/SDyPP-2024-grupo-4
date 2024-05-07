import cv2
import numpy as np

# PARTE 2:
# La imagen se divide.
# Las partes de las imágenes las reciben workers.
# Los workers (todos utilizan la misma imagen de docker) pueden estar en la misma o en distintas VM.
# Función para unir las imágenes.
# debería utilizar p1, o por lo menos hace lo mismo.

import cv2
import numpy as np

def dividir_imagen(imagen, num_filas, num_columnas):
    alto, ancho, _ = imagen.shape
    partes = []
    for i in range(num_filas):
        for j in range(num_columnas):
            parte = imagen[i * (alto // num_filas):(i + 1) * (alto // num_filas),
                            j * (ancho // num_columnas):(j + 1) * (ancho // num_columnas)]
            partes.append(parte)
    return partes

def reconstruir_imagen(partes, num_filas, num_columnas):
    alto = partes[0].shape[0]
    ancho = partes[0].shape[1]
    imagen_reconstruida = np.zeros((alto * num_filas, ancho * num_columnas, 3), dtype=np.uint8)
    contador = 0
    for i in range(num_filas):
        for j in range(num_columnas):
            imagen_reconstruida[i * alto:(i + 1) * alto, j * ancho:(j + 1) * ancho] = partes[contador]
            contador += 1
    return imagen_reconstruida

# Cargar imagen
imagen = cv2.imread('imagen.jpg')
filas = 2
columnas = 2
# Dividir imagen en 3x3 partes
partes = dividir_imagen(imagen, filas, columnas)   

# Guardar partes divididas como archivos separados
for i, parte in enumerate(partes):
    cv2.imwrite(f'parte_{i}.jpg', parte)

# Reconstruir la imagen
imagen_reconstruida = reconstruir_imagen(partes, filas, columnas)

# Mostrar imagen reconstruida
cv2.imwrite('imagen_reconstruida.jpg', imagen_reconstruida)
cv2.waitKey(0)
cv2.destroyAllWindows()
