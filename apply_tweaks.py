import re
import sys

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. SidebarIcon padding
code = re.sub(r"padding: '0.8rem 0',", "padding: '0.6rem 0',", code)

# 2. Sidebar SVGs
route_icon_old = r'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">.*?<\/svg>'

route_icon_new = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">\n    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>\n  </svg>'
code = re.sub(r'const RouteIcon = \(\) => \(\s*' + route_icon_old + r'\s*\);', 'const RouteIcon = () => (\n  ' + route_icon_new + '\n);', code, flags=re.DOTALL)

hvt_icon_new = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">\n    <circle cx="12" cy="12" r="10"></circle>\n    <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>\n    <path d="M2 12h20"></path>\n  </svg>'
code = re.sub(r'const HvtIcon = \(\) => \(\s*' + route_icon_old + r'\s*\);', 'const HvtIcon = () => (\n  ' + hvt_icon_new + '\n);', code, flags=re.DOTALL)

exo_icon_new = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">\n    <path d="M2 15c6.667-6 13.333 0 20-6"></path>\n    <path d="M9 22c1.798-1.998 2.518-3.995 2.808-5.75"></path>\n    <path d="M14 6.4c.16 1.433-.116 3.14-1.127 5.059"></path>\n    <path d="M2 9c6.667 6 13.333 0 20 6"></path>\n    <path d="M6 10.7l3.2 3"></path>\n    <path d="M14.5 10l3.5 3.5"></path>\n    <path d="M10.8 15.6l-3.5 3.5"></path>\n  </svg>'
code = re.sub(r'const ExoIcon = \(\) => \(\s*' + route_icon_old + r'\s*\);', 'const ExoIcon = () => (\n  ' + exo_icon_new + '\n);', code, flags=re.DOTALL)

# 3. Sidebar layout bottom v1.0
old_sidebar = """{!isMinimized && (
          <div style={{ width: '50px', borderRight: '1px solid rgba(255,255,255,0.1)', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '1rem 0', WebkitAppRegion: 'drag' as any }}>
            <SidebarIcon active={activeTab==='route'} onClick={() => setActiveTab('route')} icon={<RouteIcon/>} title="Route Planner" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='hvt'} onClick={() => setActiveTab('hvt')} icon={<HvtIcon/>} title="System Info (HVT)" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='exo'} onClick={() => setActiveTab('exo')} icon={<ExoIcon/>} title="Exo Tracker" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='poi'} onClick={() => setActiveTab('poi')} icon={<PoiIcon/>} title="POI Search" enableMouse={enableMouse} disableMouse={disableMouse} />
            <div style={{ flex: 1 }} />
            <button 
              onClick={() => setIsMinimized(true)}
              onMouseEnter={enableMouse}
              onMouseLeave={disableMouse}
              title="Minimize HUD"
              style={{ padding: '0.2rem 0.5rem', fontSize: '0.8rem', pointerEvents: 'auto', WebkitAppRegion: 'no-drag' as any }}
            >
              -
            </button>
          </div>
        )}"""
new_sidebar = """{!isMinimized && (
          <div style={{ width: '45px', borderRight: '1px solid rgba(255,255,255,0.1)', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '1.2rem', WebkitAppRegion: 'drag' as any }}>
            <SidebarIcon active={activeTab==='route'} onClick={() => setActiveTab('route')} icon={<RouteIcon/>} title="Route Planner" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='hvt'} onClick={() => setActiveTab('hvt')} icon={<HvtIcon/>} title="System Info (HVT)" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='exo'} onClick={() => setActiveTab('exo')} icon={<ExoIcon/>} title="Exo Tracker" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='poi'} onClick={() => setActiveTab('poi')} icon={<PoiIcon/>} title="POI Search" enableMouse={enableMouse} disableMouse={disableMouse} />
            <div style={{ flex: 1 }} />
            <div style={{ fontSize: '0.6em', opacity: 0.5, marginBottom: '0.5rem', WebkitAppRegion: 'no-drag' as any }}>v1.0</div>
          </div>
        )}"""
code = code.replace(old_sidebar, new_sidebar)

# 4. Content Area Layout
old_content = """        {/* Content Area */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1rem', overflow: 'hidden' }}>
          {isMinimized ? ("""
new_content = """        {/* Content Area */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1rem', overflow: 'hidden', position: 'relative' }}>
          {!isMinimized && (
            <button onClick={() => setIsMinimized(true)} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Minimize HUD" style={{ position: 'absolute', top: '0.5rem', right: '0.5rem', padding: '0.2rem 0.6rem', fontSize: '1rem', background: 'transparent', border: 'none', color: 'var(--text-secondary)', pointerEvents: 'auto', WebkitAppRegion: 'no-drag' as any, zIndex: 100, cursor: 'pointer', boxShadow: 'none' }}>−</button>
          )}
          {isMinimized ? ("""
code = code.replace(old_content, new_content)

# 5. Route Planner Title
code = code.replace("""Neutron Router <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>""", "Neutron Router")

