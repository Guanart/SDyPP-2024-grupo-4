#!/bin/bash
git clone https://github.com/Guanart/SDyPP-2024-grupo-4.git
cd SDyPP-2024-grupo-4
sudo find TP1 -mindepth 2 -type f -name "docker-compose.yml" -execdir docker compose up -d \;

sudo docker run -d -p 8001:8001 --name tp1-h1 grupo4sdypp2024/tp1-h1
sudo docker run -d -p 8002:8002 --name tp1-h2 grupo4sdypp2024/tp1-h2
sudo docker run -d -p 8003:8003 --name tp1-h3 grupo4sdypp2024/tp1-h3