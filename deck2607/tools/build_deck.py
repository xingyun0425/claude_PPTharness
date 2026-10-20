"""Builder for the RSI survey deck (arXiv:2607.07663) on the State Grid reference master.

Usage: python tools/build_deck.py output.pptx
Slides live in ch1.py … ch4.py (one @slide function each, registered in kit.SLIDES);
reusable icons come from art.py. Theme and layout choices follow design_brief.md.
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deckkit import Canvas, IconStore, configure_theme, new_presentation, notes
import art
import kit
import ch1, ch2, ch3, ch3b, ch4  # noqa: F401  (registers slides in order)

HERE = Path(__file__).resolve().parent.parent
THEME = {
    'colors': dict(navy='064E41', blue='008380', gold='0E6767', rose='C00000', darkRose='9E1B1B',
                   pale='EFF7F7', zone='ECF6F6', paleRose='FBE9E9', line='98D1CC', text='1F2D2D',
                   grey='57678F', neutral='8A9A9A', chipGrey='E6E6E6', sky='0070C0'),
    'font': 'Microsoft YaHei',
    'icons': art.ICONS,
}
BASE = str(HERE / 'ref.pptx')        # inherit the reference master: logo, header rule, page number, backdrop
BASE_LAYOUT = '1_标题幻灯片'


def main():
    if len(sys.argv) != 2:
        raise SystemExit('python tools/build_deck.py output.pptx')
    configure_theme(THEME['colors'], THEME.get('font'), THEME.get('icons'))
    output = Path(sys.argv[1])
    prs, _ = new_presentation(BASE, BASE_LAYOUT)
    layouts = {l.name: l for l in prs.slide_layouts}
    problems = {}
    with tempfile.TemporaryDirectory() as tmp:
        icons = IconStore(prs, tmp)
        for number, (lay, fn) in enumerate(kit.SLIDES, 1):
            sld = prs.slides.add_slide(layouts[kit.LAYOUTS[lay]])
            for ph in list(sld.placeholders):
                ph._element.getparent().remove(ph._element)
            cv = Canvas(sld.shapes, icons)
            speaker_notes = fn(cv, number)
            if not speaker_notes or not speaker_notes.strip():
                raise ValueError(f'slide {number}: sourced speaker notes are required')
            notes(sld, speaker_notes)
            found = [' '.join(str(x) for x in issue if x) for issue in cv.overlaps()]
            if found:
                problems[number] = found
            print(f'slide {number}/{len(kit.SLIDES)}: {fn.__name__}' + (f'  ({len(found)} layout finding(s))' if found else ''))
        output.parent.mkdir(parents=True, exist_ok=True)
        prs.save(output)
    record = {'deck_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'source': 'deckkit estimate (PIL font metrics)', 'slides': problems}
    output.with_suffix('.layout.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    for number, found in problems.items():
        for issue in found:
            print(f'  slide {number}: {issue}', file=sys.stderr)
    print(f'saved {output}: {len(kit.SLIDES)} slides; {sum(map(len, problems.values()))} builder layout finding(s)')


if __name__ == '__main__':
    main()
