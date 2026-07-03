with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_header = """<div className={`flex justify-between items-center ${isExoMinimized ? '' : 'mb-1'}`} style={isExoMinimized ? {} : { borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.3rem' }}>"""
new_header = """<div className={`flex justify-between items-center ${isExoMinimized ? '' : 'mb-1'}`} style={{ borderBottom: isExoMinimized ? 'none' : '1px solid rgba(255,255,255,0.1)', paddingBottom: isExoMinimized ? '0' : '0.3rem' }}>"""

if old_header in content:
    content = content.replace(old_header, new_header)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed exo header border explicitly.')
else:
    print('Error: Could not find old_header.')