# 6. Calculate & Start Button
old_calc = """<button onClick={startRoute} disabled={isCalculating} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ pointerEvents: 'auto' }}>Calculate & Start</button>"""
new_calc = """<button onClick={startRoute} disabled={isCalculating} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ pointerEvents: 'auto', padding: '0.6rem', fontWeight: 'bold', marginTop: '1rem' }}>Calculate & Start</button>"""
code = code.replace(old_calc, new_calc)

# 7. Copy Buttons
old_source = """                    <SystemAutocomplete value={source} onChange={setSource} placeholder="e.g. Sol" style={{ flex: 1 }} />
                    <button onClick={handleUseCurrentLocation} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Use Current Location">&#x2316;</button>"""
new_source = """                    <SystemAutocomplete value={source} onChange={setSource} placeholder="e.g. Sol" style={{ flex: 1 }} />
                    <button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(source); setStatusMessage('Copied Source!'); setTimeout(()=>setStatusMessage(''),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Source" style={{ padding: '0.4rem', border: 'none', background: 'rgba(255,255,255,0.05)' }}>&#x274F;</button>
                    <button onClick={handleUseCurrentLocation} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Use Current Location">&#x2316;</button>"""
code = code.replace(old_source, new_source)

old_dest = """                    <SystemAutocomplete value={destination} onChange={setDestination} placeholder="e.g. Colonia" style={{ flex: 1 }} />
                  </div>"""
new_dest = """                    <SystemAutocomplete value={destination} onChange={setDestination} placeholder="e.g. Colonia" style={{ flex: 1 }} />
                    <button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(destination); setStatusMessage('Copied Destination!'); setTimeout(()=>setStatusMessage(''),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Destination" style={{ padding: '0.4rem', border: 'none', background: 'rgba(255,255,255,0.05)' }}>&#x274F;</button>
                  </div>"""
code = code.replace(old_dest, new_dest)

# 8. POI Search Tabs
old_poi_tabs = """            <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>POI Search</h3>
            <div className="flex mb-4" style={{ gap: '1rem' }}>
              <button onClick={searchCarriers} onMouseEnter={enableMouse} onMouseLeave={disableMouse} disabled={isSearchingPoi} style={{ pointerEvents: 'auto', padding: '0.3rem 0.6rem', fontSize: '0.8rem' }}>{isSearchingPoi ? 'Searching...' : 'Nearby Fleet Carriers'}</button>
              <button disabled style={{ padding: '0.3rem 0.6rem', fontSize: '0.8rem', opacity: 0.5 }}>Scenic Views (Soon)</button>
            </div>"""
new_poi_tabs = """            <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>POI Search</h3>
            <div className="flex mb-4" style={{ gap: '1.5rem', marginTop: '1rem' }}>
              <button onClick={searchCarriers} onMouseEnter={enableMouse} onMouseLeave={disableMouse} disabled={isSearchingPoi} style={{ pointerEvents: 'auto', padding: 0, fontSize: '0.8rem', background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--accent-color)', fontWeight: 'bold' }}>{isSearchingPoi ? 'SEARCHING...' : 'NEARBY FLEET CARRIERS'}</button>
              <button disabled style={{ padding: 0, fontSize: '0.8rem', opacity: 0.5, background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)', fontWeight: 'bold' }}>SCENIC VIEWS (SOON)</button>
            </div>"""
code = code.replace(old_poi_tabs, new_poi_tabs)

# 9. Exo Tracker un-landed title
old_exo_empty = """        if (!currentPlanetBio) {
          return (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ color: 'var(--text-secondary)' }}>Please land on a planet to begin surface scanning...</div>
            </div>
          );
        }"""
new_exo_empty = """        if (!currentPlanetBio) {
          return (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>Exo Tracker</h3>
              <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ color: 'var(--text-secondary)' }}>Please land on a planet to begin surface scanning...</div>
              </div>
            </div>
          );
        }"""
code = code.replace(old_exo_empty, new_exo_empty)

# 10. POI Debug + Fix
old_poi_try = """            if (window.electronAPI && window.electronAPI.fetchProxy) {
              const res = await window.electronAPI.fetchProxy('https://spansh.co.uk/api/stations/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({
                  filters: { type: { value: ["Drake-Class Carrier"] } },
                  sort: [{ distance: { direction: "asc" } }],
                  reference_system: source
                })
              });
              data = res.data;
            }"""
new_poi_try = """            if (window.electronAPI && window.electronAPI.fetchProxy) {
              const res = await window.electronAPI.fetchProxy('https://spansh.co.uk/api/stations/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({
                  filters: { type: { value: ["Drake-Class Carrier"] } },
                  sort: [{ distance: { direction: "asc" } }],
                  reference_system: source
                })
              });
              data = res.data;
              if (res.error) setStatusMessage('Proxy Err: ' + res.error);
              if (res.status !== 200) setStatusMessage('Spansh Err ' + res.status + ': ' + JSON.stringify(res.data).substring(0, 50));
            }"""
code = code.replace(old_poi_try, new_poi_try)

old_poi_catch = """          } catch (err) {
            console.error(err);
            setStatusMessage('Failed to fetch carriers.');
          } finally {"""
new_poi_catch = """          } catch (err: any) {
            console.error(err);
            setStatusMessage('Error: ' + err.message);
          } finally {"""
code = code.replace(old_poi_catch, new_poi_catch)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied tweaks and POI debug successfully!")
