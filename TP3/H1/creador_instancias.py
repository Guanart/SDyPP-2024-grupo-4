from google.cloud import compute_v1
# from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
# load_dotenv()

# project = os.getenv('PROJECT_ID')
# zone = os.getenv('ZONE')
# instance_name = os.getenv('INSTANCE_NAME')
# machine_type = os.getenv('MACHINE_TYPE')
# image = os.getenv('IMAGE')
# network_interface = {
#     'network': 'global/networks/default',
#     'accessConfigs': [{
#         'type': 'ONE_TO_ONE_NAT',
#         'name': 'External NAT'
#     }]
# }

project = 'your-project-id'
zone = 'us-central1-a'
instance_name = 'instance-1'
machine_type = 'zones/{}/machineTypes/n1-standard-1'.format(zone)
image = 'projects/debian-cloud/global/images/debian-9-stretch-v20220407'
network_interface = {
    'network': 'global/networks/default',
    'accessConfigs': [{
        'type': 'ONE_TO_ONE_NAT',
        'name': 'External NAT'
    }]
}



compute = compute_v1.InstancesClient()
operation = compute.insert(project=project, zone=zone, body={
    'name': instance_name,
    'machineType': machine_type,
    'disks': [{
        'boot': True,
        'autoDelete': True,
        'initializeParams': {
            'sourceImage': image
        }
    }],
    'networkInterfaces': [network_interface]
})

print('Instance created: {}'.format(operation))



firewall_client = compute_v1.FirewallsClient()
firewall_body = {
    'name': 'allow-ssh-http-https',
    'network': 'global/networks/default',
    'allowed': [{
        'IPProtocol': 'tcp',
        'ports': ['22', '80', '443']
    }]
}
firewall = firewall_client.insert(project=project, body=firewall_body)
