#!/bin/bash

sudo apt update -y 
sudo apt install -y wget htop nginx ufw

# ufw allow ssh
# ufw allow http
# ufw allow https

sudo service start nginx
