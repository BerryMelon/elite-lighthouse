import re
import sys

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 1. SidebarIcon padding & size
    if 'padding: \'0.8rem 0\'' in line:
        line = line.replace('0.8rem', '0.6rem')
    
    # 2. SVGs
    if 'const RouteIcon =' in line:
        new_lines.append('const RouteIcon = () => (\n')
        new_lines.append('  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">\n')
        new_lines.append('    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>\n')
        new_lines.append('  </svg>\n')
        new_lines.append(');\n')
        i += 7
        continue
        
    if 'const HvtIcon =' in line:
        new_lines.append('const HvtIcon = () => (\n')
        new_lines.append('  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">\n')
        new_lines.append('    <circle cx="12" cy="12" r="10"></circle>\n')
        new_lines.append('    <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>\n')
        new_lines.append('    <path d="M2 12h20"></path>\n')
        new_lines.append('  </svg>\n')
        new_lines.append(');\n')
        i += 6
        continue
        
    if 'const ExoIcon =' in line:
        new_lines.append('const ExoIcon = () => (\n')
        new_lines.append('  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">\n')
        new_lines.append('    <path d="M2 15c6.667-6 13.333 0 20-6"></path>\n')
        new_lines.append('    <path d="M9 22c1.798-1.998 2.518-3.995 2.808-5.75"></path>\n')
        new_lines.append('    <path d="M14 6.4c.16 1.433-.116 3.14-1.127 5.059"></path>\n')
        new_lines.append('    <path d="M2 9c6.667 6 13.333 0 20 6"></path>\n')
        new_lines.append('    <path d="M6 10.7l3.2 3"></path>\n')
        new_lines.append('    <path d="M14.5 10l3.5 3.5"></path>\n')
        new_lines.append('    <path d="M10.8 15.6l-3.5 3.5"></path>\n')
        new_lines.append('  </svg>\n')
        new_lines.append(');\n')
        i += 7
        continue
        
    # 3. Route planner title
    if 'Neutron Router' in line and '<span style=' in line:
        line = '                <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: \'2px\', margin: 0, textTransform: \'uppercase\', fontSize: \'1rem\' }}>\n                  Neutron Router\n                </h3>\n'
        
    # 4. Copy buttons
    if 'placeholder="e.g. Sol"' in line:
        new_lines.append(line)
        new_lines.append('                    <button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(source); setStatusMessage(\'Copied Source!\'); setTimeout(()=>setStatusMessage(\'\'),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Source" style={{ padding: \'0.4rem\', border: \'none\', background: \'rgba(255,255,255,0.05)\' }}>&#x274F;</button>\n')
        i += 1
        continue
        
    if 'placeholder="e.g. Colonia"' in line:
        new_lines.append(line)
        new_lines.append('                    <button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(destination); setStatusMessage(\'Copied Destination!\'); setTimeout(()=>setStatusMessage(\'\'),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Destination" style={{ padding: \'0.4rem\', border: \'none\', background: \'rgba(255,255,255,0.05)\' }}>&#x274F;</button>\n')
        i += 1
        continue
        
    # 5. Route Planner startRoute button
    if 'onClick={startRoute}' in line:
        line = line.replace('style={{ pointerEvents: \'auto\' }}', 'style={{ pointerEvents: \'auto\', padding: \'0.6rem\', fontWeight: \'bold\', marginTop: \'1rem\' }}')
        
    # 6. POI Tabs
    if 'onClick={searchCarriers}' in line:
        new_lines.append('              <button onClick={searchCarriers} onMouseEnter={enableMouse} onMouseLeave={disableMouse} disabled={isSearchingPoi} style={{ pointerEvents: \'auto\', padding: 0, fontSize: \'0.8rem\', background: \'transparent\', border: \'none\', boxShadow: \'none\', color: \'var(--accent-color)\', fontWeight: \'bold\' }}>{isSearchingPoi ? \'SEARCHING...\' : \'NEARBY FLEET CARRIERS\'}</button>\n')
        new_lines.append('              <button disabled style={{ padding: 0, fontSize: \'0.8rem\', opacity: 0.5, background: \'transparent\', border: \'none\', boxShadow: \'none\', color: \'var(--text-secondary)\', fontWeight: \'bold\' }}>SCENIC VIEWS (SOON)</button>\n')
        i += 2
        continue
        
    if 'gap: \'1rem\'' in line and 'mb-4' in line:
        line = line.replace('gap: \'1rem\'', 'gap: \'1.5rem\', marginTop: \'1rem\'')
        
    # 7. Exo Tracker missing title
    if 'Please land on a planet to begin surface scanning...' in line:
        # We know the previous 2 lines are the container setup.
        # We will pop them out, inject the title, then put them back.
        if '<div style={{ flex: 1, display: \'flex\', flexDirection: \'column\', alignItems: \'center\', justifyContent: \'center\' }}>' in new_lines[-1]:
            new_lines[-1] = '            <div style={{ flex: 1, display: \'flex\', flexDirection: \'column\' }}>\n'
            new_lines.append('              <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: \'2px\', margin: 0, textTransform: \'uppercase\', fontSize: \'1rem\' }}>Exo Tracker</h3>\n')
            new_lines.append('              <div style={{ flex: 1, display: \'flex\', alignItems: \'center\', justifyContent: \'center\' }}>\n')
            new_lines.append(line)
            new_lines.append('              </div>\n')
            i += 1
            continue
        
    # 8. POI Search debug
    if 'data = res.data;' in line and 'searchCarriers' in "".join(lines[max(0, i-25):i]):
        new_lines.append(line)
        new_lines.append('              if (res.error) setStatusMessage(\'Proxy Err: \' + res.error);\n')
        new_lines.append('              if (res.status !== 200) setStatusMessage(\'Spansh Err \' + res.status + \': \' + JSON.stringify(res.data).substring(0, 50));\n')
        i += 1
        continue
        
    if 'setStatusMessage(\'Failed to fetch carriers.\');' in line and 'searchCarriers' in "".join(lines[max(0, i-25):i+5]):
        new_lines.append('            setStatusMessage(\'Error: \' + err.message);\n')
        i += 1
        continue
        
    if 'catch (err)' in line and 'searchCarriers' in "".join(lines[max(0, i-25):i+5]):
        line = line.replace('catch (err)', 'catch (err: any)')

    # 9. Sidebar and content layout
    if 'width: \'50px\'' in line and 'WebkitAppRegion: \'drag\'' in line:
        line = line.replace('width: \'50px\'', 'width: \'45px\'')
        line = line.replace('padding: \'1rem 0\'', 'paddingTop: \'1.2rem\'')
        
    if 'title="Minimize HUD"' in line and 'WebkitAppRegion' in lines[i+1]:
        # Skip the old minimize button by skipping 5 lines
        new_lines.pop() # remove the <button ... >
        new_lines.pop() # remove onClick
        new_lines.pop() # remove onMouse
        new_lines.pop() # remove onMouse
        i += 4
        new_lines.append('            <div style={{ fontSize: \'0.6em\', opacity: 0.5, marginBottom: \'0.5rem\', WebkitAppRegion: \'no-drag\' as any }}>v1.0</div>\n')
        continue

    if 'flex: 1, display: \'flex\', flexDirection: \'column\', padding: \'1rem\', overflow: \'hidden\'' in line and 'Content Area' in new_lines[-1]:
        line = line.replace('overflow: \'hidden\'', 'overflow: \'hidden\', position: \'relative\'')
        new_lines.append(line)
        new_lines.append('          {!isMinimized && (\n')
        new_lines.append('            <button onClick={() => setIsMinimized(true)} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Minimize HUD" style={{ position: \'absolute\', top: \'0.5rem\', right: \'0.5rem\', padding: \'0.2rem 0.6rem\', fontSize: \'1rem\', background: \'transparent\', border: \'none\', color: \'var(--text-secondary)\', pointerEvents: \'auto\', WebkitAppRegion: \'no-drag\' as any, zIndex: 100, cursor: \'pointer\', boxShadow: \'none\' }}>&minus;</button>\n')
        new_lines.append('          )}\n')
        i += 1
        continue
        
    new_lines.append(line)
    i += 1

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated App.tsx successfully.')
