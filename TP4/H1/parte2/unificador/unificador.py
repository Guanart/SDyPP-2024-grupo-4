# Este código fue lo primero que hicimos, todavía no está funcional, sirve de ejemplo
"""
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
"""