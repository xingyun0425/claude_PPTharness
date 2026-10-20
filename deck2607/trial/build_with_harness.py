"""Slide 5 rebuilt with the harness API only: deckkit.shift_hue / shift_svg_hue and cv.header.

Usage: python trial/build_with_harness.py trial/out/harness.pptx
"""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / '.claude/skills/paper-ppt/tools'))   # current harness deckkit
sys.path.insert(1, str(HERE.parent / 'tools'))                            # this deck's art/kit/ch1
import deckkit as dk
from deckkit import Canvas, IconStore, configure_theme, new_presentation, notes, shift_hue, shift_svg_hue

SHIFT = dict(degrees=50, hue_range=(150, 215), sat_scale=0.72)   # teal family -> indigo
_rgb, _svg = dk.rgb, Canvas.svg
dk.rgb = lambda h: _rgb(shift_hue(h, **SHIFT))                    # hex literals inside kit/ch1
Canvas.svg = lambda self, m, *a, **k: _svg(self, shift_svg_hue(m, **SHIFT), *a, **k)

import art, ch1  # noqa: E402

REF = dict(navy='064E41', blue='008380', gold='0E6767', rose='C00000', darkRose='9E1B1B', pale='EFF7F7',
           zone='ECF6F6', paleRose='FBE9E9', line='98D1CC', text='1F2D2D', grey='57678F',
           neutral='8A9A9A', chipGrey='E6E6E6', sky='0070C0')
NEW = {k: shift_hue(v, **SHIFT) for k, v in REF.items()}
EMBLEM = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 84">'
          f'<circle cx="42" cy="42" r="38" fill="#{NEW["pale"]}" stroke="#{NEW["navy"]}" stroke-width="3"/>'
          f'<path d="M42 16 A26 26 0 1 1 18.5 30.9" fill="none" stroke="#{NEW["blue"]}" stroke-width="6" stroke-linecap="round"/>'
          f'<path d="M11.2 33.6 L27.4 20.6 L28.9 36.3 Z" fill="#{NEW["blue"]}"/>'
          f'<circle cx="42" cy="42" r="9" fill="#{NEW["rose"]}"/></svg>')

out = Path(sys.argv[1])
for k in ('T', 'D', 'P', 'B'):
    setattr(art, k, shift_hue(getattr(art, k), **SHIFT))
configure_theme(NEW, 'Microsoft YaHei', {k: shift_svg_hue(v, **SHIFT) for k, v in art.ICONS.items()})
prs, layout = new_presentation(None)
with tempfile.TemporaryDirectory() as tmp:
    sld = prs.slides.add_slide(layout)
    cv = Canvas(sld.shapes, IconStore(prs, tmp))
    # coordinates from reference_audit.json -> layouts['1_标题幻灯片'].decorations
    cv.header(5, rule=(0, 1600, 122, NEW['navy'], 1.25), emblem=(EMBLEM, 26, 21, 84, 84),
              backdrop=[(180, 900, 420, NEW['pale'], 0.30), (520, 980, 360, NEW['pale'], 0.22)])
    notes(sld, ch1.core_cut(cv, 5))
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
print('saved', out, '| findings:', len(cv.overlaps()))
