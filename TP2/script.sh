#!/bin/bash

sudo apt update
sudo apt install python -y

# Instalar Docker
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

IMAGES=(
  "grupo4sdypp2024/tp2-h1-task1"
  "grupo4sdypp2024/tp2-h1-task2"
  "grupo4sdypp2024/tp2-h1-task3"
  "grupo4sdypp2024/tp2-h1-server"
  "grupo4sdypp2024/tp1-h1"
  "grupo4sdypp2024/tp1-h2"
  "grupo4sdypp2024/tp1-h3"
  "grupo4sdypp2024/tp1-h4"
  "grupo4sdypp2024/tp1-h5"
  "grupo4sdypp2024/tp1-h6-servidor_contactos"
  "grupo4sdypp2024/tp1-h6-cliente_servidor"
  "grupo4sdypp2024/tp1-h7-servidor_inscripciones"
  "grupo4sdypp2024/tp1-h7-cliente_servidor"
)

for IMAGE in "${IMAGES[@]}"
do
  sudo docker pull $IMAGE
done

git clone https://github.com/Guanart/SDyPP-2024-grupo-4.git
cd SDyPP-2024-grupo-4
sudo find TP1 -mindepth 2 -type f -name "docker-compose.yml" -execdir docker compose up -d \;

sudo docker run -p 8001:8001 --name tp1-h1 grupo4sdypp2024/tp1-h1
sudo docker run -p 8002:8002 --name tp1-h2 grupo4sdypp2024/tp1-h2
sudo docker run -p 8003:8003 --name tp1-h3 grupo4sdypp2024/tp1-h3
sudo docker run -p 8021:5000 --name tp2-h1 grupo4sdypp2024/tp2-h1-server