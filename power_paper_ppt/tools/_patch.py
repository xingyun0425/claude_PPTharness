import sys

path = sys.argv[1]
pairs = []
cur = None
for line in open(sys.argv[2], encoding='utf-8').read().split('\n'):
    if line == '<<<OLD':
        cur = ['', '']; mode = 0
    elif line == '===NEW':
        mode = 1
    elif line == '>>>END':
        pairs.append((cur[0][:-1], cur[1][:-1])); cur = None
    elif cur is not None:
        cur[mode] += line + '\n'
s = open(path, encoding='utf-8').read()
for old, new in pairs:
    if old not in s:
        if new in s:
            continue
        raise SystemExit(f'NOT FOUND:\n{old}')
    s = s.replace(old, new, 1)
open(path, 'w', encoding='utf-8').write(s)
print(f'{path}: {len(pairs)} edit(s)')
