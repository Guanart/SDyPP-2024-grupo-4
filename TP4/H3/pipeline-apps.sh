#!/bin/bash

gcloud container clusters get-credentials primary --region=us-east1-b
kubectl apply -f deployments/web-server-deployment.yaml
kubectl apply -f deployments/unificador-deployment.yaml
kubectl apply -f deployments/particionador-deployment.yaml

