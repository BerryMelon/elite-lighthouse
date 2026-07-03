import os

with open('electron/main.cjs', 'r', encoding='utf-8') as f:
    content = f.read()

hydration_logic = """
ipcMain.handle('hydrate-exo', async () => {
  const latestFile = getLatestJournal();
  if (!latestFile) return null;
  try {
    const lines = fs.readFileSync(latestFile, 'utf8').split('\\n').filter(l => l.trim().length > 0);
    
    let isLanded = false;
    let bioState = null;
    let currentBody = '';
    
    // Process forward to reconstruct the exact state
    for (const line of lines) {
      try {
        const event = JSON.parse(line);
        
        if (event.event === 'FSDJump' || event.event === 'SupercruiseEntry' || event.event === 'LeaveBody') {
          isLanded = false;
        } else if (event.event === 'Touchdown') {
          isLanded = true;
          currentBody = event.Body;
        } else if (event.event === 'FSSBodySignals' || event.event === 'SAASignalsFound') {
          const bioSignal = event.Signals && event.Signals.find(s => s.Type === 'Biological' || s.Type === '$SAA_SignalType_Biological;');
          if (bioSignal && bioSignal.Count > 0) {
            bioState = {
              bodyName: event.BodyName,
              totalSignals: bioSignal.Count,
              scanned: {}
            };
          }
        } else if (event.event === 'ScanOrganic') {
          if (!bioState) {
            bioState = { bodyName: 'Unknown Planet', totalSignals: 1, scanned: {} };
          }
          const species = event.Species_Localised || event.Species || 'Unknown';
          const count = event.ScanType === 'Log' ? 1 : event.ScanType === 'Sample' ? 2 : 3;
          bioState.scanned[species] = count;
        }
      } catch (e) {}
    }
    
    if (isLanded && exoWindow) {
      exoWindow.show();
    }
    
    return { isLanded, bioState };
  } catch(e) {
    return null;
  }
});
"""

if "hydrate-exo" not in content:
    content += '\n' + hydration_logic
    with open('electron/main.cjs', 'w', encoding='utf-8') as f:
        f.write(content)

with open('electron/preload.cjs', 'r', encoding='utf-8') as f:
    preload = f.read()

if "hydrateExo:" not in preload:
    preload = preload.replace("getCurrentLocation: () => ipcRenderer.invoke('get-current-location'),", "getCurrentLocation: () => ipcRenderer.invoke('get-current-location'),\n  hydrateExo: () => ipcRenderer.invoke('hydrate-exo'),")
    with open('electron/preload.cjs', 'w', encoding='utf-8') as f:
        f.write(preload)

print('Hydration logic added!')
