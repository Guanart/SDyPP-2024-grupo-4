#!/bin/bash

gcloud container clusters get-credentials primary --region=us-east1-b
kubectl apply -f deployments/rabbitmq-deployment.yaml
kubectl apply -f deployments/redis-deployment.yaml