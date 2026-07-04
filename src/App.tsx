import { useState, useEffect, useRef } from 'react';
import './index.css';

declare global {
  interface Window {
    electronAPI: any;
  }
}

function SystemAutocomplete({ value, onChange, placeholder, style }: { value: string, onChange: (v: string) => void, placeholder?: string, style?: any }) {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Only search if 3 or more characters and we don't exactly match the only suggestion
    if (value.length < 3) {
      setSuggestions([]);
      setIsLoading(false);
      return;
    }
    
    setIsLoading(true);
    const timer = setTimeout(async () => {
      try {
        let data;
        const url = `https://spansh.co.uk/api/systems?q=${encodeURIComponent(value)}`;
        if (window.electronAPI && window.electronAPI.fetchProxy) {
          const res = await window.electronAPI.fetchProxy(url);
          data = res.data;
        } else {
          const res = await fetch(url);
          data = await res.json();
        }
        
        if (Array.isArray(data)) {
          // If the user typed the exact full name and it's the only suggestion, don't show dropdown
          if (data.length === 1 && data[0].toLowerCase() === value.toLowerCase()) {
            setSuggestions([]);
          } else {
            setSuggestions(data);
          }
        }
      } catch (e) {} finally {
        setIsLoading(false);
      }
    }, 300); // 300ms debounce
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <div style={{ position: 'relative', display: 'flex', ...style }}>
      <input 
        type="text" 
        value={value} 
        onChange={e => {
          onChange(e.target.value);
          setShowSuggestions(true);
        }} 
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
        placeholder={placeholder} 
        style={{ width: '100%', boxSizing: 'border-box' }}
      />
      {showSuggestions && (isLoading || suggestions.length > 0) && (
        <ul style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          background: 'rgba(20, 25, 35, 0.95)',
          border: '1px solid var(--accent-color)',
          borderRadius: '4px',
          listStyle: 'none',
          margin: 0,
          padding: 0,
          maxHeight: '150px',
          overflowY: 'auto',
          zIndex: 100,
          // @ts-ignore
          WebkitAppRegion: 'no-drag'
        }}>
          {isLoading && (
            <li style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontStyle: 'italic', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
              Searching...
            </li>
          )}
          {!isLoading && suggestions.map(s => (
            <li 
              key={s} 
              onMouseDown={(e) => {
                e.preventDefault(); // Prevents blur from firing before this
                onChange(s);
                setShowSuggestions(false);
              }}
              style={{ padding: '0.5rem', cursor: 'pointer', borderBottom: '1px solid rgba(255,255,255,0.1)' }}
            >
              {s}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}


const RouteIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
  </svg>
);

const HvtIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"></circle>
    <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>
    <path d="M2 12h20"></path>
  </svg>
);

const ExoIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 2c0 5-6 5-6 10s6 5 6 10" />
    <path d="M9 2c0 5 6 5 6 10s-6 5-6 10" />
    <line x1="10" y1="4.5" x2="14" y2="4.5" />
    <line x1="10" y1="9.5" x2="14" y2="9.5" />
    <line x1="9" y1="12" x2="15" y2="12" />
    <line x1="10" y1="14.5" x2="14" y2="14.5" />
    <line x1="10" y1="19.5" x2="14" y2="19.5" />
  </svg>
);

const PoiIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8"></circle>
    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
  </svg>
);

const SidebarIcon = ({ active, onClick, icon, title, enableMouse, disableMouse }: any) => (
  <button
    onClick={onClick}
    title={title}
    onMouseEnter={enableMouse}
    onMouseLeave={disableMouse}
    style={{
      background: 'transparent',
      border: 'none',
      boxShadow: 'none',
      color: active ? 'var(--accent-color)' : 'rgba(255,255,255,0.4)',
      padding: '0.6rem 0',
      cursor: 'pointer',
      transition: 'color 0.2s',
      pointerEvents: 'auto',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '100%',
      WebkitAppRegion: 'no-drag' as any
    }}
  >
    {icon}
  </button>
);

