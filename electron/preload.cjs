const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getCurrentLocation: () => ipcRenderer.invoke('get-current-location'),
  hydrateExo: () => ipcRenderer.invoke('hydrate-exo'),
  copyToClipboard: (text) => ipcRenderer.send('copy-to-clipboard', text),
  setIgnoreMouseEvents: (ignore, options) => ipcRenderer.send('set-ignore-mouse-events', ignore, options),
  fetchProxy: (url, options) => ipcRenderer.invoke('fetch-proxy', url, options),
  onPoiResults: (callback) => {
    ipcRenderer.removeAllListeners('poi-results');
    ipcRenderer.on('poi-results', (event, data) => callback(data));
  },
  onFsdJump: (callback) => {
    ipcRenderer.removeAllListeners('fsd-jump');
    ipcRenderer.on('fsd-jump', (event, data) => callback(data));
  },
  onJournalEvent: (callback) => {
    ipcRenderer.removeAllListeners('journal-event');
    ipcRenderer.on('journal-event', (event, data) => callback(data));
  },
  onRealtimeHvt: (callback) => {
    ipcRenderer.removeAllListeners('realtime-hvt');
    ipcRenderer.on('realtime-hvt', (event, data) => callback(data));
  }
});
