with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old1 = '<div className="glass-panel" style={{ width: \'100%\', height: \'100%\', display: \'flex\', flexDirection: \'column\', alignItems: \'center\', justifyContent: \'center\' }}>'
new1 = '<div className="glass-panel" style={{ width: \'100%\', height: \'100%\', display: \'flex\', flexDirection: \'column\', alignItems: \'center\', justifyContent: \'center\', boxSizing: \'border-box\', padding: \'0.5rem 1rem\' }}>'

old2 = '<div className="glass-panel" style={{ width: \'100%\', height: \'100%\', display: \'flex\', flexDirection: \'column\' }}>'
new2 = '<div className="glass-panel" style={{ width: \'100%\', height: \'100%\', display: \'flex\', flexDirection: \'column\', boxSizing: \'border-box\', padding: \'0.5rem 1rem\' }}>'

if old1 in content:
    content = content.replace(old1, new1)
if old2 in content:
    content = content.replace(old2, new2)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed padding.')
