#!/bin/bash

USERNAME="gonzalobenitounlu"; ssh-keygen -t rsa -b 4096 -C "${USERNAME}@gmail.com" -f ./id_rsa_example -q -N ""
# gcloud compute project-info add-metadata --metadata "ssh-keys=${USERNAME}:$(cat ./id_rsa_gcloud.pub)"
gcloud compute project-info add-metadata --metadata "ssh-keys=${USERNAME}:$(cat ./id_rsa_example.pub)"
