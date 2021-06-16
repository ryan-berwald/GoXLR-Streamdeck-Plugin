const { app, BrowserWindow } = require('electron');


const path = require('path')

function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
          preload: path.join(__dirname, 'preload.js')
        }
      })
    
      win.loadURL('http://localhost:3000')
    }

  app.whenReady().then(() => {
    createWindow()
  });

  app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
  });