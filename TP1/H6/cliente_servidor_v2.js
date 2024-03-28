const net = require("net");

class Servidor {
  constructor(host, port) {
    this.opts = {
      host: host,
      port: port,
    };
    this.server = null;
    this.cliente = null;
  }

  setCliente(cliente){
    this.cliente = cliente
  }

  _PROTOCOLO_ = {
    saludo: (socket, id, data) => {
      setTimeout(() => {
        console.log("HOST: Respondiendo saludo...");
        this.write(socket, id, { message: "Hola!" }, null);
      }, 5000);
    },
    actualizarContactos: (socket, id, data) => {
      setTimeout(() => {
        console.log("HOST: Se recibio una nueva lista de contactos.");
        console.log("HOST: Enviando la lista actualizada al modulo CLIENTE.");
        this.cliente.actualizarContactos(data.data);
      }, 5000);
    }
  };

  instanciateServer() {
    this.server = net.createServer((socket) => {
      var buffer = "";

      socket.on("data", (chunk) => {
        buffer += chunk.toString();

        try {
          const data = this.read(buffer);
          buffer = data.buffer;

          data.messages.forEach((message) => {
            this.parse(message, socket);
          });
        } catch (err) {
          //console.error(err);
          console.error("HOST: !!! INTENTO DE HACKEO !!!");
          socket.end();
        }
      });

      socket.on("error", () => {});
    });

    this.server.listen(this.opts.port, this.opts.host, () => {
      console.log("HOST: Server ready.");
    });

    this.server.on("error", (err) => {
      console.error(err);
    });
  }

  read(buffer) {
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

  parse(message, socket) {
    console.log("HOST: El mensaje recibido:")
    console.dir(message, { depth: null });

    if (!this._PROTOCOLO_.hasOwnProperty(message.data.type)) {
      console.error("HOST: Tipo de mensaje no reconocido");
      console.error(message);
      socket.end();
      return;
    }

    try {
      this._PROTOCOLO_[message.data.type](socket, message.id, message.data);
    } catch (err) {
      console.error(message);
      console.error(err);
    }
  }

  write(socket, id, data, error) {
    try {
      data = JSON.stringify({ id, data, error });
      socket.write(data + "|");
    } catch (err) {
      console.error(data);
      console.error(err);
    }
  }
}

//--------------------------------------------------------------------

class ClienteContactos {  // Solo se registra en el server

  constructor(host, port, self_host, self_port) {
    this.opts = {
      host: host,
      port: port,
    };
    this.self_opts = {
      host: self_host,
      port: self_port,
    };
    this.reconexiones = 0;
    this.socket = null;
    this._PROMISES_ = {};
  }

