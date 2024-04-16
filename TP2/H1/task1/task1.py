from flask import Flask, jsonify, request

app = Flask(__name__)

# Esta tarea suma dos números
@app.route("/ejecutarTarea", methods=['GET', 'POST'])
def ejecutarTarea():
    task_params = request.get_json()
    print(task_params)
    response = {
        'resultado': int(task_params['number1']) + int(task_params['number2'])
    }
    response = jsonify(response)
    print(response)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)