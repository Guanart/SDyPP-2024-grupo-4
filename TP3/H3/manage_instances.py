from google.cloud import compute_v1
from google.oauth2 import service_account
import os, sys

# Path al archivo de credenciales
credentials_path = '../H1/credentials.json'

# Crea una instancia del cliente Compute Engine
credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)
client = compute_v1.InstancesClient(credentials=credentials)

project = 'sharp-technique-416800'
zone = 'us-east1-d'

def list_instances():
    instances = client.list(project=project, zone=zone)
    for instance in instances:
        print(f"[{instance.name}] {instance.id} | {instance.status}")

# Funciones para controlar las instancias
def start_instance(instance_name):
    request = client.start(project=project, zone=zone, instance=instance_name)
    return request

def stop_instance(instance_name):
    request = client.stop(project=project, zone=zone, instance=instance_name)
    return request

def restart_instance(instance_name):
    stop_instance(instance_name)
    start_instance(instance_name)

def delete_instance(instance_name):
    request = client.delete(project=project, zone=zone, instance=instance_name)
    return request


if __name__== "__main__":
    args = sys.argv
    
    if (3 < len(args)) or (len(args) < 2):
        print("Uso: python manage_instances.py list|start|stop|restart|delete <INSTANCE_NAME>")
        sys.exit(1)
    
    action = args[1]
    if len(args)==3:
        instance_name = args[2]

    match action:
        case 'list':
            list_instances()
        case 'start':
            start_instance(instance_name)
            list_instances()
        case 'stop':
            stop_instance(instance_name)
            list_instances()
        case 'restart':
            restart_instance(instance_name)
            list_instances()
        case 'delete':
            delete_instance(instance_name)
            list_instances()