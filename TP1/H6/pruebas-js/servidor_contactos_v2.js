const net = require("net");

class Servidor {
  constructor(host, port) {
    this.opts = {
      host: host,
      port: port,
    };
    this.server = null;
    this.cliente = null;
    this._CONTACTOS_ = [];
  }

  setCliente(cliente){
    this.cliente = cliente
  }

  setContactos() {
    this.cliente.setContactos(this._CONTACTOS_);
  }

  _PROTOCOLO_ = {
    setContacto: (socket, id, data) => {
      // Envía mensaje de recibido:
      this.write(socket, id, {message: "Recibido"}, null);
      // Registra nodo y envía a todos los contactos en _CONTACTOS_ la lista actualizada (hace broadcast)
      this._CONTACTOS_.push({ ip: data.ip, puerto: data.puerto }); // Agrego a la lista de contactos este nodo
      this._CONTACTOS_.forEach((contacto) => {
        this.setContactos();
        this.cliente.connectToServer(contacto.ip, contacto.puerto);
      });
      
    }
  }

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

class Cliente {
  constructor() {
    this.reconexiones = 0;
    this.socket = null;
    this._CONTACTOS_ = [];
  }

  setContactos (contactos) {
    this._CONTACTOS_ = contactos;
  }
  
  connectToServer(host, port) {
    this.socket = net.createConnection({ host: host, port: port }, () => {
      this.reconexiones = 0;
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
        console.log('Intentando reconectar...');
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
    this.write(socket, 0, data);
  }

  async _MAIN_(socket) {
    try {
      await this.task(socket, {
        type: "actualizarContactos",
        data: this._CONTACTOS_
      });
      console.log("Lista enviada");
    } catch (err) {
      console.error(err);
    }
  }
}

//--------------------------------------------------------------------

function main() {
  servidor = new Servidor("127.0.0.1", 8000);
  cliente = new Cliente();
  servidor.setCliente(cliente);
  servidor.instanciateServer();
}

main();