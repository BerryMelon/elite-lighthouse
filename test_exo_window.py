
import json
import time
import os
import glob
from pathlib import Path

# Find the latest journal file
home = Path.home()
journal_dir = home / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous'

os.makedirs(journal_dir, exist_ok=True)
files = glob.glob(str(journal_dir / 'Journal.*.01.log'))
if not files:
    latest = str(journal_dir / 'Journal.2026.01.01.01.log')
    with open(latest, 'w') as f:
        f.write('')
else:
    latest = max(files)

print(f'Writing to {latest}')

def write_event(evt):
    with open(latest, 'a') as f:
        f.write(json.dumps(evt) + '\n')
    time.sleep(2)

print('Sending Touchdown...')
write_event({'timestamp': '2026-07-01T00:00:00Z', 'event': 'Touchdown', 'Body': 'Planet X', 'Latitude': 0, 'Longitude': 0})

print('Sending FSSBodySignals...')
write_event({
    'timestamp': '2026-07-01T00:00:00Z', 
    'event': 'FSSBodySignals', 
    'BodyName': 'Planet X', 
    'Signals': [{'Type': 'Biological', 'Count': 5}]
})

print('Scanning first bio...')
write_event({
    'timestamp': '2026-07-01T00:00:00Z', 
    'event': 'ScanOrganic', 
    'ScanType': 'Log', 
    'Species_Localised': 'Stratum Tectonicas'
})

print('Sending LeaveBody...')
write_event({'timestamp': '2026-07-01T00:00:00Z', 'event': 'LeaveBody', 'Body': 'Planet X'})

print('Done!')

