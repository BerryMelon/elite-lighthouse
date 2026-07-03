import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

state_additions = """  const [statusMessage, setStatusMessage] = useState('');
  const [poiMenuOpen, setPoiMenuOpen] = useState(false);
  const [isSearchingPoi, setIsSearchingPoi] = useState(false);
  const [poiResults, setPoiResults] = useState<{name: string, system_name: string, distance: number}[] | null>(null);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setPoiMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [searchRef]);

  const searchCarriers = async () => {
    if (!destination) {
      setStatusMessage('Please enter a destination system first.');
      setPoiMenuOpen(false);
      return;
    }
    setPoiMenuOpen(false);
    setIsSearchingPoi(true);
    try {
      const response = await fetch('https://spansh.co.uk/api/stations/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          filters: { type: { value: ["Drake-Class Carrier"] } },
          sort: [{ distance: { direction: "asc" } }],
          reference_system: destination
        })
      });
      const data = await response.json();
      if (data && data.results) {
        setPoiResults(data.results.slice(0, 15).map((r: any) => ({
          name: r.name,
          system_name: r.system_name,
          distance: r.distance
        })));
      } else {
        setPoiResults([]);
      }
    } catch (err) {
      console.error(err);
      setStatusMessage('Failed to fetch carriers.');
      setPoiResults([]);
    } finally {
      setIsSearchingPoi(false);
    }
  };"""

content = content.replace("  const [statusMessage, setStatusMessage] = useState('');", state_additions)

old_dest_buttons = """            <button 
              onClick={() => {
                if (window.electronAPI && destination) {
                  window.electronAPI.copyToClipboard(destination);
                  setStatusMessage('Copied Destination!');
                  setTimeout(() => setStatusMessage(''), 3000);
                }
              }} 
              title="Copy Destination"
            >&#x274F;</button>
          </div>"""

new_dest_buttons = """            <button 
              onClick={() => {
                if (window.electronAPI && destination) {
                  window.electronAPI.copyToClipboard(destination);
                  setStatusMessage('Copied Destination!');
                  setTimeout(() => setStatusMessage(''), 3000);
                }
              }} 
              title="Copy Destination"
            >&#x274F;</button>
            <div style={{ position: 'relative' }} ref={searchRef}>
              <button onClick={() => setPoiMenuOpen(!poiMenuOpen)} title="Search POI" style={{ height: '100%' }}>&#x2630;</button>
              {poiMenuOpen && (
                <div className="glass-panel" style={{ position: 'absolute', top: '100%', right: 0, marginTop: '0.2rem', padding: '0.5rem', background: 'rgba(20, 25, 35, 0.95)', border: '1px solid var(--accent-color)', borderRadius: '4px', zIndex: 100, minWidth: '150px' }}>
                  <div 
                    onClick={searchCarriers}
                    style={{ padding: '0.4rem', cursor: 'pointer', borderBottom: '1px solid rgba(255,255,255,0.1)', fontSize: '0.85rem' }}
                  >
                    Nearby Fleet Carriers
                  </div>
                  <div 
                    style={{ padding: '0.4rem', color: 'var(--text-secondary)', fontSize: '0.85rem', fontStyle: 'italic' }}
                    title="Scenic views search coming soon"
                  >
                    Scenic views (Soon)
                  </div>
                </div>
              )}
            </div>
          </div>"""

content = content.replace(old_dest_buttons, new_dest_buttons)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Applied state and dropdown logic.')
