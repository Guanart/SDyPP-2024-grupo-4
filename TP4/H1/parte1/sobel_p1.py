import cv2
import numpy as np
import sys

def filtro_sobel(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro Sobel
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Combinar los resultados de los filtros Sobel
    sobel_combined = cv2.magnitude(sobelx, sobely)

    # Normalizar los valores entre 0 y 255
    sobel_normalized = np.uint8(255 * sobel_combined / np.max(sobel_combined))

    return sobel_normalized

def main(image):
    # Cargar la imagen de entrada
    imagen_original = cv2.imread(image)

    # Aplicar el filtro Sobel
    imagen_resultado = filtro_sobel(imagen_original)

    # Guardar la imagen resultante
    cv2.imwrite(image +'_sobel.jpg', imagen_resultado)

    print("Proceso completado. Imagen de salida guardada como 'imagen_sobel.jpg'.")

if __name__ == "__main__":  
    args = sys.argv #El sys fue lo que no le anduvo a marian? F
    
    if (2 != len(args)):
        print("Uso: python sobel.py <IMAGE_NAME> (.JPG)")
        sys.exit(0)
    main(args[1])