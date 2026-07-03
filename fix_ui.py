import sys

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. SidebarIcon padding -> tighter
code = code.replace("padding: '0.8rem 0',", "padding: '0.6rem 0',")
code = code.replace("width: '20'", "width: '18'")
code = code.replace("height: '20'", "height: '18'")

# 2. Sidebar structure & Minimize button
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

# 3. Main layout content area (add relative position and the minimize button)
old_content_area = """{/* Content Area */}
<div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1rem', overflow: 'hidden' }}>"""

new_content_area = """{/* Content Area */}
<div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1rem', overflow: 'hidden', position: 'relative' }}>
{!isMinimized && (
<button onClick={() => setIsMinimized(true)} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Minimize HUD" style={{ position: 'absolute', top: '0.5rem', right: '0.5rem', padding: '0.2rem 0.6rem', fontSize: '1rem', background: 'transparent', border: 'none', color: 'var(--text-secondary)', pointerEvents: 'auto', WebkitAppRegion: 'no-drag' as any, zIndex: 100, cursor: 'pointer', boxShadow: 'none' }}>−</button>
)}"""
code = code.replace(old_content_area, new_content_area)

# 4. Remove v1.0 from route planner
code = code.replace("""Neutron Router <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>""", """Neutron Router""")

# 5. Add margin to CALCULATE & START
old_calc_btn = """<button onClick={startRoute} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ padding: '0.6rem', fontWeight: 'bold' }}>
CALCULATE &amp; START
</button>"""
new_calc_btn = """<button onClick={startRoute} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ padding: '0.6rem', fontWeight: 'bold', marginTop: '1rem' }}>
CALCULATE &amp; START
</button>"""
code = code.replace(old_calc_btn, new_calc_btn)

# 6. Add title to Exo Tracker
old_exo_tab = """case 'exo':
return (
<div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
<div style={{ flex: 1, overflowY: 'auto' }} onMouseEnter={enableMouse} onMouseLeave={disableMouse}>"""

new_exo_tab = """case 'exo':
return (
<div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
<h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>Exo Tracker</h3>
<div style={{ flex: 1, overflowY: 'auto', marginTop: '0.5rem' }} onMouseEnter={enableMouse} onMouseLeave={disableMouse}>"""
code = code.replace(old_exo_tab, new_exo_tab)


# 7. Add Copy buttons for Source and Destination
old_source_input = """<SystemAutocomplete value={source} onChange={setSource} placeholder="e.g. Sol" style={{ flex: 1 }} />
<button onClick={handleUseCurrentLocation} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Use Current Location">&#x2316;</button>
</div>"""
new_source_input = """<SystemAutocomplete value={source} onChange={setSource} placeholder="e.g. Sol" style={{ flex: 1 }} />
<button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(source); setStatusMessage('Copied Source!'); setTimeout(()=>setStatusMessage(''),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Source">&#x274F;</button>
<button onClick={handleUseCurrentLocation} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Use Current Location">&#x2316;</button>
</div>"""
code = code.replace(old_source_input, new_source_input)

old_dest_input = """<SystemAutocomplete value={destination} onChange={setDestination} placeholder="e.g. Colonia" style={{ flex: 1 }} />
</div>"""
new_dest_input = """<SystemAutocomplete value={destination} onChange={setDestination} placeholder="e.g. Colonia" style={{ flex: 1 }} />
<button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(destination); setStatusMessage('Copied Destination!'); setTimeout(()=>setStatusMessage(''),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Destination">&#x274F;</button>
</div>"""
code = code.replace(old_dest_input, new_dest_input)

# 8. POI Search Tab styling
old_poi_btns = """<div className="flex mb-4" style={{ gap: '1rem' }}>
<button onClick={searchCarriers} onMouseEnter={enableMouse} onMouseLeave={disableMouse} disabled={isSearchingPoi} style={{ pointerEvents: 'auto', padding: '0.3rem 0.6rem', fontSize: '0.8rem' }}>{isSearchingPoi ? 'Searching...' : 'Nearby Fleet Carriers'}</button>
<button disabled style={{ padding: '0.3rem 0.6rem', fontSize: '0.8rem', opacity: 0.5 }}>Scenic Views (Soon)</button>
</div>"""

new_poi_btns = """<div className="flex mb-4" style={{ gap: '1.5rem', marginTop: '1rem' }}>
<button onClick={searchCarriers} onMouseEnter={enableMouse} onMouseLeave={disableMouse} disabled={isSearchingPoi} style={{ pointerEvents: 'auto', padding: 0, fontSize: '0.8rem', background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--accent-color)', fontWeight: 'bold' }}>{isSearchingPoi ? 'SEARCHING...' : 'NEARBY FLEET CARRIERS'}</button>
<button disabled style={{ padding: 0, fontSize: '0.8rem', opacity: 0.5, background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)', fontWeight: 'bold' }}>SCENIC VIEWS (SOON)</button>
</div>"""
code = code.replace(old_poi_btns, new_poi_btns)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
print("UI layout tweaks applied.")