  connectToServer() {
    this.socket = net.createConnection(this.opts, () => {
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
  }

  reconectar() {
    if (!this.socket || this.socket.destroyed) {
      // Verifica si no hay conexión existente
      if (this.reconexiones < 2) {
        console.log('CLIENTE: Intentando reconectar...');
        setTimeout(() => {
          this.reconexiones += 1;
          this.connectToServer();
        }, 5000);
      } else {
        console.log(
          "CLIENTE: Se han realizado 3 intentos de reconexión. Deteniendo el cliente."
        );
        this.socket.destroy();
        this.socket.end();
      }
    }
  }

  read(buffer) {
    let responses = buffer.split("|");
    buffer = responses.pop();

    try {
      responses = responses.map(JSON.parse);

      responses.forEach((message) => {
        if (!this._PROMISES_.hasOwnProperty(message.id)) {
          return;
        }

        if (message.error) {
          this._PROMISES_[message.id].reject(message.data);
          delete this._PROMISES_[message.id];
          return;
        }

        this._PROMISES_[message.id].resolve(message.data);
        delete this._PROMISES_[message.id];
      });
    } catch (err) {
      console.error(buffer);
      console.error(err);
    }

    return buffer;
  }

  write(socket, id, data) {
    try {
      data = JSON.stringify({ id, data });
      socket.write(data + "|");
    } catch (err) {
      console.error(data);
      console.error(err);
    }
  }

  async task(socket, data) {
    const id = Date.now().toString();

    return new Promise( (resolve, reject) => {
      this._PROMISES_[id] = { resolve, reject };
      console.log("CLIENTE DE CONTACTOS: Enviando contacto y esperando confirmación...");
      this.write(socket, id, data);
    });
  }

  async _MAIN_(socket) {
    try {
      var result = await this.task(socket, {
        type: "setContacto",
        ip: this.self_opts.host,
        puerto: this.self_opts.port
      });
      console.log(result);
      
      setInterval(this.obtenerContactos(socket), 15000);  // Cada 15 segundos va a obtener la lista actualizada de contactos

    } catch (err) {
      console.error(err);
    }
  }

  async obtenerContactos(socket) {  // Se va a ejecutar periódicamente
    try {
      var result = await this.task(socket, {
        type: "getContactos"
      });
      console.log(result);
    } catch (err) {
      console.error(err);
    }
  }

}




//--------------------------------------------------------------------

class Cliente {
  constructor(self_ip, self_port) {
    this.reconexiones = 0;
    this.socket = null;
    this._PROMISES_ = {};
    this._CONTACTOS_ = {};
    this.self_ip = self_ip;
    this.self_port = self_port;
  }

  connectToServer(host, port) {
    this.socket = net.createConnection({host: host, port: port}, () => {
      this.reconexiones = 0;
      var buffer = "";

      this.socket.on("data", (chunk) => {
        buffer += chunk.toString();
        buffer = this.read(buffer);
      });

      this._MAIN_(this.socket);
      this.socket.destroy();
      this.socket.end();
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
  }

  actualizarContactos(data) {
    this._CONTACTOS_ = data;
    // this._CONTACTOS_ = this._CONTACTOS_.filter(contacto => contacto.ip !== this.self_ip && contacto.puerto !== this.self_port);
    this._CONTACTOS_ = this._CONTACTOS_.filter(contacto => contacto.puerto !== this.self_port); // Todas las IP son 127.0.0.1, por eso sacaba todos
    console.log("CLIENTE: Se actualizo la lista de contactos: ");
    console.log(this._CONTACTOS_);
    if (this._CONTACTOS_.length !== 0) {
      this._CONTACTOS_.forEach((contacto) => {
      this.connectToServer(contacto.ip, contacto.puerto);
    }
    )} else {
      console.log("CLIENTE: No hay nodos que saludar.")
    }
  }

  reconectar() {
    if (!this.socket || this.socket.destroyed) {
      // Verifica si no hay conexión existente
      if (this.reconexiones < 2) {
        console.log('CLIENTE: Intentando reconectar...');
        setTimeout(() => {
          this.reconexiones += 1;
          this.connectToServer();
        }, 5000);
      } else {
        console.log(
          "CLIENTE: Se han realizado 3 intentos de reconexión. Deteniendo el cliente."
        );
        this.socket.destroy();
        this.socket.end();
        //exit(1);
      }
    }
  }

  read(buffer) {
    let responses = buffer.split("|");
    buffer = responses.pop();

    try {
      responses = responses.map(JSON.parse);

      responses.forEach((message) => {
        if (!this._PROMISES_.hasOwnProperty(message.id)) {
          return;
        }

        if (message.error) {
          this._PROMISES_[message.id].reject(message.data);
          delete this._PROMISES_[message.id];
          return;
        }

        this._PROMISES_[message.id].resolve(message.data);
        delete this._PROMISES_[message.id];
      });
    } catch (err) {
      console.error(buffer);
      console.error(err);
    }

    return buffer;
  }

  write(socket, id, data) {
    try {
      data = JSON.stringify({ id, data });
      socket.write(data + "|");
    } catch (err) {
      console.error(data);
      console.error(err);
    }
  }

  async task(socket, data) {
    const id = Date.now().toString();

    return new Promise( (resolve, reject) => {
      this._PROMISES_[id] = { resolve, reject };
      console.log("CLIENTE: Enviando y esperando saludo...");
      this.write(socket, id, data);
    });
  }

  async _MAIN_(socket) {
    try {
      var result = await this.task(socket, {
        type: "saludo",
        data: "Hola",
      });

      console.log(result);
    } catch (err) {
      console.error(err);
    }
  }
}

function main() {
  // Obtener los argumentos de la línea de comandos:
  const args = process.argv.slice(2);

  // Verificar que se proporcionaron dos argumentos:
  if (args.length !== 1) {
    console.error(
      "Se requieren UN argumento con el formato <ip:puerto> para la dirección del servidor de contactos."
    );
    process.exit(1);
  }

  // Separar la dirección IP y el puerto de los argumentos:
  const args_servidor = args[0].split(":");

  // Verificar si la separación fue exitosa:
  if (args_servidor.length !== 2) {
    console.error("Los argumentos deben estar en el formato <ip:puerto>.");
    process.exit(1);
  }

  const ip = args_servidor[0]; // IP del servidor de contactos
  const puerto = args_servidor[1];

  const ip_host = "127.0.0.1";
  const puerto_host = Math.floor(Math.random() * (65535 - 1024 + 1)) + 1024;


  
  servidor = new Servidor(ip_host, puerto_host);
  cliente_de_contacto = new ClienteContactos(ip, puerto, ip_host, puerto_host);
  cliente = new Cliente(ip_host, puerto_host);
  servidor.setCliente(cliente);
  servidor.instanciateServer();
  cliente_de_contacto.connectToServer();
}

main();