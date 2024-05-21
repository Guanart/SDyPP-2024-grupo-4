#!/bin/bash

gcloud container clusters get-credentials primary --region=us-east1-b
kubectl apply -f deployments/particionador-deployment.yaml
kubectl apply -f deployments/web-server-deployment.yaml