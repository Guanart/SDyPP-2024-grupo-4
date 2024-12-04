FROM python:alpine3.19

RUN mkdir -p /usr/local/src/pythonapp
RUN touch /usr/local/src/pythonapp/servidor_contactos.log
WORKDIR /usr/local/src/pythonapp
ADD servidor_contactos.py servidor_contactos.py
ENTRYPOINT ["python3", "servidor_contactos.py"]