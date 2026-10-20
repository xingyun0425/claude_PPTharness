"""Deck-specific helpers over deckkit: reference chrome (header, dashed lead box, red
conclusion line, category tabs, contents page) and rich text with **red keywords**."""
from pptx.enum.text import MSO_ANCHOR

import deckkit as dk
from deckkit import C, E, frame, measure, set_runs, wrap_lines, fpx, ALIGN

SLIDES = []          # (layout key, function)
LAYOUTS = {'body': '1_标题幻灯片', 'blank': '空白', 'toc': '标题幻灯片'}
CHAPTERS = ['研究背景与问题', '分类框架与语料', '四类自我改进机制', '极限、安全与展望']
CATS = ['部署时', '训练时', '自评估', '自主科研']


def slide(layout='body'):
    def deco(fn):
        SLIDES.append((layout, fn))
        return fn
    return deco


def _segs(s, color, bold):
    out = []
    for i, p in enumerate(s.split('**')):
        if p:
            out.append((p, {'bold': True, 'color': C['rose']} if i % 2 else {'bold': bold, 'color': color}))
    return out


def rich_lines(ps, pt, bold):
    """Line count / widest line for a paragraph with **bold** parts, measuring each token in its own weight."""
    toks = []
    for i, part in enumerate(ps.split('**')):
        for t in dk._TOKEN.findall(part):
            toks.append((t, bold or bool(i % 2)))
    return toks


def wrap_rich(ps, pt, bold, width):
    lines, cur, started = [], 0.0, False
    widest = 0.0
    for t, b in rich_lines(ps, pt, bold):
        tw = measure(t, pt, b)
        if cur + tw > width * 1.0 and started and t not in dk._NO_BREAK_BEFORE:
            widest = max(widest, cur)
            lines.append(cur)
            cur, started = (0.0 if t.isspace() else tw), not t.isspace()
        else:
            cur += tw
            started = started or not t.isspace()
    if started:
        lines.append(cur)
        widest = max(widest, cur)
    return max(1, len(lines)), widest


def rp(cv, s, x, y, w, pt=18, color=None, bold=False, lh=1.25, align='l', indent=False, name=None):
    """Wrapped rich paragraph(s); '**x**' = red bold keyword, '\n' = new paragraph. Returns bottom y."""
    color = C['text'] if color is None else color
    paras = s.split('\n')
    tb_h, widest, all_segs = 0, 0, []
    for k, ps in enumerate(paras):
        ps = ('　　' if indent else '') + ps
        n_l, wid = wrap_rich(ps, pt, bold, w)
        widest = max(widest, wid)
        tb_h += n_l * fpx(pt) * lh * 1.2
        all_segs.append(_segs(ps, color, bold))
    cv._reg(x if align == 'l' else x + (w - widest) / 2, y, (x + widest) if align == 'l' else x + (w + widest) / 2,
            y + tb_h, (name or s.replace('**', ''))[:18] + '…')
    tb = cv.shapes.add_textbox(E(x), E(y), E(w), E(tb_h))
    frame(tb.text_frame, anchor=MSO_ANCHOR.TOP, wrap=True)
    for k, segs in enumerate(all_segs):
        p = tb.text_frame.paragraphs[0] if k == 0 else tb.text_frame.add_paragraph()
        p.alignment = ALIGN[align]
        p.line_spacing = lh
        for t, o in segs:
            set_runs(p, t, pt, o['bold'], o['color'])
    if name:
        tb.name = name
    return y + tb_h


def text_h(s, w, pt=18, bold=False, lh=1.25):
    n = sum(wrap_rich(p, pt, bold, w)[0] for p in s.split('\n'))
    return n * fpx(pt) * lh * 1.2


def boxtext(cv, s, x, y, w, h, pt=18, color=None, bold=False, fill=None, line=None, r=10, lw=1.5,
            align='c', pad=14, lh=1.2, card=True, dash=False, name=None):
    """Box with vertically centred wrapped text inside."""
    cv.box(x, y, w, h, fill=fill, line=line, r=r, lw=lw, dash=dash, name=name or '文本框')
    if card:
        cv.cards.append((x, y, x + w, y + h, name or s[:8]))
    th = text_h(s, w - 2 * pad, pt, bold, lh)
    if th > h + 2:
        cv.overflow.append(f'[文本高于框] {s[:16]}')
    return rp(cv, s, x + pad, y + (h - th) / 2, w - 2 * pad, pt, color, bold, lh, align)


