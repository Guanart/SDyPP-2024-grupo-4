from flask import Flask, request
import uuid, requests

app = Flask(__name__)

def es_imagen_jpg(data):
    # Verificar que son los primeros bytes de un archivo JPEG/JPG
    return data[:2].lower() == b'\xff\xd8'

def particionar(imagen_data, id):
    url = "http://localhost:5001/particionar" # Arreglar
    response = requests.post(url, files={"imagen": imagen_data}, data={"id": id})
    return response.status_code

@app.route('/sobel', methods=['POST'])
def recibir_imagen():
    """
    Función que recibe una imagen en formato JPG a través de una solicitud POST.
    La imagen se guarda en el servidor con un ID único y se llama al servidor particionador.
    Si todo es exitoso, se retorna el ID de la imagen guardada.

    Returns:
        str: ID de la imagen guardada en el servidor.

    Raises:
        str: Mensaje de error si ocurre alguna excepción.
    """
    try:
        # Obtener la imagen del cuerpo de la solicitud
        imagen = request.data #or request.files["imagen"]

        if not es_imagen_jpg(imagen):
            return "El archivo no es una imagen JPG", 400
        
        # Guardar la imagen en el servidor, con un id único
        id = uuid.uuid4()
        with open("./imagen_" + str(id) + "_serverweb" + ".jpg", 'wb') as f:
            f.write(imagen)
        
        # Llamar al servidor particionador
        if particionar(imagen, id) != 200:
            return "Ocurrió un error en el servidor", 500

        # Retornar ID de la imagen
        return str(id)
    except Exception as e:
        return str(e), 500
    
if __name__ == '__main__':
    app.run()
