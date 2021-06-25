const express = require("express"); //endpoint
const ws = require("ws"); //websocket
const fs = require("fs"); //read file sys

const changeprofile = require("./goxlrdocs/changeprofile.json");
const fetchprofiles = require("./goxlrdocs/fetchprofiles.json");

let goXLRSocket;

const { URL } = require("url");
const app = express();
// Set up a headless websocket server that prints any
// events that come in.
const wsServer = new ws.Server({
  noServer: true,
});

const wss2 = new ws.Server({ noServer: true });

//Command emmitter to GoXLR
wsServer.on("connection", (socket) => {
  goXLRSocket = socket;
  console.log("GoXLR Connected!");
});

//Client websocket
wss2.on("connection", (socket) => {
  console.log("Client Connected!");
  socket.on("message", (message) => {
    console.log(message.toLowerCase().substr(0, message.indexOf("=")));
    switch (message.toLowerCase().substr(0, message.indexOf("="))) {
      case "fetchprofiles":
        console.log("Got fetch message!");
        goXLRSocket.send(JSON.stringify(fetchprofiles));
        goXLRSocket.on("message", (xlrMessage) => {
          socket.send(JSON.stringify(xlrMessage));
        });
      case "changeprofile":
        console.log("Got change profile message!");
        changeprofile.payload.settings.SelectedProfile = message.substr(
          message.indexOf("=") + 1
        );

        console.log("Sending: " + JSON.stringify(changeprofile));
        goXLRSocket.send(JSON.stringify(changeprofile));
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
const server = app.listen(6805);
server.on("upgrade", (request, socket, head) => {
  const pathname = request.url;
  if (pathname === "/?GOXLRApp") {
    wsServer.handleUpgrade(request, socket, head, (socket) => {
      wsServer.emit("connection", socket, request);
    });
  } else if (pathname === "/client") {
    wss2.handleUpgrade(request, socket, head, function done(ws) {
      wss2.emit("connection", ws, request);
    });
  }
});

const homedir = require('os').homedir();
console.log(homedir);
fs.readdir(`${homedir}\\Documents\\goxlr\\profiles`, (err, files) => {
  files.forEach((file) => {
    console.log(file);
  });
});

console.log(server.address());
