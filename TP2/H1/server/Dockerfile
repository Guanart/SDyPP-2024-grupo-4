FROM python:alpine3.19
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip install -r server_requirements.txt
ENTRYPOINT ["python", "server.py"] 
