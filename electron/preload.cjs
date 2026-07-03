const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getCurrentLocation: () => ipcRenderer.invoke('get-current-location'),
  copyToClipboard: (text) => ipcRenderer.send('copy-to-clipboard', text),
  setIgnoreMouseEvents: (ignore, options) => ipcRenderer.send('set-ignore-mouse-events', ignore, options),
  fetchProxy: (url, options) => ipcRenderer.invoke('fetch-proxy', url, options),
  onFsdJump: (callback) => {
    ipcRenderer.on('fsd-jump', (event, data) => callback(data));
  }
});
