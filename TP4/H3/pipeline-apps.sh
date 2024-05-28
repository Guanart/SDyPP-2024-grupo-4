#!/bin/bash

gcloud container clusters get-credentials primary --region=us-east1-b
kubectl apply -f deployments/web-server-deployment.yaml
kubectl apply -f deployments/unificador-deployment.yaml
kubectl apply -f deployments/particionador-deployment.yaml


crack master fiera, como genero en la nube el unificador
tengo q romper toda la infra?? ....zzzzzzz
no
un nuevo deployment y listo creo

hice kubectl apply -f . y nada
estoy en ubuntu xddddddddddddddddddd