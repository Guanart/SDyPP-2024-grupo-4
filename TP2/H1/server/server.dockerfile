FROM docker:stable-dind

WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN apk update
RUN apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python
# RUN python3 -m venv ./venv
# RUN source ./venv/bin/activate
# RUN pip install --no-cache --upgrade pip setuptools
COPY . .
RUN pip install -r server_requirements.txt
# RUN apk add --update --no-cache py3-flask py3-docker py3-jsonify
# RUN python3 -m pip install -r server_requirements.txt
# RUN python3 -m pip install --upgrade pip
# RUN docker pull grupo4sdypp2024/tp2-h1-task1
# CMD ["python", "servidor.py"]

RUN apk add --update --no-cache bash tini

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["tini", "--", "/entrypoint.sh"] 