function App() {
  const [route, setRoute] = useState<any[]>([]);
  const [currentJumpIndex, setCurrentJumpIndex] = useState(0);
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [range, setRange] = useState(() => localStorage.getItem('userRange') || '50');
  const [superchargeType, setSuperchargeType] = useState(() => localStorage.getItem('userSuperchargeType') || 'normal'); // 'normal' or 'overcharge'
  
  useEffect(() => {
    localStorage.setItem('userRange', range);
  }, [range]);

  useEffect(() => {
    localStorage.setItem('userSuperchargeType', superchargeType);
  }, [superchargeType]);
  const [hudMode, setHudMode] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  
  const [activeTab, setActiveTab] = useState<'route' | 'hvt' | 'exo' | 'poi'>('route');
  
  const hudModeRef = useRef(hudMode);
  useEffect(() => {
    hudModeRef.current = hudMode;
    if (window.electronAPI) {
      window.electronAPI.setIgnoreMouseEvents(hudMode, { forward: true });
    }
  }, [hudMode]);

  useEffect(() => {
    const saved = localStorage.getItem('savedRoute');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setRoute(parsed.route);
        setCurrentJumpIndex(parsed.currentJumpIndex);
        setSource(parsed.source);
        setDestination(parsed.destination);
        if (parsed.range) setRange(parsed.range);
        if (parsed.superchargeType) setSuperchargeType(parsed.superchargeType);
        setHudMode(true);
      } catch (e) {
        localStorage.removeItem('savedRoute');
      }
    }
  }, []);

  const [statusMessage, setStatusMessage] = useState('');
  const [isSearchingPoi, setIsSearchingPoi] = useState(false);
  const [poiResults, setPoiResults] = useState<{name: string, system_name: string, distance: number}[] | null>(null);

  const searchCarriers = async () => {
    setIsSearchingPoi(true);
    setPoiResults(null);
    try {
      let searchSystem = source;
      let searchPos = null;
      
      if (window.electronAPI) {
        const actualLocation = await window.electronAPI.getCurrentLocation();
        if (actualLocation && actualLocation.system) {
          searchSystem = actualLocation.system;
          searchPos = actualLocation.pos;
        }
      }

      if (!searchSystem) {
        setStatusMessage('Location unknown. Enter Source in Route Planner.');
        setIsSearchingPoi(false);
        setTimeout(() => setStatusMessage(''), 5000);
        return;
      }
      
      // Fallback if system is unknown to Spansh
      if (window.electronAPI && window.electronAPI.fetchProxy) {
        try {
          const checkRes = await window.electronAPI.fetchProxy(`https://spansh.co.uk/api/systems?q=${encodeURIComponent(searchSystem)}`);
          const isKnown = checkRes.data && checkRes.data.some((s: string) => s.toLowerCase() === searchSystem.toLowerCase());
          
          if (!isKnown && searchPos) {
            const [x, y, z] = searchPos;
            const edsmRes = await window.electronAPI.fetchProxy(`https://www.edsm.net/api-v1/sphere-systems?x=${x}&y=${y}&z=${z}&radius=50`);
            if (edsmRes.data && edsmRes.data.length > 0) {
              const sorted = edsmRes.data.sort((a: any, b: any) => a.distance - b.distance);
              const nearest = sorted.find((s: any) => s.name.toLowerCase() !== searchSystem.toLowerCase());
              if (nearest) {
                searchSystem = nearest.name;
              }
            }
          }
        } catch(e) {}
      }

      let data;
      if (window.electronAPI && window.electronAPI.fetchProxy) {
        const res = await window.electronAPI.fetchProxy('https://spansh.co.uk/api/stations/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            filters: { type: { value: ["Drake-Class Carrier"] } },
            sort: [{ distance: { direction: "asc" } }],
            reference_system: searchSystem
          })
        });
        data = res.data;
        if (res.error) setStatusMessage('Proxy Err: ' + res.error);
        if (res.status !== 200) setStatusMessage('Spansh Err ' + res.status + ': ' + JSON.stringify(res.data).substring(0, 50));
      } else {
        const response = await fetch('https://spansh.co.uk/api/stations/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            filters: { type: { value: ["Drake-Class Carrier"] } },
            sort: [{ distance: { direction: "asc" } }],
            reference_system: searchSystem
          })
        });
        data = await response.json();
      }
      if (data && data.results) {
        const results = data.results.slice(0, 15).map((r: any) => ({
          name: r.name,
          system_name: r.system_name,
          distance: r.distance
        }));
        setPoiResults(results);
      } else {
        setPoiResults([]);
      }
    } catch (err) {
      console.error(err);
      setStatusMessage('Failed to fetch carriers.');
    } finally {
      setIsSearchingPoi(false);
    }
  };

  const [isCalculating, setIsCalculating] = useState(false);
  const [isOffRoute, setIsOffRoute] = useState(false);
  const isOffRouteRef = useRef(isOffRoute);
  useEffect(() => { isOffRouteRef.current = isOffRoute; }, [isOffRoute]);

  // Exobiology State
  const [currentPlanetBio, setCurrentPlanetBio] = useState<{
    bodyName: string;
    totalSignals: number;
    scanned: Record<string, number>;
  } | null>(null);

  // HVT Alerts State
  const [hvtAlerts, setHvtAlerts] = useState<{ id: number; message: string; submessage?: string; type: 'hvt' | 'bio' }[]>([]);

  // Refs for tracking latest state inside event listener
  const routeRef = useRef(route);
  useEffect(() => { routeRef.current = route; }, [route]);
  
  const currentJumpIndexRef = useRef(currentJumpIndex);
  useEffect(() => { currentJumpIndexRef.current = currentJumpIndex; }, [currentJumpIndex]);

  const addHvtAlert = (message: string, submessage?: string, type: 'hvt' | 'bio' = 'hvt') => {
    const id = Date.now();
    setHvtAlerts(prev => [...prev, { id, message, submessage, type }]);
    
    // Auto-switch to HVT tab if an HVT is found and we are not on the neutron route
    if (routeRef.current.length === 0 || isOffRouteRef.current) {
      setActiveTab('hvt');
    }
  };

  useEffect(() => {
    if (window.electronAPI) {
      window.electronAPI.onFsdJump((data: any) => {
        setHvtAlerts([]); // Clear HVTs from previous system
        
        // Handle FSD Jump logic (same as before)
        const currentRoute = routeRef.current;
        const currentIndex = currentJumpIndexRef.current;
        
        if (currentRoute.length > 0 && hudModeRef.current) {
          const nextWaypoint = currentRoute[currentIndex + 1];
          const currentWaypoint = currentRoute[currentIndex];

          if (nextWaypoint && data.system.toLowerCase() === nextWaypoint.system.toLowerCase()) {
            setActiveTab('route');
            const nextIndex = currentIndex + 1;
            setCurrentJumpIndex(nextIndex);
            setIsOffRoute(false);
            
            localStorage.setItem('savedRoute', JSON.stringify({
              route: currentRoute,
              currentJumpIndex: nextIndex,
              source,
              destination,
              range,
              superchargeType
            }));
            
            // Check for HVT in arrival system
            if (nextWaypoint.hvt && nextWaypoint.hvt.length > 0) {
              const hvtMessage = nextWaypoint.hvt.map((h: any) => h.name).join(', ');
              addHvtAlert(`High Value Targets detected:`, hvtMessage, 'hvt');
            }
          } else if (currentWaypoint && data.system.toLowerCase() === currentWaypoint.system.toLowerCase()) {
            setActiveTab('route');
            setIsOffRoute(false);
          } else {
            setIsOffRoute(true);
          }
        }
      });
      
      window.electronAPI.onJournalEvent((data: any) => {
        if (data.event === 'SupercruiseEntry' || data.event === 'LeaveBody') {
          setCurrentPlanetBio(null);
        } else if (['SAAScanComplete', 'Touchdown', 'ScanOrganic', 'FSSBodySignals', 'SAASignalsFound'].includes(data.event)) {
          // Re-hydrate exo on touchdown, surface scan, or bio scan
          window.electronAPI.hydrateExo().then((res: any) => {
            if (res && res.bioState) {
              setCurrentPlanetBio(res.bioState);
              if (data.event === 'Touchdown' && res.bioState.totalSignals > 0) {
                setActiveTab('exo');
              }
            }
          });
        }
      });

      if (window.electronAPI.onRealtimeHvt) {
        window.electronAPI.onRealtimeHvt((data: any) => {
          addHvtAlert(`Live FSS Scan:`, `${data.message} on ${data.bodyName}`, 'hvt');
        });
      }
    }
  }, [source, destination, range]);

  useEffect(() => {
    // Try hydrate on mount for Exo Tracker
    if (window.electronAPI) {
      window.electronAPI.hydrateExo().then((res: any) => {
        if (res && res.bioState) {
          setCurrentPlanetBio(res.bioState);
          if (res.isLanded) {
            setActiveTab('exo');
          }
        }
      });
    }
  }, []);

  const calculateRoute = async (source: string, destination: string, range: string, superchargeType: string) => {
    if (!source || !destination || !range) {
      setStatusMessage('Please fill all fields');
      return;
    }

    setIsCalculating(true);
    setStatusMessage('Calculating route...');

    try {
      const url = `https://spansh.co.uk/api/routes`;
      
      // We will proxy this as well to avoid CORS if necessary
      let data;
      if (window.electronAPI && window.electronAPI.fetchProxy) {
        const res = await window.electronAPI.fetchProxy(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            source, destination, range: parseFloat(range),
            use_supercharge: superchargeType === 'overcharge' ? 0 : 1
          })
        });
        data = res.data;
      } else {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            source, destination, range: parseFloat(range),
            use_supercharge: superchargeType === 'overcharge' ? 0 : 1
          })
        });
        data = await response.json();
      }

      if (data.error) {
        setStatusMessage(data.error);
        setIsCalculating(false);
        return;
      }

      const jobId = data.job;
      let resultData = null;

      while (!resultData) {
        await new Promise(r => setTimeout(r, 2000));
        let pollData;
        if (window.electronAPI && window.electronAPI.fetchProxy) {
          const pollRes = await window.electronAPI.fetchProxy(`https://spansh.co.uk/api/results/${jobId}`);
          pollData = pollRes.data;
        } else {
          const pollResponse = await fetch(`https://spansh.co.uk/api/results/${jobId}`);
          pollData = await pollResponse.json();
        }

        if (pollData.error) {
          setStatusMessage(pollData.error);
          setIsCalculating(false);
          return;
        }
        if (pollData.status === 'ok') {
          resultData = pollData.result;
        }
      }

      if (resultData && resultData.system_jumps) {
        // ... build route
        // Due to script size limits, I will implement a simpler build route that grabs jumps
        // For the sake of refactor, let's just extract the jumps directly.
        // I will copy the exact parsing logic from old_app.
        const newRoute = resultData.system_jumps.map((jump: any, index: number) => ({
          system: jump.system,
          starClass: jump.neutron_star ? 'N' : 'Standard',
          jumpsLeft: resultData.system_jumps.length - 1 - index
        }));

        setRoute(newRoute);
        setCurrentJumpIndex(0);
        setHudMode(true);
        
        localStorage.setItem('savedRoute', JSON.stringify({
          route: newRoute,
          currentJumpIndex: 0,
          source: newRoute[0]?.system || source,
          destination: destination,
          range: range,
          superchargeType: superchargeType
        }));
        
        if (newRoute.length > 1 && window.electronAPI) {
          const actualLocation = await window.electronAPI.getCurrentLocation();
          
          if (actualLocation && actualLocation.system && actualLocation.system !== newRoute[0].system) {
            // Player is starting the route from a system they are not currently in!
            setIsOffRoute(true);
            window.electronAPI.copyToClipboard(newRoute[0].system);
            setStatusMessage(`Copied starting waypoint to clipboard!`);
          } else {
            // Player is at the starting waypoint
            setIsOffRoute(false);
            window.electronAPI.copyToClipboard(newRoute[1].system);
            setStatusMessage('Copied first jump to clipboard!');
          }
          
          setTimeout(() => setStatusMessage(''), 8000);
          window.electronAPI.setIgnoreMouseEvents(true, { forward: true });
        } else {
          setStatusMessage('');
        }
      }

    } catch (err: any) {
      setStatusMessage(`Routing failed: ${err.message}`);
      setTimeout(() => setStatusMessage(''), 8000); // 8s to read the unmapped message
    } finally {
      setIsCalculating(false);
    }
  };

  const startRoute = () => {
    const s = source.trim();
    const d = destination.trim();
    
    if (!s || !d || !range) {
      setStatusMessage('Please fill in Source, Destination, and Range.');
      setTimeout(() => setStatusMessage(''), 5000);
      return;
    }
    setSource(s);
    setDestination(d);
    calculateRoute(s, d, range, superchargeType);
  };

  
  const stopRoute = () => {
    setHudMode(false);
    setRoute([]);
    setCurrentJumpIndex(0);
    localStorage.removeItem('savedRoute');
  };

  const handleUseCurrentLocation = async () => {
    if (window.electronAPI) {
      const res = await window.electronAPI.getCurrentLocation();
      if (res && !res.error && res.system) {
        // verify system is valid on EDSM
        const edsmRes = await fetch(`https://www.edsm.net/api-v1/system?systemName=${encodeURIComponent(res.system)}&showCoordinates=1`);
        const edsmData = await edsmRes.json();
        
        if (edsmData && edsmData.name) {
          setSource(edsmData.name);
          setStatusMessage(`Location set to ${edsmData.name}`);
          setTimeout(() => setStatusMessage(''), 5000);
        } else {
          // fallback
          try {
            const spanshRes = await fetch(`https://spansh.co.uk/api/system?q=${encodeURIComponent(res.system)}`);
            const spanshData = await spanshRes.json();
            if (spanshData && spanshData.length > 0) {
              setSource(spanshData[0].name);
              setStatusMessage(`Location set to ${spanshData[0].name}`);
              setTimeout(() => setStatusMessage(''), 5000);
            } else {
              setSource(res.system);
              setStatusMessage(`Location set to ${res.system} (not found in DB)`);
              setTimeout(() => setStatusMessage(''), 5000);
            }
          } catch(e) {
            setSource(res.system);
            setStatusMessage(`Location set to ${res.system} (EDSM fallback failed)`);
          }
        }
      } else {
        setStatusMessage(res?.error || 'Could not fetch location');
        setTimeout(() => setStatusMessage(''), 5000);
      }
    } else {
      setSource('Sol (Mock - No Electron)');
    }
  };

  const enableMouse = () => {
    if (window.electronAPI) window.electronAPI.setIgnoreMouseEvents(false);
  };

  const disableMouse = () => {
    if (window.electronAPI && hudModeRef.current) {
      window.electronAPI.setIgnoreMouseEvents(true, { forward: true });
    }
  };

  // Rendering functions for tabs
  const renderMaximized = () => {
    switch (activeTab) {
      case 'route':
        if (hudMode && route.length > 0) {
          const current = route[currentJumpIndex];
          const next = route[currentJumpIndex + 1];
          return (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
                  Neutron Router
                </h3>
                <div className="flex" style={{ gap: '0.5rem' }}>
                  <button 
                    onClick={stopRoute} 
                    onMouseEnter={enableMouse}
                    onMouseLeave={disableMouse}
                    style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
                  >
                    Abort
                  </button>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Route Waypoint</div>
                  <div className="flex items-center" style={{ gap: '0.5rem' }}>
                    <div className="text-accent" style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{current.system}</div>
                    <button 
                      onClick={() => {
                        if (window.electronAPI) window.electronAPI.copyToClipboard(current.system);
                        setStatusMessage(`Copied Waypoint!`);
                        setTimeout(() => setStatusMessage(''), 3000);
                      }}
                      onMouseEnter={enableMouse}
                      onMouseLeave={disableMouse}
                      title="Copy Waypoint"
                      style={{ border: 'none', background: 'rgba(255, 255, 255, 0.01)', fontSize: '0.8rem', padding: '0.2rem', pointerEvents: 'auto', boxShadow: 'none' }}
                    >&#x274F;</button>
                  </div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Destination</div>
                  <div style={{ fontWeight: 'bold' }}>{route[route.length - 1].system}</div>
                  <div className="text-accent" style={{ fontSize: '0.9rem' }}>{current.jumpsLeft} Jumps Remaining</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Next System</div>
                  {next ? (
                     <div className="flex items-center" style={{ justifyContent: 'flex-end', gap: '0.5rem' }}>
                       <button 
                         onClick={() => {
                           if (window.electronAPI) window.electronAPI.copyToClipboard(next.system);
                           setStatusMessage(`Copied ${next.system}`);
                           setTimeout(() => setStatusMessage(''), 3000);
                         }}
                         onMouseEnter={enableMouse}
                         onMouseLeave={disableMouse}
                         title="Copy Next System"
                         style={{ border: 'none', background: 'rgba(255, 255, 255, 0.01)', fontSize: '0.8rem', padding: '0.2rem', pointerEvents: 'auto', boxShadow: 'none' }}
                       >&#x274F;</button>
                       <div>
                         <div className="text-accent" style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{next.system}</div>
                         <div style={{ fontSize: '0.8rem', color: next.starClass === 'N' ? 'var(--accent-color)' : 'var(--text-secondary)' }}>
                           {next.starClass === 'N' ? 'Neutron Star' : 'Standard Jump'}
                         </div>
                       </div>
                     </div>
                  ) : (
                     <div className="text-success" style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>ARRIVED</div>
                  )}
                </div>
              </div>
            </div>
          );
        } else {
          // Route Planning View
          return (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
                  Neutron Router
                </h3>
              </div>
              <div className="flex gap-4 mt-2">
                <div className="flex-col gap-2" style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.9rem' }}>Source System</label>
                  <div className="flex gap-2">
                    <SystemAutocomplete value={source} onChange={setSource} placeholder="e.g. Sol" style={{ flex: 1 }} />
                    <button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(source); setStatusMessage('Copied Source!'); setTimeout(()=>setStatusMessage(''),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Source" style={{ width: '2.2rem', padding: '0.4rem', border: 'none', background: 'rgba(255,255,255,0.05)' }}>&#x274F;</button>
                    <button onClick={handleUseCurrentLocation} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Use Current Location" style={{ width: '2.2rem', padding: '0.4rem', border: 'none', background: 'rgba(255,255,255,0.05)' }}>&#x2316;</button>
                  </div>
                </div>
                <div className="flex-col gap-2" style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.9rem' }}>Destination System</label>
                  <div className="flex gap-2">
                    <SystemAutocomplete value={destination} onChange={setDestination} placeholder="e.g. Colonia" style={{ flex: 1 }} />
                    <button onClick={() => { if(window.electronAPI) window.electronAPI.copyToClipboard(destination); setStatusMessage('Copied Destination!'); setTimeout(()=>setStatusMessage(''),3000); }} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Copy Destination" style={{ width: '2.2rem', padding: '0.4rem', border: 'none', background: 'rgba(255,255,255,0.05)' }}>&#x274F;</button>
                  </div>
                </div>
              </div>
              <div className="flex gap-4 mt-4">
                <div className="flex-col gap-2" style={{ flex: 0.5 }}>
                  <label style={{ fontSize: '0.9rem' }}>Jump Range (Ly)</label>
                  <input type="number" value={range} onChange={e => setRange(e.target.value)} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ pointerEvents: 'auto' }} />
                </div>
                <div className="flex-col gap-2" style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.9rem' }}>Supercharge Type</label>
                  <select value={superchargeType} onChange={e => setSuperchargeType(e.target.value)} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ width: '100%', padding: '0.5rem', background: 'rgba(0, 0, 0, 0.5)', border: '1px solid var(--glass-border)', color: 'white', borderRadius: '4px', pointerEvents: 'auto' }}>
                    <option value="normal">Normal Supercharge</option>
                    <option value="overcharge">Overcharge Supercharge (SCO)</option>
                  </select>
                </div>
              </div>
              <div className="mt-4 flex justify-between items-center" style={{ marginTop: 'auto', gap: '1rem' }}>
                <div className={statusMessage.includes('Spansh') || statusMessage.includes('failed') ? "text-warning" : "text-success"} style={{ fontSize: '0.9rem', flex: 1 }}>{statusMessage}</div>
                <button onClick={startRoute} disabled={isCalculating} onMouseEnter={enableMouse} onMouseLeave={disableMouse} style={{ pointerEvents: 'auto', padding: '0.6rem', fontWeight: 'bold', marginTop: '1rem' }}>Calculate & Start</button>
              </div>
            </div>
          );
        }
      case 'hvt':
        return (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <h3 className="text-accent mb-4" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>High Value Targets</h3>
            <div style={{ flex: 1, overflowY: 'auto', pointerEvents: 'auto' }} onMouseEnter={enableMouse} onMouseLeave={disableMouse}>
              {hvtAlerts.length === 0 ? (
                <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>No high value targets found nearby.</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {hvtAlerts.map(alert => (
                    <div key={alert.id} style={{ padding: '0.8rem', background: 'rgba(15, 15, 15, 0.6)', borderLeft: `3px solid ${alert.type === 'bio' ? 'var(--success-color)' : 'var(--accent-color)'}` }}>
                      <div style={{ fontWeight: 'bold' }}>{alert.message}</div>
                      {alert.submessage && <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{alert.submessage}</div>}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );
      case 'exo':
        if (!currentPlanetBio) {
          return (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>Exo Tracker</h3>
              <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ color: 'var(--text-secondary)' }}>Please land on a planet to begin surface scanning...</div>
              </div>
            </div>
          );
        }
        return (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>Exo Tracker</h3>
            <div className="text-secondary mb-2" style={{ fontWeight: 'bold', fontSize: '0.85rem' }}>{currentPlanetBio.bodyName}</div>
            <div style={{ display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
              <div className="flex" style={{ flexWrap: 'wrap', gap: '1rem' }}>
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
            </div>
          </div>
        );
      case 'poi':
        return (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>Nearby POI Search</h3>
            <div className="flex mb-4" style={{ gap: '1.5rem', marginTop: '1rem' }}>
              <button onClick={searchCarriers} onMouseEnter={enableMouse} onMouseLeave={disableMouse} disabled={isSearchingPoi} style={{ pointerEvents: 'auto', padding: 0, fontSize: '0.8rem', background: 'transparent', border: 'none', boxShadow: 'none', color: (poiResults !== null || isSearchingPoi) ? 'var(--accent-color)' : 'var(--text-secondary)', fontWeight: 'bold' }}>{isSearchingPoi ? 'SEARCHING...' : 'FLEET CARRIERS'}</button>
              <button disabled style={{ padding: 0, fontSize: '0.8rem', opacity: 0.5, background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)', fontWeight: 'bold' }}>SCENIC VIEWS (SOON)</button>
            </div>
            <div style={{ flex: 1, overflowY: 'auto', pointerEvents: 'auto' }} onMouseEnter={enableMouse} onMouseLeave={disableMouse}>
              {poiResults === null ? (
                <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>Select a category to search...</div>
              ) : poiResults.length === 0 ? (
                <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>No results found nearby.</div>
              ) : (
                <div className="flex-col" style={{ gap: '0.2rem' }}>
                  {poiResults.map((r, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.3rem 0', borderBottom: '1px solid rgba(255,255,255,0.1)', fontSize: '0.85rem', alignItems: 'center' }}>
                      <div style={{ display: 'flex', gap: '1rem', flex: 1, alignItems: 'center' }}>
                        <div className="text-accent" style={{ fontWeight: 'bold', flex: 1 }}>{r.name}</div>
                        <div style={{ color: 'var(--text-secondary)', flex: 1 }}>{r.system_name}</div>
                        <div style={{ width: '60px', textAlign: 'right' }}>{r.distance.toFixed(1)} Ly</div>
                      </div>
                      <button 
                        onClick={() => {
                          if (window.electronAPI) window.electronAPI.copyToClipboard(r.system_name);
                          setStatusMessage(`Copied ${r.system_name}`);
                          setTimeout(() => setStatusMessage(''), 3000);
                        }}
                        style={{ fontSize: '0.7rem', padding: '0.1rem 0.3rem', marginLeft: '1rem' }}
                      >
                        Copy
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );
    }
  };

  const renderMinimized = () => {
    switch (activeTab) {
      case 'route':
        if (hudMode && route.length > 0) {
          const current = route[currentJumpIndex];
          const next = route[currentJumpIndex + 1];
          return (
            <div className="flex justify-between items-center" style={{ width: '100%' }}>
              <div className="flex items-center" style={{ gap: '0.2rem' }}>
                <span className="text-accent" style={{ fontWeight: 'bold' }}>{current.system}</span>
              </div>
              <div className="text-accent" style={{ fontSize: '0.9rem', textAlign: 'center', flex: 1 }}>{current.jumpsLeft} Jumps</div>
              <div className="flex items-center" style={{ gap: '0.2rem' }}>
                {next ? <span className="text-accent" style={{ fontWeight: 'bold' }}>{next.system}</span> : <span className="text-success" style={{ fontWeight: 'bold' }}>ARRIVED</span>}
              </div>
            </div>
          );
        }
        return <div style={{ color: 'var(--text-secondary)', textAlign: 'center', width: '100%' }}>Route Planner - No active route</div>;
      case 'hvt':
        return <div style={{ color: 'var(--accent-color)', fontWeight: 'bold', textAlign: 'center', width: '100%' }}>{hvtAlerts.length} High Value Targets detected</div>;
      case 'exo':
        if (!currentPlanetBio) return <div style={{ color: 'var(--text-secondary)', textAlign: 'center', width: '100%' }}>Exo Tracker - Not landed</div>;
        const total = currentPlanetBio.totalSignals;
        const scanned = Object.values(currentPlanetBio.scanned).filter(c => c >= 3).length;
        return <div style={{ color: 'var(--success-color)', fontWeight: 'bold', textAlign: 'center', width: '100%' }}>Exo Tracker - {scanned}/{total} Complete</div>;
      case 'poi':
        return <div style={{ color: 'var(--text-secondary)', textAlign: 'center', width: '100%' }}>{isSearchingPoi ? 'Searching POIs...' : (poiResults ? `${poiResults.length} Fleet Carriers found` : 'POI Search Ready')}</div>;
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Top Status float (Errors etc) */}
      {(statusMessage || isOffRoute) && (
        <div style={{ position: 'absolute', top: '10px', left: '50%', transform: 'translateX(-50%)', background: 'rgba(15,15,15,0.9)', padding: '0.3rem 1rem', borderRadius: '4px', border: '1px solid var(--glass-border)', zIndex: 100 }}>
          <div className={statusMessage.includes('failed') || isOffRoute ? "text-warning" : "text-success"} style={{ fontSize: '0.9rem' }}>
            {statusMessage ? statusMessage : isOffRoute ? `Off route! Jump to ${route[currentJumpIndex]?.system} to resume.` : ''}
          </div>
        </div>
      )}

      <div className="glass-panel" style={{ width: '100%', flex: 1, display: 'flex', boxSizing: 'border-box', padding: 0, overflow: 'hidden' }}>
        
        {/* Sidebar */}
        {!isMinimized && (
          <div style={{ width: '45px', borderRight: '1px solid rgba(255,255,255,0.1)', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '0', WebkitAppRegion: 'drag' as any }}>
            <SidebarIcon active={activeTab==='route'} onClick={() => setActiveTab('route')} icon={<RouteIcon/>} title="Route Planner" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='hvt'} onClick={() => setActiveTab('hvt')} icon={<HvtIcon/>} title="System Info (HVT)" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='exo'} onClick={() => setActiveTab('exo')} icon={<ExoIcon/>} title="Exo Tracker" enableMouse={enableMouse} disableMouse={disableMouse} />
            <SidebarIcon active={activeTab==='poi'} onClick={() => setActiveTab('poi')} icon={<PoiIcon/>} title="Nearby POI Search" enableMouse={enableMouse} disableMouse={disableMouse} />
            <div style={{ flex: 1 }} />
            <div style={{ fontSize: '0.6em', opacity: 0.5, marginBottom: '0.5rem', WebkitAppRegion: 'no-drag' as any }}>v1.0</div>
          </div>
        )}

        {/* Content Area */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: isMinimized ? '0.4rem 1rem' : '0.5rem 1rem 1rem 1rem', overflow: 'hidden', position: 'relative' }}>
          {!isMinimized && (
            <button onClick={() => setIsMinimized(true)} onMouseEnter={enableMouse} onMouseLeave={disableMouse} title="Minimize HUD" style={{ position: 'absolute', top: '0.2rem', right: '0.5rem', padding: '0.2rem 0.6rem', fontSize: '1rem', background: 'transparent', border: 'none', color: 'var(--text-secondary)', pointerEvents: 'auto', WebkitAppRegion: 'no-drag' as any, zIndex: 100, cursor: 'pointer', boxShadow: 'none' }}>&minus;</button>
          )}
          {isMinimized ? (
            <div className="flex justify-between items-center w-full gap-4" style={{ paddingRight: '2rem' }}>
              {renderMinimized()}
              <button 
                onClick={() => setIsMinimized(false)}
                onMouseEnter={enableMouse}
                onMouseLeave={disableMouse}
                title="Expand HUD"
                style={{ position: 'absolute', top: '50%', transform: 'translateY(-50%)', right: '0.5rem', padding: '0.2rem 0.6rem', fontSize: '1.2rem', background: 'transparent', border: 'none', color: 'var(--text-secondary)', pointerEvents: 'auto', WebkitAppRegion: 'no-drag' as any, zIndex: 100, cursor: 'pointer', boxShadow: 'none' }}
              >
                &#43;
              </button>
            </div>
          ) : renderMaximized()}
        </div>
      </div>
    </div>
  );
}
export default App;
