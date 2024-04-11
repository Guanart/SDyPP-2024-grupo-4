FROM python:3.9.19-alpine3.19
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install jsonify
CMD ["python", "tarea.py"]