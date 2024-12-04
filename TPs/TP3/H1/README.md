# H1

## Descripción de funcionamiento

En el archivo ```main.tf``` se encuentra el resource "google_compute_instance" "vm_instance", y dentro del mismo se tienen dos parámetros que permiten generar un número determinado de instancias, son ```count = var.num_instances``` y ```name = "my-instance-${count.index}"```. 

En el archivo ```variables.tf``` se encuentra definida una variable llamada ```"num_instances"``` que no se encuentra inicializada, y permite que al ejecutar el "apply" del proyecto terraform, se solicite por consola el número de instancias a generar.

Lo solicitado en el H2 también se encuentra en esta carpeta, y la carpeta H2 contiene la respuesta a la pregunta teórica.