"""Score a wrap rule against PowerPoint's actual line breaks (results.json from calibrate_text.py).

PowerPoint's wrapping does not depend on the box height, so candidate rules can be scored offline.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.claude/skills/paper-ppt/tools'))
import deckkit as dk

rows = json.loads((Path(__file__).parent / 'results.json').read_text(encoding='utf-8'))
OPEN = set('（《“‘「【(')


def wrap(s, pt, width, fill, keep_open):
    lines, cur = [], ''
    for t in dk._TOKEN.findall(s):
        if dk.measure(cur + t, pt, False) > width * fill and cur.strip() and t not in dk._NO_BREAK_BEFORE:
            carry = ''
            while keep_open and cur and cur[-1] in OPEN:
                carry, cur = cur[-1] + carry, cur[:-1]
            lines.append(cur.rstrip())
            cur = carry + t.lstrip()
        else:
            cur += t
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def score(fill, keep_open):
    exact = fewer = more = 0
    for r in rows:
        act = [l.strip() for l in r['act'] if l.strip()]
        pred = [l.strip() for l in wrap(r['text'], r['pt'], r['w'], fill, keep_open)]
        exact += pred == act
        fewer += len(pred) < len(act)
        more += len(pred) > len(act)
    return exact, fewer, more


print(f'{len(rows)} PowerPoint paragraphs')
for fill in (0.97, 0.99, 1.0, 1.01):
    for keep_open in (False, True):
        e, f, m = score(fill, keep_open)
        print(f'fill {fill:.2f} keep-open-bracket {keep_open!s:5}: identical breaks {e:3d}, '
              f'line count too FEW {f:2d} (clipping risk), too many {m:2d}')
