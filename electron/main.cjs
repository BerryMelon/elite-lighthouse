const { app, BrowserWindow, ipcMain, clipboard } = require('electron');
const path = require('path');
const fs = require('fs');

const isDev = !app.isPackaged;

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

function getRecentJournals(count=5) {
  if (!fs.existsSync(journalDir)) return [];
  const files = fs.readdirSync(journalDir).filter(f => f.startsWith('Journal.') && f.endsWith('.01.log'));
  if (files.length === 0) return [];
  files.sort();
  return files.slice(-count).map(f => path.join(journalDir, f));
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
let fssTracker = {};

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
              
              const relevantEvents = [
                'FSDJump', 'Scan', 'ScanOrganic', 'Touchdown', 'LeaveBody', 
                'SupercruiseEntry', 'FSSBodySignals', 'SAASignalsFound'
              ];
              
              if (relevantEvents.includes(event.event)) {
                
                // Track FSS data for HVT alerts
                if (event.event === 'FSDJump') {
                  fssTracker = {}; // reset on jump
                } else if (event.event === 'Scan' && event.BodyName && event.PlanetClass) {
                  if (!fssTracker[event.BodyName]) fssTracker[event.BodyName] = {};
                  fssTracker[event.BodyName].planetClass = event.PlanetClass;
                } else if (event.event === 'FSSBodySignals' && event.BodyName) {
                  if (!fssTracker[event.BodyName]) fssTracker[event.BodyName] = {};
                  const bioSignal = event.Signals && event.Signals.find(s => s.Type === 'Biological' || s.Type === '$SAA_SignalType_Biological;');
                  if (bioSignal) {
                    fssTracker[event.BodyName].bioCount = bioSignal.Count;
                  }
                }

                // Check for HVT if we have FSS data
                if (event.BodyName && fssTracker[event.BodyName] && !fssTracker[event.BodyName].hvtAlerted) {
                  const body = fssTracker[event.BodyName];
                  let isHvt = false;
                  let hvtMessage = "";
                  
                  if (body.planetClass) {
                    const pc = body.planetClass.toLowerCase();
                    if (pc === 'earthlike body') {
                      isHvt = true; hvtMessage = "Earth-Like World Candidate";
                    } else if (pc === 'ammonia world') {
                      isHvt = true; hvtMessage = "Ammonia World Candidate";
                    } else if (pc === 'water world') {
                      isHvt = true; hvtMessage = "Water World Candidate";
                    } else if (pc === 'high metal content body' && body.bioCount === 1) {
                      isHvt = true; hvtMessage = "Stratum Tectonicas Candidate (1 Bio)";
                    }
                  }

                  if (!isHvt && body.bioCount >= 5) {
                    isHvt = true;
                    hvtMessage = `High Bio Diversity (${body.bioCount} Signals)`;
                  }

                  if (isHvt) {
                    fssTracker[event.BodyName].hvtAlerted = true;
                    BrowserWindow.getAllWindows().forEach(win => {
                      win.webContents.send('realtime-hvt', {
                        bodyName: event.BodyName,
                        message: hvtMessage
                      });
                    });
                  }
                }

                BrowserWindow.getAllWindows().forEach(win => {
                  win.webContents.send('journal-event', event);
                  if (event.event === 'FSDJump') {
                    win.webContents.send('fsd-jump', event);
                  }
                });
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


ipcMain.handle('hydrate-exo', async () => {
  const recentFiles = getRecentJournals(5);
  if (recentFiles.length === 0) return null;
  try {
    let isLanded = false;
    let bioState = null;
    let currentBody = '';
    
    // Process forward across up to 5 latest files to reconstruct the exact state
    for (const file of recentFiles) {
      const lines = fs.readFileSync(file, 'utf8').split('\n').filter(l => l.trim().length > 0);
      for (const line of lines) {
      try {
        const event = JSON.parse(line);
        
        if (event.event === 'FSDJump' || event.event === 'SupercruiseEntry' || event.event === 'LeaveBody') {
          isLanded = false;
          bioState = null;
        } else if (event.event === 'Touchdown') {
          isLanded = true;
          currentBody = event.Body;
        } else if (event.event === 'FSSBodySignals' || event.event === 'SAASignalsFound') {
          const bioSignal = event.Signals && event.Signals.find(s => s.Type === 'Biological' || s.Type === '$SAA_SignalType_Biological;');
          if (bioSignal && bioSignal.Count > 0) {
            if (bioState && bioState.bodyName === event.BodyName) {
              bioState.totalSignals = bioSignal.Count;
            } else {
              bioState = {
                bodyName: event.BodyName,
                totalSignals: bioSignal.Count,
                scanned: {}
              };
            }
          }
        } else if (event.event === 'ScanOrganic') {
          if (!bioState) {
            bioState = { bodyName: 'Unknown Planet', totalSignals: 1, scanned: {} };
          }
          const species = event.Species_Localised || event.Species || 'Unknown';
          
          if (bioState.scanned[species] === undefined) {
            bioState.scanned[species] = 0;
          }
          
          if (event.ScanType === 'Log' || event.ScanType === 'Sample') {
            bioState.scanned[species] += 1;
            if (bioState.scanned[species] > 2) bioState.scanned[species] = 2;
          } else if (event.ScanType === 'Analyse' || event.ScanType === 'Analyze') {
            bioState.scanned[species] = 3;
          }
        } else if (event.event === 'Location') {
          if (event.Latitude !== undefined && event.Longitude !== undefined && !event.Docked) {
            isLanded = true;
          }
        }
      } catch (e) {}
    }
  }
    
  return { isLanded, bioState };
  } catch(e) {
    return null;
  }
});

ipcMain.handle('hydrate-stats', async () => {
  const recentFiles = getRecentJournals(30).reverse(); // newest to oldest
  let jumps = 0;
  let planetsScanned = new Set();
  let biosScanned = 0;
  let currentPos = null;
  let dockFound = false;

  for (const file of recentFiles) {
    if (dockFound) break;
    try {
      const lines = fs.readFileSync(file, 'utf8').split('\n').filter(l => l.trim().length > 0);
      for (let i = lines.length - 1; i >= 0; i--) {
        try {
          const event = JSON.parse(lines[i]);
          
          if (event.event === 'Docked' && event.StationType !== 'FleetCarrier' && event.StationType !== 'MegaShip') {
            dockFound = true;
            break;
          }
          
          if (event.event === 'FSDJump') {
            jumps++;
          } else if (event.event === 'Scan' && event.PlanetClass && event.BodyName) {
            planetsScanned.add(event.BodyName);
          } else if (event.event === 'ScanOrganic' && (event.ScanType === 'Analyse' || event.ScanType === 'Analyze')) {
            biosScanned++;
          }
          
          if (!currentPos && (event.event === 'Location' || event.event === 'FSDJump') && event.StarPos) {
             currentPos = event.StarPos;
          }
        } catch(e) {}
      }
    } catch(err) {}
  }

  let distToSol = 0;
  if (currentPos) {
    distToSol = Math.sqrt(currentPos[0]*currentPos[0] + currentPos[1]*currentPos[1] + currentPos[2]*currentPos[2]);
  }

  return {
    jumps,
    planetsScanned: planetsScanned.size,
    biosScanned,
    distanceToSol: distToSol.toFixed(2)
  };
});



