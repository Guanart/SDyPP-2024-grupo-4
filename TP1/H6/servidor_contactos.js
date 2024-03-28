const net = require("net");

// --------------------------------------------------------
// { id: integer, data: {Object}}

// nodo: clase cliente corriendo - clase servidor corriendo
// PASOS:
// 1 - El cliente le envía su IP y puerto.  // HECHO
// 2 - El servidor de contactos agrega esos datos a la lista. // HECHO
// 3 - El servidor de contactos le informa a cada nodo la actualización de la lista. (necesitamos una lista de sockets)  // HECHO
// 4 - El cliente de contactos recibe la lista y se la da al modulo cliente

// Código antiguo: ;(
/*
  const index = sockets.findIndex(i => i.socket === socket);  // Agregamos el id del mensaje
  sockets[index].id_msg = id;

  sockets.forEach((socket) => {
    write(socket.socket, socket.id_msg, _CONTACTOS_, null) // Le notificamos la nueva lista a todos los nodos
  });  
*/

let sockets = []; // { socket: socket, id_msg: integer }

let _CONTACTOS_ = []; // Objetos {ip: String, puerto: integer}
/*
FORMATO DEL MENSAJE:
  { 
    id: integer,
    data: {
      type: 'setContacto',
      ip: string,
      port: ing
    }
  }
 */

const _PROTOCOLO_ = {
  setContacto: (socket, id, data) => {
    // Registra nodo y envía a todos los contactos en _CONTACTOS_ la lista actualizada (hace broadcast)
    _CONTACTOS_.push({ ip: data.ip, puerto: data.puerto }); // Agrego a la lista de contactos este nodo

    // funcionalidad cliente para conectarse al servidor y pasar la lista

    
  


  },
};

function connectToServer(ip, puerto) {
  const socket = net.createConnection(this.opts, () => {
    this.reconexiones = 0;
    var buffer = "";

    this.socket.on("data", (chunk) => {
      buffer += chunk.toString();
      buffer = this.read(buffer);
    });

    this._MAIN_(this.socket);
  });

  this.socket.on("end", () => {
    console.log("CLIENTE: Desconectado del server");
    this.reconectar();
  });

  this.socket.on("error", (err) => {
    if (err.code === "ECONNRESET") {
      console.log("CLIENTE: El servidor cerró de forma abrupta");
      this.reconectar();
    } else if (err.code === "ECONNREFUSED") {
      console.log("CLIENTE: El servidor está cerrado");
      this.reconectar();
    } else {
      console.error(err);
    }
  });
};


const server = net.createServer((socket) => {
  sockets.push({ socket: socket, id_msg: null }); // Agrego el socket a la lista

  var buffer = "";

  socket.on("end", () => {
    socket.destroy();
    sockets = sockets.filter((i) => i !== socket); // Itera en todos los sockets
  });

  socket.on("data", (chunk) => {
    buffer += chunk.toString();

    try {
      const data = read(buffer);
      buffer = data.buffer;

      data.messages.forEach((message) => {
        parse(message, socket);
      });
    } catch (err) {
      console.error("!!! INTENTO DE HACKEO !!!");
      socket.end();
    }
  });

  socket.on("error", () => {});
});

server.on("error", (err) => {
  console.error(err);
});

server.listen(8080, () => {
  console.log("Contact server ready.");
});

// --------------------------------------------------------

function read(buffer) {
  let messages = buffer.split("|");

  buffer = messages.pop();
  messages = messages
    .map((msj) => {
      // array de Objects
      try {
        msj = JSON.parse(msj); //trata de analizar el mensaje como JSON
      } catch (err) {
        msj = false;
      }

      return msj;
    })
    .filter(Boolean); // elimina los false y los null

  return { messages, buffer };
}

function parse(message, socket) {
  console.dir(message, { depth: null });

  if (!_PROTOCOLO_.hasOwnProperty(message.data.type)) {
    console.error("Tipo de mensaje no reconocido");
    console.error(message);
    socket.end();
    return;
  }

  try {
    _PROTOCOLO_[message.data.type](socket, message.id, message.data.data);
  } catch (err) {
    console.error(message);
    console.error(err);
  }
}

function write(socket, id, data, error) {
  try {
    data = JSON.stringify({ id, data, error });
    socket.write(data + "|");
  } catch (err) {
    console.error(data);
    console.error(err);
  }
}
