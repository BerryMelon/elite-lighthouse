with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the bad block from the top
bad_block = """  const isExoMode = new URLSearchParams(window.location.search).get('mode') === 'exo';

  useEffect(() => {
    if (isExoMode && window.electronAPI) {
      window.electronAPI.hydrateExo().then((res: any) => {
        if (res && res.bioState) {
          setCurrentPlanetBio(res.bioState);
        }
      });
    }
  }, [isExoMode]);


  if (isExoMode) {
    if (!currentPlanetBio) {
      return (
        <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ color: 'var(--text-secondary)' }}>Waiting for surface scan...</div>
        </div>
      );
    }
    return (
      <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="flex justify-between items-center mb-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 'bold' }}>
            EXO-TRACKER
          </div>
          <div className="text-accent" style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
            {currentPlanetBio.bodyName}
          </div>
        </div>
        <div className="flex" style={{ flexWrap: 'wrap', gap: '1rem', overflowY: 'auto' }}>
          {Array.from({ length: Math.max(currentPlanetBio.totalSignals, Object.keys(currentPlanetBio.scanned).length) }).map((_, i) => {
             const scannedKeys = Object.keys(currentPlanetBio.scanned);
             if (i < scannedKeys.length) {
               const species = scannedKeys[i];
               const count = currentPlanetBio.scanned[species];
               const isComplete = count >= 3;
               return (
                 <div key={i} className={isComplete ? "text-success" : "text-accent"} style={{ fontSize: '0.9rem', flex: '1 1 45%' }}>
                   {isComplete ? `✓ ${species}` : `🧬 ${species} (${count}/3)`}
                 </div>
               );
             } else {
               return (
                 <div key={i} className="text-secondary" style={{ fontSize: '0.9rem', flex: '1 1 45%' }}>
                   ? Unknown Bio Signal
                 </div>
               );
             }
          })}
        </div>
      </div>
    );
  }"""

if bad_block in content:
    content = content.replace(bad_block, "")
else:
    print("WARNING: Could not find exact bad block, check manually.")

# 2. Add it back safely right before the render sections
safe_block = """  const isExoMode = new URLSearchParams(window.location.search).get('mode') === 'exo';

  useEffect(() => {
    if (isExoMode && window.electronAPI) {
      window.electronAPI.hydrateExo().then((res: any) => {
        if (res && res.bioState) {
          setCurrentPlanetBio(res.bioState);
        }
      });
    }
  }, [isExoMode]);

  if (isExoMode) {
    if (!currentPlanetBio) {
      return (
        <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ color: 'var(--text-secondary)' }}>Waiting for surface scan...</div>
        </div>
      );
    }
    return (
      <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="flex justify-between items-center mb-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 'bold' }}>
            EXO-TRACKER
          </div>
          <div className="text-accent" style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
            {currentPlanetBio.bodyName}
          </div>
        </div>
        <div className="flex" style={{ flexWrap: 'wrap', gap: '1rem', overflowY: 'auto' }}>
          {Array.from({ length: Math.max(currentPlanetBio.totalSignals, Object.keys(currentPlanetBio.scanned).length) }).map((_, i) => {
             const scannedKeys = Object.keys(currentPlanetBio.scanned);
             if (i < scannedKeys.length) {
               const species = scannedKeys[i];
               const count = currentPlanetBio.scanned[species];
               const isComplete = count >= 3;
               return (
                 <div key={i} className={isComplete ? "text-success" : "text-accent"} style={{ fontSize: '0.9rem', flex: '1 1 45%' }}>
                   {isComplete ? `✓ ${species}` : `🧬 ${species} (${count}/3)`}
                 </div>
               );
             } else {
               return (
                 <div key={i} className="text-secondary" style={{ fontSize: '0.9rem', flex: '1 1 45%' }}>
                   ? Unknown Bio Signal
                 </div>
               );
             }
          })}
        </div>
      </div>
    );
  }
"""

anchor = "  if (hudMode && route.length > 0) {"
if anchor in content:
    content = content.replace(anchor, safe_block + '\n' + anchor)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fix applied successfully.")
else:
    print("WARNING: Could not find anchor.")
