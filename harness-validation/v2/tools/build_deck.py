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
THEME = {'colors': {'navy': '0B6E6E', 'blue': '13897F', 'rose': 'C0392B', 'pale': 'E6F2F1', 'line': 'BFD9D6', 'zone': 'F2F8F7'}, 'font': 'Microsoft YaHei'}
# Path to the reference .pptx when the new deck must carry its masters (logo, header
# band, footer); None builds on a blank 16:9 deck. Keep content clear of the decoration
# zones recorded in reference_audit.json -> layouts.
BASE = r'C:/Users/16947/Downloads/page_study/合稿-20260707电力人工智能自主科研引擎方案汇报.pptx'
BASE_LAYOUT = None


def slide(fn):
    SLIDES.append(fn)
    return fn


# Each @slide function receives (cv, number) and returns speaker notes that cite
# the paper's pages/figures. Words, tables, charts and diagram labels stay native
# and editable; SVG (cv.svg / cv.icon_c) is only for artwork.

LOOP = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">'
        '<circle cx="200" cy="200" r="150" fill="none" stroke="#13897F" stroke-width="10" stroke-dasharray="26 14"/>'
        '<path d="M330,120 l26,-6 l-6,28" fill="none" stroke="#13897F" stroke-width="10" stroke-linejoin="round"/></svg>')


@slide
def components(cv, number):
    cv.text('技术验证：参考母版 + 原生组件 + 自绘 SVG', 130, 62, pt=26, bold=True, color='0B6E6E')
    cv.para('合成内容，仅验证工具链：母版装饰来自参考 PPT，文字与形状可编辑，循环图为本页自绘 SVG。', 110, 150, 1380, pt=18)
    cv.svg(LOOP, 160, 230, 400, name='反馈循环插图')
    for i, (s, ang) in enumerate([('生成假设', (360, 245)), ('执行实验', (560, 430)), ('分析结果', (360, 615)), ('沉淀知识', (160, 430))]):
        cv.pill(s, *ang, pt=18, fill='0B6E6E')
    g = cv.group('说明卡片')
    g.card(700, 250, 790, 420)
    g.text('标签为原生文本，叠放在 SVG 之上', 740, 300, pt=22, bold=True, color='0B6E6E')
    g.bullets(['SVG 只承担线条和形状', '改字不需要重新生成图片', '颜色来自本次参考的主题'], 740, 350, 700, pt=18)
    return 'Source: synthetic integration fixture; no research claims.'


@slide
def evidence(cv, number):
    cv.text('技术验证：原生表格与折线图', 130, 62, pt=26, bold=True, color='0B6E6E')
    cv.table(110, 160, [220, 170], ['项目', '数值'], [['A', '10'], ['B', '15'], ['C', '12']], row_h=70, head_h=70, pt=18, head_pt=18)
    cv.line_chart(600, 150, 900, 520, ['A', 'B', 'C'], [('合成', [10, 15, 12], '13897F', False)], 20, major=5, pt=16)
    return 'Source: synthetic values A=10, B=15, C=12.'


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