def head(cv, title, sub=None):
    cv.text(title, 118, 64, pt=28, bold=True, color=C['navy'], name='标题')
    if sub:
        cv.text('– ' + sub, 118 + measure(title, 28, True) + 14, 67, pt=20, bold=True, color=C['navy'], name='副标题')


def lead(cv, s, y=142, pt=20):
    """Reference lead box: dashed teal hairline, first-line indent, red keywords. Returns bottom y."""
    th = text_h('　　' + s, 1560 - 36, pt, False, 1.25)
    h = th + 24
    cv.box(20, y, 1560, h, line='008A88', lw=1.5, dash=True, name='导语框')
    rp(cv, s, 38, y + 12, 1560 - 36, pt=pt, indent=True, name='导语')
    return y + h


def concl(cv, s, y=826, pt=20):
    """Red conclusion line, centred; **x** parts bold."""
    segs = []
    for i, p in enumerate(s.split('**')):
        if p:
            segs.append((p, {'bold': bool(i % 2), 'color': C['rose']}))
    cv.rich(segs, 800, y, pt=pt, align='c', name='结论句')


def tabs(cv, active):
    """ref-37 category tab group at the top right; the current category is solid."""
    w, h, x0, y = 136, 46, 1580 - 4 * 136, 42
    for i, s in enumerate(CATS):
        on = s == active
        cv.label_box(s, x0 + i * w, y, w, h, pt=18, bold=True, color=C['white'] if on else C['text'],
                     fill=C['blue'] if on else C['white'], line=C['grey'] if not on else C['blue'], lw=1.5, name=f'类别 {s}')


def rpanel(cv, x, y, w, h, title, icon=None, pt=22, color=None):
    """ref-16 panel: white, thin teal outline, teal bold heading (with an icon to its left)."""
    color = C['blue'] if color is None else color
    cv.card(x, y, w, h, fill=C['white'], line=color, r=12, shadow=True, name=f'面板 {title}')
    tw = measure(title, pt, True)
    isz = 44 if icon else 0
    left = x + (w - tw - isz - (12 if icon else 0)) / 2
    if icon:
        cv.icon_c(icon, left + isz / 2, y + 38, isz, name=f'图标 {title}')
    cv.text(title, left + isz + (12 if icon else 0), y + 38, pt=pt, bold=True, color=color, name=f'面板标题 {title}')


def tag(cv, s, cx, cy, pt=18, fill=None, w=None):
    w = w or measure(s, pt, True) + 44
    cv.label_box(s, cx - w / 2, cy - 22, w, 44, pt=pt, bold=True, color=C['white'], fill=fill or C['blue'], r=6, name=f'标签 {s}')


def chip(cv, s, x, y, w, h, pt=18, **kw):
    """ref-16 small pale box with teal hairline."""
    return boxtext(cv, s, x, y, w, h, pt=pt, fill=C['pale'], line=C['blue'], r=12, **kw)


def toc(cv, active):
    cv.box(114, 152, 227, 518, fill='EBEBEB', name='目录底块')
    cv.box(83, 475, 69, 273, fill=C['blue'], name='目录竖条')
    cv.text('目    录', 335, 340, pt=40, bold=True, color=C['blue'], align='c', name='目录')
    cv.text('CONTENTS', 335, 414, pt=28, bold=True, color=C['blue'], align='c', name='CONTENTS')
    for i, (n, s) in enumerate(zip('一二三四', CHAPTERS)):
        y = 210 + i * 127
        on = i == active
        fill, col = (C['blue'], C['white']) if on else (C['chipGrey'], '595959')
        cv.label_box(n, 516, y, 100, 100, pt=28, bold=True, color=col, fill=fill, name=f'章号 {n}')
        cv.label_box(s, 664, y, 802, 100, pt=28, bold=True, color=col, fill=fill, name=f'章名 {s}')


def bigtext(cv, s, cx, cy, pt, color, bold=True):
    """Large single line (cover/end), bypassing nothing: still goes through set_runs."""
    cv.text(s, cx, cy, pt=pt, bold=bold, color=color, align='c')
