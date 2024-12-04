const net = require("net");

const opts = {
  host: "35.185.42.7",
  port: 8001,
};

const socket = net.createConnection(opts, () => {
  var buffer = "";

  socket.on("data", (chunk) => {
    buffer += chunk.toString(); // Cada ves que llega data, se concatena en el buffer el chunk de datos.
    buffer = read(buffer); // Se llama a la función read para que obtenga los datos que estén antes de un "separador", deja en el buffer el resto
  });

  _MAIN_(socket);
});

socket.on("end", () => {
  console.log("Desconectado del server");
});

socket.on("error", (err) => {
  if (err.code === "ECONNREFUSED") {
    console.log("El servidor está cerrado");
  } else {
    console.error(err);
  }
});

// --------------------------------------------------------

const _PROMISES_ = {};

function read(buffer) {
  let responses = buffer.split("|"); // Separo por "|"
  buffer = responses.pop(); // Dejo en buffer solo lo que llegó luego de último "|"

  try {
    responses = responses.map(JSON.parse); // Deserealizamos cada respuesta

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

// --------------------------------------------------------
