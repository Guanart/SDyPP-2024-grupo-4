#!/bin/bash

# Turn on bash's job control
set -m

# Start docker service in background
/usr/local/bin/dockerd-entrypoint.sh &

# Wait that the docker service is up
while ! docker info; do
    echo "Waiting docker..."
    sleep 3
done

docker pull grupo4sdypp2024/tp2-h1-task1

python servidor.py &

# Bring docker service back to foreground
fg %1