FROM python:alpine3.19

RUN mkdir -p /usr/local/src/pythonapp
RUN touch /usr/local/src/pythonapp/cliente_servidor.log
WORKDIR /usr/local/src/pythonapp
ADD cliente_servidor.py cliente_servidor.py
ENTRYPOINT ["python3", "cliente_servidor.py"]