const net = require("net");

class Servidor {
  constructor(host, port) {
    this.opts = {
      host: host,
      port: port,
    };
    this.server = null;
  }

  _PROTOCOLO_ = {
    saludo: (socket, id, data) => {
      setTimeout(() => {
        console.log("HOST: Respondiendo saludo...");
        this.write(socket, id, { message: "Hola!" }, null);
      }, 5000);
    },
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
    console.dir(message, { depth: null });

    if (!this._PROTOCOLO_.hasOwnProperty(message.data.type)) {
      console.error("HOST: Tipo de mensaje no reconocido");
      console.error(message);
      socket.end();
      return;
    }

    try {
      this._PROTOCOLO_[message.data.type](
        socket,
        message.id,
        message.data.data
      );
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
  constructor(host, port) {
    this.opts = {
      host: host,
      port: port,
    };
    this.socket = null;
    this._PROMISES_ = {};
  }

  connectToServer() {
    this.socket = net.createConnection(this.opts, () => {
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
    console.log("CLIENTE: Intentando reconectar...");
    setTimeout(() => {
      this.connectToServer();
    }, 5000);
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
      this.socket.write(data + "|");
    } catch (err) {
      console.error(data);
      console.error(err);
    }
  }

  async task(socket, data) {
    const id = Date.now().toString();

    return new Promise((resolve, reject) => {
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
  if (args.length !== 2) {
    console.error(
      "Se requieren dos argumentos en el formato <ip:puerto> para la dirección del servidor y del cliente."
      );
      console.log("Argumentos:")
      console.log(args);
    process.exit(1);
  }

  // Separar la dirección IP y el puerto de los argumentos:
  const args_servidor = args[0].split(":");
  const args_cliente = args[1].split(":");

  // Verificar si la separación fue exitosa:
  if (args_servidor.length !== 2 || args_cliente.length !== 2) {
    console.error("Los argumentos deben estar en el formato <ip:puerto>.");
    process.exit(1);
  }

  const ip_listening = args_servidor[0]; // IP de la interfaz donde escuchará el servidor
  const port_listening = args_servidor[1];
  const ip_to_connect = args_cliente[0]; // IP del servidor a conectarse
  const port_to_connect = args_cliente[1];

  cliente = new Cliente(ip_to_connect, port_to_connect);
  servidor = new Servidor(ip_listening, port_listening);
  servidor.instanciateServer();
  cliente.connectToServer();
}

main();
