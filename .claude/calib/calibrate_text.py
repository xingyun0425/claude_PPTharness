"""Measure how PowerPoint wraps and sizes deckkit paragraphs, versus deckkit's prediction.

Builds a grid of para() boxes (CJK, mixed CJK/Latin, varying width, size and line height),
renders it with ppt_render.ps1, and compares predicted vs actual line counts and heights.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path.home() / '.claude/skills/paper-ppt/tools'
sys.path.insert(0, str(SKILL))
import deckkit as dk
from deckkit import Canvas, IconStore, new_presentation, wrap_lines, fpx

OUT = Path(__file__).parent
SAMPLES = [
    '奖励是可验证的二值信号；KL、EWC 约束都挡不住"科学失忆"：反复 DPO 保住行为，却丢了诊断知识',
    '多轮自博弈对话漂移到与话题无关的吸引子状态，模型崩塌随递归训练加剧',
    '信息几何统一理论：真实数据混合/熵奖励/检索都是"熵储备"，外部信号占比趋于零时退化随之而来',
    'Shumailov（Nature）：递归训练导致退化；Zenil：外部信号占比趋于零，退化随之而来',
    '不需要奖励模型错位，优化动力学本身就足以自我退化',
    '杠杆在脚手架：更强的搜索架构可替代更大的模型（LEVI），FunSearch 与 AlphaEvolve 共同方向',
]
WIDTHS = [260, 340, 420, 560, 760]
SIZES = [(16, 1.25), (18, 1.3), (20, 1.25), (18, 1.4)]


def build(path):
    prs, layout = new_presentation(None)
    cases = []
    with tempfile.TemporaryDirectory() as tmp:
        icons = IconStore(prs, tmp)
        for si, (pt, lh) in enumerate(SIZES):
            sld = prs.slides.add_slide(layout)
            cv = Canvas(sld.shapes, icons)
            x, y, col_h = 20, 20, 0
            for wi, w in enumerate(WIDTHS):
                for ti, s in enumerate(SAMPLES):
                    pred = wrap_lines(s, pt, False, w)
                    h = len(pred) * fpx(pt) * lh * 1.2
                    if y + h > 880:
                        x, y = x + w + 20 if False else x, 20
                    cid = f'c{si}_{wi}_{ti}'
                    if x + w > 1590:
                        sld = prs.slides.add_slide(layout)
                        cv = Canvas(sld.shapes, icons)
                        x, y = 20, 20
                    bottom = cv.para(s, x, y, w, pt=pt, lh=lh, name=cid)
                    cases.append(dict(id=cid, pt=pt, lh=lh, w=w, text=s, pred=pred, pred_h=bottom - y))
                    y = bottom + 16
                    if y > 760:
                        x, y = x + w + 24, 20
        prs.save(path)
    return cases


def main():
    deck = OUT / 'calib.pptx'
    cases = build(deck)
    audit = OUT / 'extents.json'
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(SKILL / 'ppt_render.ps1'),
                    '-Pptx', str(deck), '-OutDir', str(OUT / 'png'), '-AuditJson', str(audit)], check=True)
    data = json.loads(audit.read_text(encoding='utf-8-sig'))
    scale = 1600 / data['slide_w']
    actual = {}
    for sl in data['slides']:
        shapes = sl['shapes'] if isinstance(sl['shapes'], list) else [sl['shapes']]
        for sh in shapes:
            lines = sh['lines'] if isinstance(sh['lines'], list) else [sh['lines']]
            actual[sh['name']] = dict(lines=[l for l in lines if l is not None], bound_h=sh['bound'][3] * scale,
                                      frame_h=sh['frame'][3] * scale)
    rows = []
    for c in cases:
        a = actual.get(c['id'])
        if not a:
            continue
        rows.append(dict(c, act=a['lines'], act_h=a['bound_h']))
    (OUT / 'results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(rows)} cases measured')


if __name__ == '__main__':
    main()
