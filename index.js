const { app, BrowserWindow } = require("electron");
var exec = require("child_process").exec;

function Callback(err, stdout, stderr) {
  if (err) {
    console.log(`exec error: ${err}`);
    return;
  } else {
    console.log(`${stdout}`);
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 786,
    resizable: false,
    webPreferences: {
      nodeIntegration: true,
    },
  });
  res = exec("gunicorn backend.wsgi:server", Callback);
  win.loadURL("http://127.0.0.1:8000");
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
