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

function App() {
  const [hudMode, setHudMode] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const hudModeRef = useRef(hudMode);
  
  useEffect(() => {
    hudModeRef.current = hudMode;
  }, [hudMode]);

  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  
  const [range, setRange] = useState(() => localStorage.getItem('shipRange') || '50');
  const [superchargeType, setSuperchargeType] = useState(() => localStorage.getItem('superchargeType') || 'normal');

  useEffect(() => {
    localStorage.setItem('shipRange', range);
  }, [range]);

  useEffect(() => {
    localStorage.setItem('superchargeType', superchargeType);
  }, [superchargeType]);

  // Real route state
  const [route, setRoute] = useState<{system: string, starClass: string, jumpsLeft: number}[]>([]);
  const [currentJumpIndex, setCurrentJumpIndex] = useState(0);

  useEffect(() => {
    const savedRouteData = localStorage.getItem('savedRoute');
    if (savedRouteData) {
      try {
        const parsed = JSON.parse(savedRouteData);
        if (parsed.route && parsed.route.length > 0) {
          setRoute(parsed.route);
          setCurrentJumpIndex(parsed.currentJumpIndex || 0);
          setSource(parsed.source || '');
          setDestination(parsed.destination || '');
          setHudMode(true);
        }
      } catch (e) {
        localStorage.removeItem('savedRoute');
      }
    }
  }, []);

  const [statusMessage, setStatusMessage] = useState('');
  const [isCalculating, setIsCalculating] = useState(false);

  const [isOffRoute, setIsOffRoute] = useState(false);

  // Handle FSDJump events from Electron
  useEffect(() => {
    if (hudMode && window.electronAPI) {
      window.electronAPI.onFsdJump((data: any) => {
        const expectedCurrent = route[currentJumpIndex];
        const expectedNext = route[currentJumpIndex + 1];
        
        if (expectedNext && data.StarSystem === expectedNext.system) {
          // Normal progression
          setIsOffRoute(false);
          const newIndex = currentJumpIndex + 1;
          setCurrentJumpIndex(newIndex);
          
          const savedStr = localStorage.getItem('savedRoute');
          if (savedStr) {
            try {
              const savedObj = JSON.parse(savedStr);
              savedObj.currentJumpIndex = newIndex;
              localStorage.setItem('savedRoute', JSON.stringify(savedObj));
            } catch(e) {}
          }
          
          const newNext = route[newIndex + 1];
          if (newNext) {
            window.electronAPI.copyToClipboard(newNext.system);
            setStatusMessage(`Arrived at ${data.StarSystem}. Copied ${newNext.system} to clipboard!`);
          } else {
            setStatusMessage(`Arrived at final destination: ${data.StarSystem}!`);
          }
        } else if (expectedCurrent && data.StarSystem === expectedCurrent.system) {
          // Player returned to the expected current system (getting back on route)
          setIsOffRoute(false);
          if (expectedNext) {
            window.electronAPI.copyToClipboard(expectedNext.system);
            setStatusMessage(`Back on route at ${data.StarSystem}. Copied ${expectedNext.system} to clipboard!`);
          }
        } else {
          // Off route! Advise them to return
          setIsOffRoute(true);
          if (expectedCurrent) {
            window.electronAPI.copyToClipboard(expectedCurrent.system);
            setStatusMessage(`Jumped off route to ${data.StarSystem}. Copied waypoint to clipboard!`);
          }
        }

        setTimeout(() => setStatusMessage(''), 8000);
      });
    }
  }, [hudMode, route, currentJumpIndex]);

  const calculateRoute = async (from: string, to: string, jumpRange: string, sType: string) => {
    setIsCalculating(true);
    setStatusMessage('Calculating route via Spansh...');
    
    try {
      const params = new URLSearchParams();
      params.append('efficiency', '60');
      params.append('range', jumpRange);
      params.append('from', from);
      params.append('to', to);
      // Pass the correct supercharge multiplier based on the selection
      if (sType === 'overcharge') {
        params.append('supercharge_multiplier', '6');
      } else {
        // Normal supercharge is 4x for neutrons
        params.append('supercharge_multiplier', '4');
      }
      
      let data;
      if (window.electronAPI && window.electronAPI.fetchProxy) {
        const res = await window.electronAPI.fetchProxy('https://spansh.co.uk/api/route', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: params.toString()
        });
        if (res.error) throw new Error(res.error);
        data = res.data;
      } else {
        // Fallback for browser testing (will likely fail CORS)
        const res = await fetch('https://spansh.co.uk/api/route', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: params.toString()
        });
        data = await res.json();
      }
      
      if (data.error) {
        if (data.error.includes("Could not find starting system")) {
          throw new Error("Spansh doesn't know your starting system. You might be in an unmapped system!");
        }
        throw new Error(data.error);
      }

      const jobId = data.job;
      let result = null;

      // Poll for results
      while (true) {
        await new Promise(r => setTimeout(r, 2000));
        let dataPoll;
        if (window.electronAPI && window.electronAPI.fetchProxy) {
          const resPoll = await window.electronAPI.fetchProxy(`https://spansh.co.uk/api/results/${jobId}`);
          if (resPoll.error) throw new Error(resPoll.error);
          dataPoll = resPoll.data;
        } else {
          const resPoll = await fetch(`https://spansh.co.uk/api/results/${jobId}`);
          dataPoll = await resPoll.json();
        }
        
        if (dataPoll.status === 'ok') {
          result = dataPoll.result;
          break;
        } else if (dataPoll.status === 'error') {
          throw new Error(dataPoll.error);
        }
      }

      const newRoute = result.system_jumps.map((jump: any, index: number) => ({
        system: jump.system,
        starClass: jump.neutron_star ? 'N' : 'Standard',
        jumpsLeft: result.system_jumps.length - 1 - index
      }));

      setRoute(newRoute);
      setCurrentJumpIndex(0);
      setHudMode(true);
      
      localStorage.setItem('savedRoute', JSON.stringify({
        route: newRoute,
        currentJumpIndex: 0,
        source: newRoute[0]?.system || source,
        destination: destination
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
    setStatusMessage('');
    localStorage.removeItem('savedRoute');
    if (window.electronAPI) {
      setTimeout(() => window.electronAPI.setIgnoreMouseEvents(false), 50);
    }
  };

  const handleUseCurrentLocation = async () => {
    if (window.electronAPI) {
      setStatusMessage('Fetching current location...');
      const res = await window.electronAPI.getCurrentLocation();
      
      if (res && res.system) {
        let isKnown = false;
        try {
          const checkRes = await window.electronAPI.fetchProxy(`https://spansh.co.uk/api/systems?q=${encodeURIComponent(res.system)}`);
          if (checkRes.data && checkRes.data.some((s: string) => s.toLowerCase() === res.system.toLowerCase())) {
            isKnown = true;
          }
        } catch (e) {}

        if (isKnown) {
          setSource(res.system);
          setStatusMessage(`Location set to ${res.system}`);
          setTimeout(() => setStatusMessage(''), 3000);
        } else if (res.pos) {
          setStatusMessage(`System unknown to Spansh. Searching EDSM for nearest...`);
          try {
            const [x, y, z] = res.pos;
            const edsmRes = await window.electronAPI.fetchProxy(`https://www.edsm.net/api-v1/sphere-systems?x=${x}&y=${y}&z=${z}&radius=50`);
            
            let nearest = null;
            if (edsmRes.data && edsmRes.data.length > 0) {
              const sorted = edsmRes.data.sort((a: any, b: any) => a.distance - b.distance);
              nearest = sorted.find((s: any) => s.name.toLowerCase() !== res.system.toLowerCase());
            }
            
            if (nearest) {
              setSource(nearest.name);
              setStatusMessage(`Unknown system. Used nearest known: ${nearest.name} (${nearest.distance.toFixed(1)} Ly)`);
              setTimeout(() => setStatusMessage(''), 8000);
            } else {
              setSource(res.system);
              setStatusMessage(`Location unknown to Spansh and no nearby systems found.`);
              setTimeout(() => setStatusMessage(''), 5000);
            }
          } catch(e) {
            setSource(res.system);
            setStatusMessage(`Location set to ${res.system} (EDSM fallback failed)`);
          }
        } else {
          setSource(res.system);
          setStatusMessage(`Location set to ${res.system} (Unknown, no coordinates available)`);
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

  if (hudMode && route.length > 0) {
    const current = route[currentJumpIndex];
    const next = route[currentJumpIndex + 1];

    return (
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="glass-panel" style={{ width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '0.5rem 1rem' }}>
          
          {isMinimized ? (
            <div className="flex justify-between items-center">
              {/* Waypoint */}
              <div className="flex items-center" style={{ gap: '0.2rem' }}>
                <span className="text-accent" style={{ fontWeight: 'bold' }}>{current.system}</span>
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
                >
                  &#x274F;
                </button>
              </div>

              {/* Jumps */}
              <div className="text-accent" style={{ fontSize: '0.9rem', textAlign: 'center', flex: 1 }}>{current.jumpsLeft} Jumps</div>
              
              {/* Next & Expand */}
              <div className="flex items-center" style={{ gap: '0.2rem' }}>
                {next ? (
                  <>
                    <span className="text-accent" style={{ fontWeight: 'bold' }}>{next.system}</span>
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
                    >
                      &#x274F;
                    </button>
                  </>
                ) : (
                  <span className="text-success" style={{ fontWeight: 'bold' }}>ARRIVED</span>
                )}
                
                <button 
                  onClick={() => setIsMinimized(false)} 
                  onMouseEnter={enableMouse}
                  onMouseLeave={disableMouse}
                  title="Expand"
                  style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto', marginLeft: '0.5rem' }}
                >
                  +
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-accent" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
                  Lighthouse <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>
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
                  <button 
                    onClick={() => setIsMinimized(true)} 
                    onMouseEnter={enableMouse}
                    onMouseLeave={disableMouse}
                    title="Minimize"
                    style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', pointerEvents: 'auto' }}
                  >
                    -
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
                    >
                      &#x274F;
                    </button>
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
                       >
                         &#x274F;
                       </button>
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
            </>
          )}
        </div>
        
        {/* Floating status message outside the glass panel */}
        {(statusMessage || isOffRoute) && (
          <div 
            className="glass-panel" 
            style={{ 
              marginTop: '0.5rem', 
              padding: '0.5rem 1rem', 
              display: 'inline-block',
              alignSelf: 'center',
              pointerEvents: 'none',
              background: 'rgba(15, 15, 15, 0.8)'
            }}
          >
            <div className={isOffRoute && !statusMessage ? "text-warning" : "text-success"} style={{ fontSize: '0.9rem' }}>
              {statusMessage ? (
                <span>&#x2139; {statusMessage}</span>
              ) : isOffRoute ? (
                <span>&#x26A0; Off route! Please jump to {route[currentJumpIndex]?.system} to resume.</span>
              ) : null}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ width: '100%', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column' }}>
      <h3 className="text-accent mb-2" style={{ fontWeight: 600, letterSpacing: '2px', margin: 0, textTransform: 'uppercase', fontSize: '1rem' }}>
        Lighthouse <span style={{ fontSize: '0.6em', opacity: 0.6 }}>v1.0</span>
      </h3>
      
      <div className="flex gap-4 mt-4">
        <div className="flex-col gap-2" style={{ flex: 1 }}>
          <label style={{ fontSize: '0.9rem' }}>Source System</label>
          <div className="flex gap-2">
            <SystemAutocomplete 
              value={source} 
              onChange={setSource} 
              placeholder="e.g. Sol" 
              style={{ flex: 1 }}
            />
            <button 
              onClick={() => {
                if (window.electronAPI && source) {
                  window.electronAPI.copyToClipboard(source);
                  setStatusMessage('Copied Source!');
                  setTimeout(() => setStatusMessage(''), 3000);
                }
              }} 
              title="Copy Source"
            >&#x274F;</button>
            <button onClick={handleUseCurrentLocation} title="Use Current Location">&#x2316;</button>
          </div>
        </div>
        
        <div className="flex-col gap-2" style={{ flex: 1 }}>
          <label style={{ fontSize: '0.9rem' }}>Destination System</label>
          <div className="flex gap-2">
            <SystemAutocomplete 
              value={destination} 
              onChange={setDestination} 
              placeholder="e.g. Colonia" 
              style={{ flex: 1 }}
            />
            <button 
              onClick={() => {
                if (window.electronAPI && destination) {
                  window.electronAPI.copyToClipboard(destination);
                  setStatusMessage('Copied Destination!');
                  setTimeout(() => setStatusMessage(''), 3000);
                }
              }} 
              title="Copy Destination"
            >&#x274F;</button>
          </div>
        </div>
      </div>

      <div className="flex gap-4 mt-4">
        <div className="flex-col gap-2" style={{ flex: 0.5 }}>
          <label style={{ fontSize: '0.9rem' }}>Jump Range (Ly)</label>
          <input 
            type="number" 
            value={range} 
            onChange={e => setRange(e.target.value)} 
            placeholder="e.g. 50" 
          />
        </div>

        <div className="flex-col gap-2" style={{ flex: 1 }}>
          <label style={{ fontSize: '0.9rem' }}>Supercharge Type</label>
          <select 
            value={superchargeType} 
            onChange={e => setSuperchargeType(e.target.value)} 
            style={{ width: '100%', padding: '0.5rem', background: 'rgba(0, 0, 0, 0.5)', border: '1px solid var(--glass-border)', color: 'white', borderRadius: '4px' }}
          >
            <option value="normal">Normal Supercharge</option>
            <option value="overcharge">Overcharge Supercharge (SCO)</option>
          </select>
        </div>
      </div>

      <div className="mt-4 flex justify-between items-center" style={{ marginTop: 'auto', paddingTop: '0.5rem', gap: '1rem' }}>
        <div 
          className={statusMessage.includes('Spansh') || statusMessage.includes('failed') || statusMessage.includes('Please') ? "text-warning" : "text-success"} 
          style={{ fontSize: '0.9rem', flex: 1, wordWrap: 'break-word', lineHeight: '1.2' }}
        >
          {statusMessage}
        </div>
        <button onClick={startRoute} disabled={isCalculating} style={{ flexShrink: 0 }}>Calculate & Start Route</button>
      </div>
    </div>
  );
}

export default App;
