with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """    return (
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
          <div className="flex" style={{ flexWrap: 'wrap', gap: '1rem', overflowY: 'auto' }}>"""

new_block = """    return (
      <div className="glass-panel" style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="flex justify-between items-center mb-1" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.3rem' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 'bold' }}>
            EXO-TRACKER
          </div>
          <button 
            onClick={() => setIsExoMinimized(!isExoMinimized)}
            onMouseEnter={enableMouse}
            onMouseLeave={disableMouse}
            title={isExoMinimized ? "Expand" : "Minimize"}
            style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
          >
            {isExoMinimized ? '+' : '-'}
          </button>
        </div>
        
        {!isExoMinimized && (
          <div style={{ display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
            <div className="text-accent mb-2" style={{ fontWeight: 'bold', fontSize: '0.85rem', wordBreak: 'break-all', marginTop: '0.2rem' }}>
              {currentPlanetBio.bodyName}
            </div>
            <div className="flex" style={{ flexWrap: 'wrap', gap: '1rem' }}>"""


old_end = """           })}
          </div>
        )}
      </div>
    );
  }"""

new_end = """           })}
            </div>
          </div>
        )}
      </div>
    );
  }"""


if old_block in content:
    content = content.replace(old_block, new_block)
    content = content.replace(old_end, new_end)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed clipping.')
else:
    print('Error: Could not find block')
