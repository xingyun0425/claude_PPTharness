"""Trial: rebuild slide 5 (1.3 核心区分) without the reference master, in a content-chosen hue.

- No BASE: blank 16:9 deck. Header emblem, header rule, page number and the pale backdrop
  are redrawn with native shapes / new SVG at the reference's positions.
- Colour: the paper is an AI survey (no tie to the power grid), so the reference's teal family
  (hue 169-205) is rotated to indigo; lightness and saturation are kept, so every dark element
  stays dark and every tint stays light. Red emphasis and neutral greys are unchanged.
- Slide content comes unchanged from tools/ch1.core_cut; nothing in tools/ is modified.

Usage: python trial/build_trial.py trial/out/trial.pptx
"""
import colorsys
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import deckkit as dk
from deckkit import Canvas, IconStore, configure_theme, new_presentation, notes

HUE_SHIFT = 50          # 180 (teal) -> 230 (indigo); 205 (second-path blue) -> 255 (violet)
SAT_SCALE = 0.72        # strong teal reads softer than strong blue at equal saturation


def _lum(rgb):
    """WCAG relative luminance: what the eye reads as dark or light."""
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def remap(h):
    """Rotate teal/blue-family colours by HUE_SHIFT and keep each colour's luminance, so
    dark title bands stay as dark and tints stay as light as in the reference."""
    h = h.lstrip('#').upper()
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    hue, light, sat = colorsys.rgb_to_hls(*rgb)
    if not (150 <= hue * 360 <= 215 and sat > 0.1):
        return h
    target, hue = _lum(rgb), (hue + HUE_SHIFT / 360) % 1
    sat = sat * SAT_SCALE if light < 0.8 else sat
    lo, hi = 0.0, 1.0
    for _ in range(40):                       # bisect lightness to match the reference luminance
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _lum(colorsys.hls_to_rgb(hue, mid, sat)) < target else (lo, mid)
    return '%02X%02X%02X' % tuple(round(v * 255) for v in colorsys.hls_to_rgb(hue, lo, sat))


def remap_svg(markup):
    return re.sub(r'#([0-9A-Fa-f]{6})', lambda m: '#' + remap(m.group(1)), markup)


# Every native fill/line/font colour passes through deckkit.rgb; SVG passes through Canvas.svg.
_rgb = dk.rgb
dk.rgb = lambda h: _rgb(remap(h))
_svg = Canvas.svg
Canvas.svg = lambda self, markup, *a, **k: _svg(self, remap_svg(markup), *a, **k)

import art   # noqa: E402  (after the patch; icons are remapped below)
import kit   # noqa: E402
import ch1   # noqa: E402

REF_COLORS = dict(navy='064E41', blue='008380', gold='0E6767', rose='C00000', darkRose='9E1B1B',
                  pale='EFF7F7', zone='ECF6F6', paleRose='FBE9E9', line='98D1CC', text='1F2D2D',
                  grey='57678F', neutral='8A9A9A', chipGrey='E6E6E6', sky='0070C0')
NEW = {k: remap(v) for k, v in REF_COLORS.items()}

# Header emblem drawn for this deck: a recursion loop (3/4 ring + arrowhead) around a core node.
EMBLEM = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 84">'
          f'<circle cx="42" cy="42" r="38" fill="#{NEW["pale"]}" stroke="#{NEW["navy"]}" stroke-width="3"/>'
          f'<path d="M42 16 A26 26 0 1 1 18.5 30.9" fill="none" stroke="#{NEW["blue"]}" stroke-width="6" stroke-linecap="round"/>'
          f'<path d="M11.2 33.6 L27.4 20.6 L28.9 36.3 Z" fill="#{NEW["blue"]}"/>'
          f'<circle cx="42" cy="42" r="9" fill="#{NEW["rose"]}"/></svg>')


def chrome(cv, number):
    """The reference master's furniture, redrawn natively at the same positions."""
    # pale backdrop (reference: faint building photo under the content area, lower left)
    for cx, cy, r, a in ((180, 900, 420, 0.30), (520, 980, 360, 0.22)):
        sp = cv.circle(cx, cy, r, fill=NEW['pale'], name='底纹')
        sf = sp._element.spPr.find(dk.qn('a:solidFill'))
        dk.etree.SubElement(sf[0], dk.qn('a:alpha'), val=str(int(a * 100000)))
    cv.svg(EMBLEM, 26, 21, 84, 84, name='页眉标识')
    cv.line(0, 122, 1600, 122, color=NEW['navy'], lw=1.25, name='页眉线')
    cv.text(str(number), 1580, 881, pt=16, color=NEW['grey'], align='r', name='页码')


def main():
    out = Path(sys.argv[1])
    for k in ('T', 'D', 'P', 'B'):           # module colours used by art.* drawing functions
        setattr(art, k, remap(getattr(art, k)))
    configure_theme(NEW, 'Microsoft YaHei', {k: remap_svg(v) for k, v in art.ICONS.items()})
    prs, layout = new_presentation(None)
    with tempfile.TemporaryDirectory() as tmp:
        icons = IconStore(prs, tmp)
        sld = prs.slides.add_slide(layout)
        cv = Canvas(sld.shapes, icons)
        chrome(cv, 5)
        notes(sld, ch1.core_cut(cv, 5))
        issues = cv.overlaps()
        out.parent.mkdir(parents=True, exist_ok=True)
        prs.save(out)
    print('colour map (reference -> trial):')
    for k, v in REF_COLORS.items():
        if NEW[k] != v:
            print(f'  {k:9s} {v} -> {NEW[k]}')
    print(f'saved {out}; {len(issues)} builder layout finding(s)', *issues, sep='\n  ')


if __name__ == '__main__':
    main()
