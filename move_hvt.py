with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_style = "position: 'fixed', top: '1rem', right: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', zIndex: 1000, pointerEvents: 'none'"
new_style = "display: 'flex', flexDirection: 'column', gap: '0.5rem', pointerEvents: 'none', marginTop: '0.5rem', alignItems: 'flex-start'"

if old_style in content:
    content = content.replace(old_style, new_style)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('HVT position updated successfully!')
else:
    print('Error: Could not find old_style string in App.tsx.')
