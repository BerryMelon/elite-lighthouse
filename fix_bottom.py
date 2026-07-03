with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the bottom of the file
old_bottom = """      <div className="mt-4 flex justify-between items-center" style={{ marginTop: 'auto', paddingTop: '0.5rem', gap: '1rem' }}>
        <div 
          className={statusMessage.includes('Spansh') || statusMessage.includes('failed') || statusMessage.includes('Please') ? "text-warning" : "text-success"} 
          style={{ fontSize: '0.9rem', flex: 1, wordWrap: 'break-word', lineHeight: '1.2' }}
        >
          {statusMessage}
        </div>
        <button onClick={startRoute} disabled={isCalculating} style={{ flexShrink: 0 }}>Calculate & Start Route</button>

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
    </div>
  );
}"""

new_bottom = """      <div className="mt-4 flex justify-between items-center" style={{ marginTop: 'auto', paddingTop: '0.5rem', gap: '1rem' }}>
        <div 
          className={statusMessage.includes('Spansh') || statusMessage.includes('failed') || statusMessage.includes('Please') ? "text-warning" : "text-success"} 
          style={{ fontSize: '0.9rem', flex: 1, wordWrap: 'break-word', lineHeight: '1.2' }}
        >
          {statusMessage}
        </div>
        <button onClick={startRoute} disabled={isCalculating} style={{ flexShrink: 0 }}>Calculate & Start Route</button>
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

if old_bottom in content:
    content = content.replace(old_bottom, new_bottom)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed bottom!')
else:
    print('Error: Could not find old_bottom block in App.tsx.')
