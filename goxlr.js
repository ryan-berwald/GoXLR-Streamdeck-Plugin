const express = require("express"); //endpoint
const ws = require("ws"); //websocket
const http = require("http");
const pino = require("pino");

//create logger that prints out to a file named server.log
const logger = pino(
  { level: process.env.LOG_LEVEL || "info" },
  pino.destination("./logs/server.log")
);

const changeprofile = require("./goxlrdocs/changeprofile.json");
const fetchprofiles = require("./goxlrdocs/fetchprofiles.json");

let goXLRSocket;

const server = http.createServer();
// Set up a headless websocket server
const ws1 = new ws.Server({
  noServer: true,
});

const ws2 = new ws.Server({
  noServer: true,
});

//Command emmitter to GoXLR
ws1.on("connection", (socket) => {
  goXLRSocket = socket;
  logger.info("GoXLR Connected.");
});

//Client websocket
ws2.on("connection", (socket) => {
  logger.info("Client Connected!");
  socket.on("message", (message) => {
    logger.info(message);
    switch (message.toLowerCase().substr(0, message.indexOf("="))) {
      case "fetchprofiles":
        logger.info("Got fetch message!");
        try {
          goXLRSocket.send(JSON.stringify(fetchprofiles));
        } catch (err) {
          logger.error(
            "GoXLR not connected to websocket at ws://0.0.0.0:6805/?GoXLRApp"
          );
          logger.error(err);
        }
        goXLRSocket.on("message", (xlrMessage) => {
          socket.send(JSON.stringify(xlrMessage));
        });
      case "changeprofile":
        logger.info("Got change profile message!");
        changeprofile.payload.settings.SelectedProfile = message.substr(
          message.indexOf("=") + 1
        );

        logger.info("Sending: " + JSON.stringify(changeprofile));
        try {
          goXLRSocket.send(JSON.stringify(changeprofile));
        } catch (err) {
          logger.error(
            "GoXLR not connected to websocket at ws://0.0.0.0:6805/?GoXLRApp"
          );
          logger.error(err);
          break;
        }
        goXLRSocket.on("message", (xlrMessage) => {
          console.log("received: " + xlrMessage);
          socket.send(JSON.stringify(xlrMessage));
        });
    }
  });
});

// `server` is a vanilla Node.js HTTP server, so use
// the same ws upgrade process described here:
// https://www.npmjs.com/package/ws#multiple-servers-sharing-a-single-https-server
server.on("upgrade", (request, socket, head) => {
  console.log("Started");
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
