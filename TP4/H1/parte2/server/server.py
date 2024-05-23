from flask import Flask, request, send_file
import uuid, requests, io

app = Flask(__name__)

@app.route('/getImage', methods=['GET'])
def retornar_imagen():
    id = request.args.get("id")
    url = 'http://unificador:5002/getImage?id=' + id
    response = requests.get(url)

    if response.status_code != 200:
        return response.text, response.status_code
    else:
        img_file = io.BytesIO(response.content)
        return send_file(img_file, mimetype='image/jpeg')

@app.route('/sobel', methods=['POST'])
def recibir_imagen():
    if "imagen" not in request.files or "filas" not in request.form or "columnas" not in request.form:
        return "Faltan datos en la petición", 400
    
    imagen = request.files["imagen"]
    filas = request.form["filas"]
    columnas = request.form["columnas"]
    imagen_binario = imagen.read()
    
    if imagen_binario[:2].lower() != b'\xff\xd8':
        return "El archivo no es una imagen JPG, solo se aceptan extensiones .jpg o .jpeg", 400
    
    id = uuid.uuid4()
    
    response = requests.post("http://particionador:5001/particionar", 
                            files={"imagen": imagen_binario}, 
                            data={"filas": filas, "columnas": columnas, "id": id})
    
    if response.status_code != 200:
        return response.text, response.status_code
    else:
        return str(id), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
