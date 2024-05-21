# H2
## Sobel con offloading en la nube

Ahora se tiene un esquema híbrido:
- En una VM se encuentran dockerizados el server, el particionador, el unificador, Redis y RabbitMQ.
- En VMs del tipo "SPOT" hay Workers consumiendo en la cola que se encuentra en el RabbitMQ de la otra VM.
- El cliente que se conecta puede tener un docker trabajando como worker también.

Para utilizar el cliente, se debe ejecutar el siguiente comando:
```
python client.py
```
Este programa le pide que ingrese la dirección IP del servidor, ahora mismo la IP es: ```34.138.74.138```.