#!/bin/bash
gcloud compute firewall-rules create allow-http-tp1-h1 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8001 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-http-tp1-h2 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8002 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-http-tp1-h3 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8003 --source-ranges=0.0.0.0/0

gcloud compute instances delete tp1 --zone us-east1-b --quiet
gcloud compute instances create tp1 \
    --machine-type=e2-micro \
    --preemptible \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server \
    --metadata="ssh-keys=:$(cat ../id_rsa_example.pub)" \
    --metadata-from-file user-data=script.sh \
    --zone="us-east1-b" \
    --address=instance-public-ip

# gcloud compute ssh vm1 --zone=us-east1-b --ssh-key-file=../id_rsa_example --command "cat /var/log/cloud-init-output.log"
gcloud compute ssh --zone "us-east1-b" "tp1" --project "sharp-technique-416800"