"""Native PPTX authoring scaffold. Copy to the project as tools/build_deck.py and add
one real, sourced @slide function per entry in slide_plan.json.

Usage: python tools/build_deck.py output.pptx

API: run `python <skill>/tools/deckkit_api.py` for the exact Canvas signatures. Do not
guess helpers (there is no Deck class, chart_line(), arc_arrow() or register()).
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deckkit import Canvas, IconStore, configure_theme, new_presentation, notes

SLIDES = []
# Fill from design_brief.md, i.e. from this reference, never from an earlier project:
# {'colors': {'navy': '...', 'blue': '...', ...}, 'font': '...', 'icons': {...}}
THEME = None
# Path to the reference .pptx when the new deck must carry its masters (logo, header
# band, footer); None builds on a blank 16:9 deck. Keep content clear of the decoration
# zones recorded in reference_audit.json -> layouts.
BASE = None
BASE_LAYOUT = None


def slide(fn):
    SLIDES.append(fn)
    return fn


# Each @slide function receives (cv, number) and returns speaker notes that cite
# the paper's pages/figures. Words, tables, charts and diagram labels stay native
# and editable; SVG (cv.svg / cv.icon_c) is only for artwork.


def main():
    if len(sys.argv) != 2 or not SLIDES:
        raise SystemExit('Add real @slide functions, then run: python tools/build_deck.py output.pptx')
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
            for ph in list(sld.placeholders):          # empty placeholders show "Click to add" boxes
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
    # The draft is always saved so it can be rendered and inspected; unresolved findings
    # are copied into review.json by render_review.py and block delivery until fixed or waived.
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
