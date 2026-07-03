with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_start = """  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
        <div className="flex justify-between items-center mb-2">"""

new_start = """  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: '1rem' }}>
      <div style={{ width: '400px', flexShrink: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
        <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
          <div className="flex justify-between items-center mb-2">"""

old_end = """      {/* HVT Alerts */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', pointerEvents: 'none', marginTop: '0.5rem', alignItems: 'flex-start' }}>
        {hvtAlerts.map(alert => (
          <div key={alert.id} className="glass-panel" style={{ padding: '0.5rem 1rem', background: 'rgba(15, 15, 15, 0.9)', borderLeft: `3px solid ${alert.type === 'bio' ? 'var(--success-color)' : 'var(--accent-color)'}` }}>
            <div style={{ fontWeight: 'bold' }}>{alert.message}</div>
            {alert.submessage && <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{alert.submessage}</div>}
          </div>
        ))}
      </div>

    </div>
  );
}"""

new_end = """      {/* HVT Alerts */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', pointerEvents: 'none', marginTop: '0.5rem', alignItems: 'flex-start' }}>
        {hvtAlerts.map(alert => (
          <div key={alert.id} className="glass-panel" style={{ padding: '0.5rem 1rem', background: 'rgba(15, 15, 15, 0.9)', borderLeft: `3px solid ${alert.type === 'bio' ? 'var(--success-color)' : 'var(--accent-color)'}` }}>
            <div style={{ fontWeight: 'bold' }}>{alert.message}</div>
            {alert.submessage && <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{alert.submessage}</div>}
          </div>
        ))}
      </div>

      </div> {/* End left column */}

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
}"""

content = content.replace(old_start, new_start)
content = content.replace(old_end, new_end)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Applied UI layout changes.')
