const net = require('net');

// Al iniciar el programa C, se le deben proporcionar por parámetros la dirección IP 
// y el puerto para escuchar saludos, así como la dirección IP y el puerto de otro nodo C.
// De esta manera, al tener dos instancias de C en ejecución, cada una configurada
// con los parámetros del otro, ambas se saludan mutuamente a través de cada canal de comunicación.

// FUNCIONES DE SERVIDOR:

// 