with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

hydration_effect = """
  useEffect(() => {
    if (isExoMode && window.electronAPI) {
      window.electronAPI.hydrateExo().then((res: any) => {
        if (res && res.bioState) {
          setCurrentPlanetBio(res.bioState);
        }
      });
    }
  }, [isExoMode]);
"""

old_line = "const isExoMode = new URLSearchParams(window.location.search).get('mode') === 'exo';"
new_line = old_line + '\n' + hydration_effect

if hydration_effect not in content:
    content = content.replace(old_line, new_line)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)

print('App.tsx updated!')
