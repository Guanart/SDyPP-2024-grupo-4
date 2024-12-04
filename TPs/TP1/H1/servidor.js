const net = require("net");

// { id: integer, data: {Object}}
const PORT = 8001;
const _PROTOCOLO_ = {
  saludo: function (socket, id, data) {
    setTimeout(() => {
      console.log("Respondiendo saludo...");
      write(socket, id, { message: "Hola!" }, null);
    }, 3000);
  },
};

const server = net.createServer((socket) => {
  var buffer = "";

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

server.listen(PORT, () => {
  console.log("Server ready.");
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
