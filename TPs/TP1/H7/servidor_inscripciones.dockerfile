FROM python:alpine3.19

RUN mkdir -p /usr/local/src/pythonapp
RUN touch /usr/local/src/pythonapp/servidor_inscripciones.log
WORKDIR /usr/local/src/pythonapp
ADD servidor_inscripciones.py servidor_inscripciones.py
ENTRYPOINT ["python3", "servidor_inscripciones.py"]