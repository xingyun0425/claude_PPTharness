"""RSI 综述汇报（论文 arXiv:2607.07663；视觉参考：电力人工智能自主科研引擎方案汇报）。

Usage: python tools/build_deck.py output.pptx

母版沿用参考 .pptx：正文页「1_标题幻灯片」、封面/结束页「空白」、目录页「标题幻灯片」。
每页一个 @slide 函数，分章写在 ch1.py … ch4.py；页面组件在 helpers.py。
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deckkit import Canvas, IconStore, configure_theme, new_presentation, notes
import helpers
import ch1, ch2, ch3, ch4  # noqa: F401  (registration order = slide order)

# design_brief.md「调色板 → deckkit 角色」
THEME = {'colors': {
    'navy': '064E41', 'blue': '008380', 'gold': '0E6767', 'rose': 'C00000', 'darkRose': '9E1B1B',
    'pale': 'D5ECEB', 'zone': 'ECF6F6', 'paleRose': 'FBE9E9', 'line': '98D1CC', 'text': '1F2D2D',
    'grey': '57678F', 'neutral': '8A9A9A', 'chipGrey': 'E6E6E6', 'sky': '0070C0', 'white': 'FFFFFF',
    'paleGold': 'F2F6F6', 'goldLine': 'B9DAD7', 'goldText': '0E6767'}}
BASE = 'C:/Users/16947/Downloads/合稿-20260707电力人工智能自主科研引擎方案汇报.pptx'
LAYOUTS = {'body': '1_标题幻灯片', 'cover': '空白', 'toc': '标题幻灯片'}


def main():
    if len(sys.argv) != 2:
        raise SystemExit('python tools/build_deck.py output.pptx')
    configure_theme(THEME['colors'], THEME.get('font'), THEME.get('icons'))
    output = Path(sys.argv[1])
    prs, _ = new_presentation(BASE, LAYOUTS['body'])
    by_name = {l.name: l for l in prs.slide_layouts}
    only = {int(x) for x in sys.argv[2:]} if False else None
    problems = {}
    with tempfile.TemporaryDirectory() as tmp:
        icons = IconStore(prs, tmp)
        for number, (kind, fn) in enumerate(helpers.SLIDES, 1):
            sld = prs.slides.add_slide(by_name[LAYOUTS[kind]])
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
            print(f'slide {number}/{len(helpers.SLIDES)}: {fn.__name__}' + (f'  ({len(found)} layout finding(s))' if found else ''))
        output.parent.mkdir(parents=True, exist_ok=True)
        prs.save(output)
    record = {'deck_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'source': 'deckkit estimate (PIL font metrics)', 'slides': problems}
    output.with_suffix('.layout.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    for number, found in problems.items():
        for issue in found:
            print(f'  slide {number}: {issue}', file=sys.stderr)
    print(f'saved {output}: {len(helpers.SLIDES)} slides; {sum(map(len, problems.values()))} builder layout finding(s)')


if __name__ == '__main__':
    main()
