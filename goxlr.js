const http = require("http");
const ws = require("ws"); //websocket
const fs = require("fs");
const pino = require("pino");
const PORT = 6805;
const logdir = require("os").homedir() + "\\Documents\\GoXLRPlugin\\logs";
//create logger that prints out to a file named server.log


const logger = pino(
  { level: process.env.LOG_LEVEL || "info" },
  pino.destination(logdir + "\\server.log")
);

/* fs.truncate(logdir + "\\server.log", 0, function () {
  console.log("file reset");
}); */

const changeprofile = require("./goxlrdocs/changeprofile.json");
const fetchprofiles = require("./goxlrdocs/fetchprofiles.json");
let connStatus = {
  'Client': false,
  'GoXLR': false,
};

let goXLRSocket;
let clientSocket; 

const { URL } = require("url");
const { json } = require("express");
const server = http.createServer();
// Set up a headless websocket server
const ws1 = new ws.Server({
  noServer: true
});

const ws2 = new ws.Server({ noServer: true });

//GoXLR socket
ws1.on("connection", (socket) => {
  goXLRSocket = socket;
  connStatus.GoXLR = true;
  logger.info("GoXLR Connected.");
  logger.info(connStatus + "sending to client")
  if(connStatus.Client == true) {
    clientSocket.send(JSON.stringify(connStatus))
  }
});

ws1.on("close", (socket) => {
  connStatus.goXLR = false;
  logger.info(connStatus);
  logger.info("GoXLR disconnected.");
});

ws2.on("connection", (socket) => {
  logger.info("Client connected")
  connStatus.Client = true;
  clientSocket = socket;
  socket.send(JSON.stringify(connStatus));
});

//Client websocket and emitting commands to GoXLRSocket based on received data
ws2.on("connection", (socket) => {
  logger.info("Client connected")
  connStatus.Client = true;
  clientSocket = socket;
  socket.send(JSON.stringify(connStatus));
  socket.on("message", (message) => {
    logger.info(message);
    switch (message.toLowerCase().substr(0, message.indexOf("="))) {
      case "fetchprofiles":
        logger.info("Got fetch message!");
        try {
          goXLRSocket.send(JSON.stringify(fetchprofiles));
          goXLRSocket.on("message", (xlrMessage) => {
            socket.send(JSON.stringify(xlrMessage));
          });
        } catch (err) {
          connStatus.goXLR = false;
          logger.error(
            "GoXLR not connected to websocket at ws://0.0.0.0:6805/?GoXLRApp"
          );
          logger.error(err);
        }
      case "changeprofile":
        logger.info("Got change profile message!");
        changeprofile.payload.settings.SelectedProfile = message.substr(
          message.indexOf("=") + 1
        );

        logger.info("Sending: " + JSON.stringify(changeprofile));
        try {
          goXLRSocket.send(JSON.stringify(changeprofile));
        } catch (err) {
          connStatus.goXLR = false;
          logger.error(
            "GoXLR not connected to websocket at ws://0.0.0.0:6805/?GoXLRApp"
          );
          break;
        }
        goXLRSocket.on("message", (xlrMessage) => {
          socket.send(JSON.stringify(xlrMessage));
        });

      case "verifyconnection":
        socket.send(JSON.stringify(connStatus));
        logger.info(connStatus);
    }
  });
});

ws2.on("close", (socket) => {
  connStatus.Client = false;
  socket.send(JSON.stringify(connStatus));
  logger.info(connStatus);
});

// `server` is a vanilla Node.js HTTP server, so use
// the same ws upgrade process described here:
// https://www.npmjs.com/package/ws#multiple-servers-sharing-a-single-https-server
server.on("upgrade", (request, socket, head) => {
  logger.info("Listening on: " + PORT);

  const pathname = request.url;
  if (pathname === "/?GOXLRApp") {
    ws1.handleUpgrade(request, socket, head, (socket) => {
      ws1.emit("connection", socket, request);
    });
  } else if (pathname === "/client") {
    ws2.handleUpgrade(request, socket, head, function done(ws) {
      ws2.emit("connection", ws, request);
    });
  }
});
server.listen(6805);



//catching exceptions and closing server if it crashes instead of a graceful exit.
process.on('uncaughtException', (err, origin) => server.close());
process.on('SIGTERM', (err, origin) => server.close());