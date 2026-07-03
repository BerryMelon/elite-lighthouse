const { app, BrowserWindow, ipcMain, clipboard } = require('electron');
const path = require('path');
const fs = require('fs');

const isDev = process.env.NODE_ENV !== 'production';

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 300,
    y: 20, // Top of screen
    x: undefined, // center horizontally if x is not defined? Actually we can center it later
    frame: false, // frameless
    transparent: true,
    alwaysOnTop: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Center horizontally at the top
  const { width } = require('electron').screen.getPrimaryDisplay().workAreaSize;
  mainWindow.setPosition(Math.floor((width - 800) / 2), 20);
  
  // Force the window to stay above fullscreen/borderless games
  mainWindow.setAlwaysOnTop(true, 'screen-saver');

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // Make the window ignore mouse events if we only want a pure HUD, 
  // but we need to click buttons for the main interface. 
  // We can toggle this from the renderer later.
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

const home = require('os').homedir();
const journalDir = path.join(home, 'Saved Games', 'Frontier Developments', 'Elite Dangerous');

function getLatestJournal() {
  if (!fs.existsSync(journalDir)) return null;
  const files = fs.readdirSync(journalDir).filter(f => f.startsWith('Journal.') && f.endsWith('.01.log'));
  if (files.length === 0) return null;
  files.sort();
  return path.join(journalDir, files[files.length - 1]);
}

ipcMain.handle('get-current-location', async () => {
  const latestFile = getLatestJournal();
  if (!latestFile) return { error: 'Journal directory or files not found' };

  try {
    const content = fs.readFileSync(latestFile, 'utf8');
    const lines = content.split('\n').filter(l => l.trim().length > 0);
    
    // Read backwards to find the last known location
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const event = JSON.parse(lines[i]);
        if (event.event === 'Location' || event.event === 'FSDJump') {
          return { system: event.StarSystem, pos: event.StarPos };
        }
      } catch (e) {}
    }
  } catch (err) {
    return { error: 'Error reading journal' };
  }
  return { error: 'Location not found' };
});

// Watch the journal for new FSDJump events
let currentWatcher = null;
let lastSize = 0;

function watchLatestJournal() {
  const latestFile = getLatestJournal();
  if (!latestFile) return;

  if (currentWatcher) currentWatcher.close();

  lastSize = fs.statSync(latestFile).size;

  currentWatcher = fs.watch(latestFile, (eventType) => {
    if (eventType === 'change') {
      const stats = fs.statSync(latestFile);
      if (stats.size > lastSize) {
        // Read the new chunk
        const stream = fs.createReadStream(latestFile, { start: lastSize, end: stats.size });
        stream.on('data', (chunk) => {
          const lines = chunk.toString().split('\n').filter(l => l.trim().length > 0);
          for (const line of lines) {
            try {
              const event = JSON.parse(line);
              if (event.event === 'FSDJump') {
                if (mainWindow) {
                  mainWindow.webContents.send('fsd-jump', event);
                }
              }
            } catch(e) {}
          }
        });
        lastSize = stats.size;
      }
    }
  });
}

// Check for new journal files being created
if (fs.existsSync(journalDir)) {
  fs.watch(journalDir, (eventType, filename) => {
    if (filename && filename.startsWith('Journal.') && filename.endsWith('.01.log')) {
      watchLatestJournal();
    }
  });
  watchLatestJournal();
}

ipcMain.on('copy-to-clipboard', (event, text) => {
  clipboard.writeText(text);
});

// To toggle ignore mouse events (HUD mode)
ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  if (win) {
    win.setIgnoreMouseEvents(ignore, options);
  }
});

// Proxy fetch requests to bypass CORS in the renderer
ipcMain.handle('fetch-proxy', async (event, url, options) => {
  try {
    const res = await fetch(url, options);
    const data = await res.json();
    return { data, status: res.status };
  } catch (err) {
    return { error: err.message };
  }
});
