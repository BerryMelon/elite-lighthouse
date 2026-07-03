with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state variable
state_var = '  const [isExoMinimized, setIsExoMinimized] = useState(false);'
if state_var not in content:
    content = content.replace('  const [hudMode, setHudMode] = useState(false);', state_var + '\n  const [hudMode, setHudMode] = useState(false);')

# 2. Update the ExoTracker render block
old_exo_render = """  if (isExoMode) {
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

new_exo_render = """  if (isExoMode) {
    if (!currentPlanetBio) {
      return (
        <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ color: 'var(--text-secondary)' }}>Waiting for surface scan...</div>
        </div>
      );
    }
    return (
      <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="flex justify-between items-start mb-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 'bold', flexShrink: 0, marginTop: '0.2rem' }}>
            EXO-TRACKER
          </div>
          
          {isExoMinimized ? (
             <button 
               onClick={() => setIsExoMinimized(false)}
               onMouseEnter={enableMouse}
               onMouseLeave={disableMouse}
               title="Expand"
               style={{ fontSize: '0.8rem', padding: '0.1rem 0.4rem', pointerEvents: 'auto' }}
             >
               +
             </button>
          ) : (
             <div className="flex flex-col items-end" style={{ flex: 1, marginLeft: '0.5rem', minWidth: 0 }}>
               <div className="text-accent" style={{ fontWeight: 'bold', fontSize: '0.85rem', textAlign: 'right', wordBreak: 'break-word', lineHeight: '1.2' }}>
                 {currentPlanetBio.bodyName}
               </div>
               <button 
                 onClick={() => setIsExoMinimized(true)}
                 onMouseEnter={enableMouse}
                 onMouseLeave={disableMouse}
                 title="Minimize"
                 style={{ fontSize: '0.7rem', padding: '0.1rem 0.3rem', pointerEvents: 'auto', marginTop: '0.3rem' }}
               >
                 - Minimize
               </button>
             </div>
          )}
        </div>
        
        {!isExoMinimized && (
          <div className="flex" style={{ flexWrap: 'wrap', gap: '1rem', overflowY: 'auto' }}>
            {Array.from({ length: Math.max(currentPlanetBio.totalSignals, Object.keys(currentPlanetBio.scanned).length) }).map((_, i) => {
               const scannedKeys = Object.keys(currentPlanetBio.scanned);
               if (i < scannedKeys.length) {
                 const species = scannedKeys[i];
                 const count = currentPlanetBio.scanned[species];
                 const isComplete = count >= 3;
                 return (
                   <div key={i} className={isComplete ? "text-success" : "text-accent"} style={{ fontSize: '0.85rem', flex: '1 1 45%' }}>
                     {isComplete ? `✓ ${species}` : `🧬 ${species} (${count}/3)`}
                   </div>
                 );
               } else {
                 return (
                   <div key={i} className="text-secondary" style={{ fontSize: '0.85rem', flex: '1 1 45%' }}>
                     ? Unknown Bio Signal
                   </div>
                 );
               }
            })}
          </div>
        )}
      </div>
    );
  }"""

if old_exo_render in content:
    content = content.replace(old_exo_render, new_exo_render)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated App.tsx successfully.')
else:
    print('Error: Could not find block')
