from flask import Flask, request
import uuid, requests

app = Flask(__name__)

def es_imagen_jpg(data):
    # Verificar que son los primeros bytes de un archivo JPEG/JPG
    return data[:2].lower() == b'\xff\xd8'

@app.route('/sobel', methods=['POST'])
def recibir_imagen():
    try:
        # Obtener la imagen del cuerpo de la solicitud
        imagen = request.data

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
    

def particionar(imagen_data, id):
    url = "http://localhost:5001/" # Arreglar
    response = requests.post(url, files={"imagen": imagen_data}, data={"id": id})
    return response.status_code

if __name__ == '__main__':
    app.run()
