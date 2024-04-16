from flask import jsonify
import requests
import json


url = 'http://localhost:5000/getRemoteTask'
data = {
	"image": "grupo4sdypp2024/tp2-h1-task1",
	"number1": 1,
	"number2": 2
}
headers = {'Content-Type': 'application/json'}
json_data = json.dumps(data)
response = requests.post(url, data=json_data, headers=headers)

print(response)
print(response.text)
