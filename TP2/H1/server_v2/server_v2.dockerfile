FROM python:alpine3.19
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip install -r server_v2_requirements.txt
ENTRYPOINT ["python", "servidor_v2.py"] 
