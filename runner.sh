gcloud services enable logging.googleapis.com
gcloud logging read "resource.type=gce_instance AND protoPayload.methodName=beta.compute.instances.insert"
gcloud compute firewall-rules create allow-ssh --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0

gcloud compute instances create vm2 \
    --machine-type=e2-micro \
    --preemptible \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server \
    --metadata="ssh-keys=$(cat ./id_rsa_gcloud.pub)" \
    --metadata-from-file user-data=script.sh \
    --zone="us-east1-b" \
    --address=instance-public-ip

gcloud compute ssh vm2 --zone=us-east1-b --command "cat /var/log/cloud-init-output.log"