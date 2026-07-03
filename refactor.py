import re
import sys

def modify_main():
    with open('electron/main.cjs', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add searchWindow
    if 'let searchWindow;' not in content:
        content = content.replace('let exoWindow;', 'let exoWindow;\nlet searchWindow;')
    
    window_create_block = """  searchWindow = new BrowserWindow({
    width: 350,
    height: 400,
    y: 100, // Below top
    x: 820, // Right of main window assuming main is centered? Let's just put it roughly on right
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });
  
  searchWindow.setAlwaysOnTop(true, 'screen-saver');
  
  if (isDev) {
    searchWindow.loadURL('http://localhost:5173/?mode=search');
  } else {
    searchWindow.loadFile(path.join(__dirname, '../dist/index.html'), { query: { mode: 'search' } });
  }"""
    
    if 'searchWindow = new BrowserWindow' not in content:
        content = content.replace('  if (isDev) {', window_create_block + '\n\n  if (isDev) {', 1)

    # Center it dynamically or just place it right of center
    # Wait, the main window is at Math.floor((width - 800) / 2)
    # So searchWindow x = Math.floor((width - 800) / 2) + 800 + 10 (margin)
    position_code = """
  // Position search window to the right of the main window
  searchWindow.setPosition(Math.floor((width - 800) / 2) + 800 + 10, 20);"""
    
    if 'searchWindow.setPosition' not in content:
        content = content.replace('mainWindow.setPosition(Math.floor((width - 800) / 2), 20);', 'mainWindow.setPosition(Math.floor((width - 800) / 2), 20);\n' + position_code)


    ipc_code = """
ipcMain.on('show-search-window', (event, data) => {
  if (searchWindow) {
    searchWindow.show();
    // Send data to the search window
    searchWindow.webContents.send('poi-results', data);
  }
});

ipcMain.on('hide-search-window', () => {
  if (searchWindow) {
    searchWindow.hide();
  }
});"""
    if 'show-search-window' not in content:
        content = content + '\n' + ipc_code

    with open('electron/main.cjs', 'w', encoding='utf-8') as f:
        f.write(content)

def modify_preload():
    with open('electron/preload.cjs', 'r', encoding='utf-8') as f:
        content = f.read()
    
    apis = """
  showSearchWindow: (results) => ipcRenderer.send('show-search-window', results),
  hideSearchWindow: () => ipcRenderer.send('hide-search-window'),
  onPoiResults: (callback) => {
    ipcRenderer.removeAllListeners('poi-results');
    ipcRenderer.on('poi-results', (event, data) => callback(data));
  },
  onFsdJump:"""
    content = content.replace('  onFsdJump:', apis)

    with open('electron/preload.cjs', 'w', encoding='utf-8') as f:
        f.write(content)

def modify_app():
    with open('src/App.tsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update searchCarriers to use IPC
    old_search = """      const data = await response.json();
      if (data && data.results) {
        setPoiResults(data.results.slice(0, 15).map((r: any) => ({
          name: r.name,
          system_name: r.system_name,
          distance: r.distance
        })));
      } else {
        setPoiResults([]);
      }
    } catch (err) {
      console.error(err);
      setStatusMessage('Failed to fetch carriers.');
      setPoiResults([]);
    } finally {
      setIsSearchingPoi(false);
    }"""
    
    new_search = """      const data = await response.json();
      if (data && data.results) {
        const results = data.results.slice(0, 15).map((r: any) => ({
          name: r.name,
          system_name: r.system_name,
          distance: r.distance
        }));
        if (window.electronAPI) window.electronAPI.showSearchWindow(results);
      } else {
        if (window.electronAPI) window.electronAPI.showSearchWindow([]);
      }
    } catch (err) {
      console.error(err);
      setStatusMessage('Failed to fetch carriers.');
    } finally {
      setIsSearchingPoi(false);
    }"""
    content = content.replace(old_search, new_search)

    # 2. Revert main window layout and move dropdown
    old_start = """  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: '1rem' }}>
      <div style={{ width: '400px', flexShrink: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
        <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
          <div className="flex justify-between items-center mb-2">
        <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
          Lighthouse <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>
        </h3>
        <button 
          onClick={() => setIsMinimized(true)} 
          onMouseEnter={enableMouse}
          onMouseLeave={disableMouse}
          title="Minimize"
          style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
        >
          -
        </button>
      </div>"""

    new_start = """  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
        <div className="flex justify-between items-center mb-2">
        <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
          Lighthouse <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>
        </h3>
        <div className="flex gap-2">
          <div style={{ position: 'relative' }} ref={searchRef}>
            <button 
              onClick={() => setPoiMenuOpen(!poiMenuOpen)} 
              onMouseEnter={enableMouse}
              onMouseLeave={disableMouse}
              title="Search POI" 
              style={{ fontSize: '0.8rem', padding: '0.2rem 0.4rem', pointerEvents: 'auto' }}
            >&#x1F50E;</button>
            {poiMenuOpen && (
              <div className="glass-panel" style={{ position: 'absolute', top: '100%', right: 0, marginTop: '0.2rem', padding: '0.5rem', background: 'rgba(20, 25, 35, 0.95)', border: '1px solid var(--accent-color)', borderRadius: '4px', zIndex: 100, minWidth: '150px' }}>
                <div 
                  onClick={() => { searchCarriers(); enableMouse(); }}
                  onMouseEnter={enableMouse}
                  onMouseLeave={disableMouse}
                  style={{ pointerEvents: 'auto', padding: '0.4rem', cursor: 'pointer', borderBottom: '1px solid rgba(255,255,255,0.1)', fontSize: '0.85rem' }}
                >
                  Nearby Fleet Carriers
                </div>
                <div 
                  style={{ padding: '0.4rem', color: 'var(--text-secondary)', fontSize: '0.85rem', fontStyle: 'italic' }}
                >
                  Scenic views (Soon)
                </div>
              </div>
            )}
          </div>
          <button 
            onClick={() => setIsMinimized(true)} 
            onMouseEnter={enableMouse}
            onMouseLeave={disableMouse}
            title="Minimize"
            style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
          >
            -
          </button>
        </div>
      </div>"""
    content = content.replace(old_start, new_start)

    # 3. Remove old dropdown from destination
    old_dest = """            <button 
              onClick={() => {
                if (window.electronAPI && destination) {
                  window.electronAPI.copyToClipboard(destination);
                  setStatusMessage('Copied Destination!');
                  setTimeout(() => setStatusMessage(''), 3000);
                }
              }} 
              title="Copy Destination"
            >&#x274F;</button>
            <div style={{ position: 'relative' }} ref={searchRef}>
              <button onClick={() => setPoiMenuOpen(!poiMenuOpen)} title="Search POI" style={{ height: '100%' }}>&#x2630;</button>
              {poiMenuOpen && (
                <div className="glass-panel" style={{ position: 'absolute', top: '100%', right: 0, marginTop: '0.2rem', padding: '0.5rem', background: 'rgba(20, 25, 35, 0.95)', border: '1px solid var(--accent-color)', borderRadius: '4px', zIndex: 100, minWidth: '150px' }}>
                  <div 
                    onClick={searchCarriers}
                    style={{ padding: '0.4rem', cursor: 'pointer', borderBottom: '1px solid rgba(255,255,255,0.1)', fontSize: '0.85rem' }}
                  >
                    Nearby Fleet Carriers
                  </div>
                  <div 
                    style={{ padding: '0.4rem', color: 'var(--text-secondary)', fontSize: '0.85rem', fontStyle: 'italic' }}
                    title="Scenic views search coming soon"
                  >
                    Scenic views (Soon)
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>"""
    new_dest = """            <button 
              onClick={() => {
                if (window.electronAPI && destination) {
                  window.electronAPI.copyToClipboard(destination);
                  setStatusMessage('Copied Destination!');
                  setTimeout(() => setStatusMessage(''), 3000);
                }
              }} 
              title="Copy Destination"
            >&#x274F;</button>
          </div>
        </div>
      </div>"""
    content = content.replace(old_dest, new_dest)

    # 4. Remove right panel and close divs correctly
    old_end = """      </div> {/* End left column */}

      {/* POI Search Results Right Panel */}
      {(isSearchingPoi || poiResults !== null) && (
        <div className="glass-panel" style={{ width: '350px', flexShrink: 0, maxHeight: '100%', overflowY: 'auto', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem', boxSizing: 'border-box' }}>
          <div className="flex justify-between items-center mb-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.3rem' }}>
            <h3 className="text-accent" style={{ fontWeight: 600, margin: 0, fontSize: '0.9rem' }}>NEARBY FLEET CARRIERS</h3>
            <button onClick={() => setPoiResults(null)} style={{ fontSize: '0.8rem', padding: '0.1rem 0.4rem', pointerEvents: 'auto' }}>X</button>
          </div>
          
          {isSearchingPoi && <div className="text-secondary" style={{ fontStyle: 'italic', fontSize: '0.85rem' }}>Searching Spansh...</div>}
          
          {!isSearchingPoi && poiResults && poiResults.length === 0 && (
            <div className="text-warning" style={{ fontSize: '0.85rem' }}>No Fleet Carriers found near {destination}.</div>
          )}

          {!isSearchingPoi && poiResults && poiResults.length > 0 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {poiResults.map((carrier, idx) => (
                <div key={idx} style={{ background: 'rgba(255,255,255,0.05)', padding: '0.4rem', borderRadius: '4px' }}>
                  <div className="text-accent" style={{ fontWeight: 'bold', fontSize: '0.85rem' }}>{carrier.name}</div>
                  <div className="flex justify-between items-center" style={{ fontSize: '0.75rem', marginTop: '0.2rem' }}>
                    <span className="text-secondary">{carrier.system_name}</span>
                    <span className="text-success">{carrier.distance.toFixed(2)} Ly</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

    </div>
  );
}

export default App;"""
    new_end = """    </div>
  );
}

export default App;"""
    
    content = content.replace(old_end, new_end)

    # 5. Add search Mode routing
    search_mode = """
  // ==== POI Search Results Mode ====
  if (mode === 'search') {
    return (
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', padding: '0' }}
           onMouseEnter={enableMouse} onMouseLeave={disableMouse}>
        <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem', overflowY: 'auto' }}>
          <div className="flex justify-between items-center mb-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.3rem', pointerEvents: 'auto' }}>
            <h3 className="text-accent" style={{ fontWeight: 600, margin: 0, fontSize: '0.9rem' }}>FLEET CARRIERS</h3>
            <button 
              onClick={() => window.electronAPI && window.electronAPI.hideSearchWindow()} 
              style={{ fontSize: '0.8rem', padding: '0.1rem 0.4rem' }}
            >
              X
            </button>
          </div>
          
          {(!poiResults) && (
            <div className="text-secondary" style={{ fontStyle: 'italic', fontSize: '0.85rem' }}>Loading results...</div>
          )}

          {poiResults && poiResults.length === 0 && (
            <div className="text-warning" style={{ fontSize: '0.85rem' }}>No Fleet Carriers found.</div>
          )}

          {poiResults && poiResults.length > 0 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', pointerEvents: 'auto' }}>
              {poiResults.map((carrier, idx) => (
                <div key={idx} style={{ background: 'rgba(255,255,255,0.05)', padding: '0.4rem', borderRadius: '4px' }}>
                  <div className="text-accent" style={{ fontWeight: 'bold', fontSize: '0.85rem' }}>{carrier.name}</div>
                  <div className="flex justify-between items-center" style={{ fontSize: '0.75rem', marginTop: '0.2rem' }}>
                    <span className="text-secondary">{carrier.system_name}</span>
                    <span className="text-success">{carrier.distance.toFixed(2)} Ly</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }"""
    
    # Needs to listen for `onPoiResults`
    state_setup = """  const searchRef = useRef<HTMLDivElement>(null);"""
    state_setup_new = """  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (mode === 'search' && window.electronAPI) {
      window.electronAPI.onPoiResults((data: any) => {
        setPoiResults(data);
      });
    }
  }, [mode]);"""
    content = content.replace(state_setup, state_setup_new)

    if "if (mode === 'search')" not in content:
        content = content.replace("  // ==== Exo-Tracker Mode ====", search_mode + "\n\n  // ==== Exo-Tracker Mode ====")

    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)

modify_main()
modify_preload()
modify_app()
print('Refactored architecture for detached search window')
