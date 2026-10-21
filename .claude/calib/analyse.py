import json
import statistics
from collections import defaultdict
from pathlib import Path

rows = json.loads((Path(__file__).parent / 'results.json').read_text(encoding='utf-8'))
fpx = lambda pt: pt / 0.6
mismatch = [r for r in rows if len(r['pred']) != len(r['act'])]
fewer = [r for r in mismatch if len(r['pred']) < len(r['act'])]
print(f'line count: {len(rows) - len(mismatch)}/{len(rows)} exact; predicted FEWER lines in {len(fewer)}, more in {len(mismatch) - len(fewer)}')
same_breaks = sum(1 for r in rows if [l.strip() for l in r['pred']] == [l.strip() for l in r['act']])
print(f'identical line breaks: {same_breaks}/{len(rows)}')
for r in fewer[:6]:
    print(f"  pt{r['pt']} w{r['w']}: pred {len(r['pred'])} vs act {len(r['act'])}")
    print('    pred:', ' | '.join(r['pred']))
    print('    act :', ' | '.join(r['act']))

# per-line height actually used by PowerPoint, per (pt, lh)
per = defaultdict(list)
for r in rows:
    n = len(r['act'])
    if n >= 2:
        per[(r['pt'], r['lh'])].append(r['act_h'] / n / fpx(r['pt']))
print('\nactual height per line / font px  (deckkit assumes lh * 1.2):')
for (pt, lh), v in sorted(per.items()):
    print(f'  pt{pt} lh{lh}: {statistics.mean(v):.3f}  (deckkit {lh * 1.2:.3f})  ratio {statistics.mean(v) / (lh * 1.2):.3f}')

over = [r for r in rows if r['act_h'] > r['pred_h'] + 2]
print(f'\nboxes where PowerPoint text is taller than the deckkit box: {len(over)}/{len(rows)}')

# orphans: last actual line of 1-2 chars
orph = [r for r in rows if len(r['act']) > 1 and len(r['act'][-1].strip()) <= 2]
print(f'orphan last lines (<=2 chars) in PowerPoint: {len(orph)}; e.g.', [r['act'][-2:] for r in orph[:4]])
