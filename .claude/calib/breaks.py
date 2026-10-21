"""Where do deckkit's predicted line breaks differ from PowerPoint's, and by how much width?"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.claude/skills/paper-ppt/tools'))
from deckkit import measure

rows = json.loads((Path(__file__).parent / 'results.json').read_text(encoding='utf-8'))
ratios, kinds = [], {'pp_fuller': 0, 'pp_shorter': 0}
for r in rows:
    act = [l for l in r['act'] if l.strip()]
    for line in act[:-1]:                      # every non-final PowerPoint line is "full"
        ratios.append(measure(line.rstrip(), r['pt']) / r['w'])
    p0, a0 = r['pred'][0].strip(), act[0].strip()
    if p0 != a0:
        kinds['pp_fuller' if len(a0) > len(p0) else 'pp_shorter'] += 1
ratios.sort()
print('PowerPoint full-line width / box width: min %.3f  p5 %.3f  median %.3f  max %.3f' %
      (ratios[0], ratios[len(ratios) // 20], ratios[len(ratios) // 2], ratios[-1]))
print('first-line differences:', kinds)
for r in rows[:120]:
    act = [l for l in r['act'] if l.strip()]
    if r['pred'][0].strip() != act[0].strip():
        print(f"pt{r['pt']} w{r['w']}\n  pred: {r['pred'][0]!r} ({measure(r['pred'][0], r['pt']):.0f})"
              f"\n  act : {act[0]!r} ({measure(act[0].rstrip(), r['pt']):.0f})")
        break
