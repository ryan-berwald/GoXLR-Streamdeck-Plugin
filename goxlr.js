const express = require('express'); //endpoint
const ws = require('ws'); //websocket
const fs = require('fs'); //read file sys

const changeprofile = require('./changeprofile.json');
const goxlrJson = require('./goxlr.json');

const {
  URL
} = require('url');
const app = express();
// Set up a headless websocket server that prints any
// events that come in.
const wsServer = new ws.Server({
  noServer: true
});
wsServer.on('connection', (socket) => {
  console.log('someone connected');
  socket.send(JSON.stringify(changeprofile));
  socket.on('message', (message) => 
  {
    switch (message.toLowerCase()){
      case 'fetchprofiles':
        socket.send(JSON.stringify(goxlrJson));
    }
    console.log(message);
  });

});
// `server` is a vanilla Node.js HTTP server, so use
// the same ws upgrade process described here:
// https://www.npmjs.com/package/ws#multiple-servers-sharing-a-single-https-server
const server = app.listen(6805);
server.on('upgrade', (request, socket, head) => {
  const pathname = request.url;
  if (pathname === '/?GOXLRApp') {
    wsServer.handleUpgrade(request, socket, head, (socket) => {
      wsServer.emit('connection', socket, request);
    });
  }
});

/* fs.readdir("C:\\Users\\rberw\\Documents\\goxlr", (err, files) => {
  files.forEach(file => {
    console.log(file);
  });
}); */

