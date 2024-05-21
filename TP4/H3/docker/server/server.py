from flask import Flask, request, send_file
import uuid, requests, io

app = Flask(__name__)

def es_imagen_jpg(data):
    # Verifica que son los primeros bytes de un archivo JPEG/JPG
    return data[:2].lower() == b'\xff\xd8'

def particionar(imagen_data, id):
    # Envia la imagen al particionador, esperando respuesta
    response = requests.post("http://particionador:5001/particionar", files={"imagen": imagen_data}, data={"id": id})
    return response.status_code

def unificador(id):
    url = 'http://unificador:5002/getImage?id=' + id;
    return requests.get(url)

@app.route('/getImage', methods=['GET'])
def retornar_imagen():
    id = request.args.get('id')
    response = unificador(id)
    if response.status_code == 200:
        img_file = io.BytesIO(response.content)
        return send_file(img_file, mimetype='image/jpeg')
    else:
        return "Ocurrió un error en el servidor", 500

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
        imagen = request.data #or request.files["imagen"]
        if not es_imagen_jpg(imagen):
            return "El archivo no es una imagen JPG", 400
        
        id = uuid.uuid4()   # Genera un ID único para la imagen

        """with open("./imagen_" + str(id) + "_serverweb" + ".jpg", 'wb') as f:
            f.write(imagen)"""
        
        if particionar(imagen, id) != 200:
            return "Ocurrió un error en el servidor", 500

        return str(id)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
