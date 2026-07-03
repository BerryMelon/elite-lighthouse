import re

with open('rewrite_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the search patterns to match the current App.tsx
code = code.replace(
    "start_route_idx = old_app.find('const jumps = resultData.system_jumps.map')",
    "start_route_idx = old_app.find('const newRoute = result.system_jumps.map')"
)

code = code.replace(
    "start_route_idx = old_app.rfind('// Wait for the job', 0, start_route_idx)",
    "start_route_idx = old_app.rfind('const calculateRoute = async', 0, start_route_idx)"
)

# And fix the input file path
code = code.replace(r"C:\Users\chund\.gemini\antigravity\brain\2b49ac0d-c011-433f-97ba-cc39f0044bff\scratch\App_backup.tsx", "src/App.tsx")

with open('rewrite_app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated rewrite_app.py')
