with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Minimized Setup Screen
old_minimized = """  if (!hudMode && isMinimized) {
    return (
      <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
        <div className="flex justify-between items-center">
          <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
            Lighthouse <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>
          </h3>
          <button 
            onClick={() => setIsMinimized(false)} 
            onMouseEnter={enableMouse}
            onMouseLeave={disableMouse}
            title="Expand"
            style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
          >
            +
          </button>
        </div>

      {/* HVT Alerts */}
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

new_minimized = """  if (!hudMode && isMinimized) {
    return (
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
          <div className="flex justify-between items-center">
            <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
              Lighthouse <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>
            </h3>
            <button 
              onClick={() => setIsMinimized(false)} 
              onMouseEnter={enableMouse}
              onMouseLeave={disableMouse}
              title="Expand"
              style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
            >
              +
            </button>
          </div>
        </div>

        {/* HVT Alerts */}
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

# 2. Fix Maximized Setup Screen
old_setup = """  return (
    <div className="glass-panel" style={{ width: '100%', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
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

new_setup = """  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
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

old_setup_end = """      {/* HVT Alerts */}
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

new_setup_end = """      </div>

      {/* HVT Alerts */}
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

if old_minimized in content:
    content = content.replace(old_minimized, new_minimized)
else:
    print('Warning: old_minimized not found')
    
if old_setup in content and old_setup_end in content:
    content = content.replace(old_setup, new_setup)
    content = content.replace(old_setup_end, new_setup_end)
else:
    print('Warning: old_setup or old_setup_end not found')
    
with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Structure updated!')
