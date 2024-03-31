const net = require("net");

const opts = {
  host: "35.185.42.7",
  port: 8002,
};

let reconexiones = 0;

function callback() {
  reconexiones = 0;
  var buffer = "";

  socket.on("data", (chunk) => {
    buffer += chunk.toString();
    buffer = read(buffer);
  });

  _MAIN_(socket);
}

let socket;

function connect() {
  socket = net.createConnection(opts, callback);
  socket.on("end", () => {
    console.log("Desconectado del server");
    reconectar();
  });

  socket.on("error", (err) => {
    if (err.code === "ECONNRESET") {
      console.log("El servidor cerró de forma abrupta");
      reconectar();
    } else if (err.code === "ECONNREFUSED") {
      console.log("El servidor está cerrado");
      reconectar();
    } else {
      console.error(err);
    }
  });
}

function reconectar() {
  if (reconexiones < 3) {
    console.log("Intentando reconectar...");
    setTimeout(() => {
      reconexiones += 1;
      connect();
    }, 5000);
  } else {
    console.log(
      "Se han realizado 3 intentos de reconexión. Deteniendo el cliente."
    );
    socket.destroy();
  }
}

connect();

const _PROMISES_ = {};

function read(buffer) {
  let responses = buffer.split("|");
  buffer = responses.pop();

  try {
    responses = responses.map(JSON.parse);

    responses.forEach((message) => {
      if (!_PROMISES_.hasOwnProperty(message.id)) {
        return;
      }

      if (message.error) {
        _PROMISES_[message.id].reject(message.data);
        delete _PROMISES_[message.id];
        return;
      }

      _PROMISES_[message.id].resolve(message.data);
      delete _PROMISES_[message.id];
    });
  } catch (err) {
    console.error(buffer);
    console.error(err);
  }

  return buffer;
}

function write(socket, id, data) {
  try {
    data = JSON.stringify({ id, data });
    socket.write(data + "|");
  } catch (err) {
    console.error(data);
    console.error(err);
  }
}

// --------------------------------------------------------

async function task(socket, data) {
  const id = Date.now().toString();

  return new Promise(function (resolve, reject) {
    _PROMISES_[id] = { resolve, reject };
    console.log("Enviando y esperando saludo...");
    write(socket, id, data);
  });
}

// --------------------------------------------------------

async function _MAIN_(socket) {
  try {
    var result = await task(socket, {
      type: "saludo",
      data: "Hola",
    });

    console.log(result);
  } catch (err) {
    console.error(err);
  }
}
