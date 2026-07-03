import json
log_path = r'C:\Users\chund\.gemini\antigravity\brain\2b49ac0d-c011-433f-97ba-cc39f0044bff\.system_generated\logs\transcript_full.jsonl'
lines = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        lines.append(line)

found_step = -1
for i, line in enumerate(lines):
    if "Let's unify all the panels" in line:
        found_step = i
        break

if found_step != -1:
    print('Found at step index', found_step)
    for j in range(found_step + 1, min(len(lines), found_step + 150)):
        entry = json.loads(lines[j])
        if entry.get('source') == 'MODEL' and 'tool_calls' in entry:
            for call in entry['tool_calls']:
                if call['name'] == 'write_to_file':
                    target = call['args'].get('TargetFile', '')
                    print('Wrote to:', target)
                    if target.endswith('.py') and 'rewrite' in target.lower():
                        print('Found rewrite script:', target)
                        with open(target, 'w', encoding='utf-8') as out:
                            out.write(call['args']['CodeContent'])
