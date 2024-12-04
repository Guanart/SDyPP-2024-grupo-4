FROM python:3.12.3-slim
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "particionador.py"]