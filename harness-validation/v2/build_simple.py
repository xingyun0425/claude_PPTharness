"""Minimal builder for harness integration fixture: 2 content slides + icon library."""
import json
import sys
import tempfile
from pathlib import Path

skill_path = Path.home() / '.claude/skills/paper-ppt/tools'
sys.path.insert(0, str(skill_path))
from deckkit import Canvas, IconStore, configure_theme, new_presentation, notes

SLIDES = []
THEME = {
    'colors': {'navy': '0B6E6E', 'blue': '13897F', 'rose': 'C0392B', 'pale': 'E0F7F7'},
    'font': 'Microsoft YaHei',
}
BASE = Path(r'C:\Users\16947\Downloads\claude_trail_2\power_paper_ppt\review\reference\合稿-20260707电力人工智能自主科研引擎方案汇报.pptx')
BASE_LAYOUT = None


def slide(fn):
    SLIDES.append(fn)
    return fn


@slide
def fixture_one(cv, number):
    cv.title('Fixture slide 1')
    cv.para('Verify base master, SVG artwork and native labels', 180, 230, 600, pt=18)
    lock_svg = '<svg viewBox="0 0 24 24"><rect x="7" y="11" width="10" height="9" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 11 v-3 a3 3 0 0 1 6 0 v3" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
    cv.svg(lock_svg, 400, 300, 48, 48)
    return 'Source: synthetic'


@slide
def fixture_two(cv, number):
    cv.title('Fixture slide 2')
    cv.table(180, 200, [120, 120], ['Item', 'Value'], [['A', '100'], ['B', '200']])
    return 'Source: synthetic'


def main():
    if len(sys.argv) != 2 or not SLIDES:
        raise SystemExit('Add real @slide functions, then run: python build_simple.py output.pptx')
    if THEME is None:
        raise SystemExit("Set THEME from this deck's reference analysis before generating")
    configure_theme(THEME['colors'], THEME.get('font'), THEME.get('icons'))
    output = Path(sys.argv[1])
    prs, layout = new_presentation(BASE, BASE_LAYOUT)
    problems = {}
    with tempfile.TemporaryDirectory() as tmp:
        icons = IconStore(prs, tmp)
        for number, fn in enumerate(SLIDES, 1):
            sld = prs.slides.add_slide(layout)
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
            print(f'slide {number}/{len(SLIDES)}: {fn.__name__}' + (f'  ({len(found)} layout finding(s))' if found else ''))
        output.parent.mkdir(parents=True, exist_ok=True)
        prs.save(output)
    import hashlib
    record = {'deck_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'source': 'deckkit estimate (PIL font metrics)', 'slides': problems}
    output.with_suffix('.layout.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    for number, found in problems.items():
        for issue in found:
            print(f'  slide {number}: {issue}', file=sys.stderr)
    print(f'saved {output}: {len(SLIDES)} slides; {sum(map(len, problems.values()))} builder layout finding(s)')


if __name__ == '__main__':
    main()
