"""参考（电力自主科研方案汇报）的页面组件：虚线导语框、红色关键词、青绿标签头、面板、结论行。

标记语法：{{红色加粗}}  [[深青加粗]]
"""
import re

from lxml import etree
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn

import deckkit as dk
from deckkit import C, E, fpx, frame, measure, set_runs, wrap_lines

SLIDES = []


def slide(kind='body'):
    def deco(fn):
        SLIDES.append((kind, fn))
        return fn
    return deco


def col(c):
    """颜色角色名或十六进制。"""
    return C.get(c, c) if c else c


_MARK = re.compile(r'(\{\{.*?\}\}|\[\[.*?\]\])')


def parse(s, color='text', bold=False):
    out = []
    for part in _MARK.split(s):
        if not part:
            continue
        if part.startswith('{{'):
            out.append((part[2:-2], True, C['rose']))
        elif part.startswith('[['):
            out.append((part[2:-2], True, C['navy']))
        else:
            out.append((part, bold, col(color)))
    return out


def plain(s):
    return _MARK.sub(lambda m: m.group(0)[2:-2], s)


def rtext(cv, s, x, y, w, pt=18, color='text', bold=False, align='l', lh=1.25,
          indent=False, anchor='t', h=None, name=None):
    """可换行的多色文本框，(x, y) 为左上角；支持 \\n 分段。返回估算底边 y。"""
    paras = s.split('\n')
    n = 0
    widest = 0
    for p in paras:
        txt = ('　　' if indent else '') + plain(p)
        marked = bold or bool(_MARK.search(p))
        lines = wrap_lines(txt, pt, bold, w * (0.97 if marked and not bold else 1))
        n += len(lines)
        widest = max(widest, max(measure(l, pt, bold) for l in lines))
    est = n * fpx(pt) * lh * 1.2
    hh = h if h else est
    tb = cv.shapes.add_textbox(E(x), E(y), E(w), E(hh))
    frame(tb.text_frame, anchor={'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE}[anchor], wrap=True)
    for i, p in enumerate(paras):
        par = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
        par.alignment = dk.ALIGN[align]
        par.line_spacing = lh
        if indent:
            set_runs(par, '　　', pt, False, col(color))
        for seg, b, c in parse(p, color, bold):
            set_runs(par, seg, pt, b, c)
    if name:
        tb.name = name
    top = y if anchor == 't' else y + (hh - est) / 2
    left = {'l': x, 'c': x + (w - min(widest, w)) / 2, 'r': x + w - min(widest, w)}[align]
    cv._reg(left, top, left + min(widest, w), top + est, plain(s)[:14] + '…')
    if est > hh + 4:
        cv.overflow.append(f'[文本高于框] {plain(s)[:20]}')
    return top + est


def header(cv, title, sub=None):
    """编号标题，位于 logo 右侧；副标题以“ – ”接在后面。"""
    cv.text(title, 122, 66, pt=28, bold=True, color=C['navy'], name='标题')
    if sub:
        x = 122 + measure(title, 28, True) + 14
        cv.text('– ' + sub, x, 70, pt=20, bold=True, color=C['navy'], name='副标题')


def tabs(cv, labels, active):
    """右上定位标签组（ref-37）。"""
    w, h = 118, 50
    x = 1580 - w * len(labels)
    for i, lab in enumerate(labels):
        on = i == active
        cv.label_box(lab, x + i * w, 40, w, h, pt=16, bold=True,
                     color=C['white'] if on else C['text'], fill=C['blue'] if on else C['white'],
                     line=C['gold'], lw=1.5, name=f'定位 {lab}')


def intro(cv, s, y=142, lines=None):
    """青绿虚线导语框，首行缩进两字，20 pt。返回框底 y。"""
    pt = 20
    # 按 rtext 自己的 wrap_lines 计算真实行数（est_lines 是速算，容易一行之差）
    n = lines or len(wrap_lines('　　' + plain(s), pt, False, 1512 * (0.97 if _MARK.search(s) else 1)))
    h = n * fpx(pt) * 1.3 * 1.2 + 26
    cv.box(20, y, 1560, h, line='008A88', lw=1.5, dash=True, name='导语框')
    rtext(cv, s, 44, y + 13, 1512, pt=pt, lh=1.3, indent=True, name='导语')
    return y + h


def est_lines(s, pt, w, indent=0):
    """按各段真实字重累加宽度估算行数（导语框这类长段落比逐词断行估算更准）。"""
    total = indent * fpx(pt) + sum(measure(seg, pt, b) for seg, b, _ in parse(s))
    # 对照 PowerPoint 渲染校准：比值 ≤2.16 实际为 2 行，2.35 起为 3 行
    return max(1, -(-int(total) // int(w * 1.05)))


def bullets(cv, items, x, y, w, pt=18, gap=10, lh=1.25, color='text', dot='blue'):
    """青绿方点条目；返回底边 y。"""
    for s in items:
        cv.box(x, y + fpx(pt) * 0.45, 9, 9, fill=col(dot), name='项目符号')
        y = rtext(cv, s, x + 20, y, w - 20, pt=pt, lh=lh, color=color) + gap
    return y


def tag(cv, s, x, y, w, h=50, pt=20, fill='blue'):
    """青绿实心标签头（ref-07 计划概况）。"""
    sp = cv.label_box(s, x, y, w, h, pt=pt, bold=True, color=C['white'], fill=col(fill), r=6,
                      name=f'标签 {s}')
    return sp


def panel(cv, x, y, w, h, head=None, fill='zone', line='blue', head_color='navy', pt=20):
    """浅青圆角面板（ref-04），标题居中加粗。"""
    cv.cards.append((x, y, x + w, y + h, f'面板 {head or ""}'))
    cv.box(x, y, w, h, fill=col(fill), line=col(line), lw=1.5, r=10, name=f'面板 {head or ""}')
    if head:
        cv.text(head, x + w / 2, y + 34, pt=pt, bold=True, color=col(head_color), align='c')


def chip(cv, s, x, y, w, h, pt=18, fill='pale', line='blue', color='text', bold=False):
    """浅青小框（ref-04 “资源认知建模难”），可两行。"""
    cv.box(x, y, w, h, fill=col(fill), line=col(line), lw=1.2, r=8, name=f'条目 {plain(s)[:8]}')
    rtext(cv, s, x + 6, y, w - 12, pt=pt, color=color, bold=bold, align='c', anchor='m', h=h, lh=1.15)


def float_tag(cv, s, cx, cy, pt=18, fill='blue'):
    """面板边上的浮动标签（ref-16 “解决思路”）。"""
    w = measure(s, pt, True) + 48
    cv.label_box(s, cx - w / 2, cy - 22, w, 44, pt=pt, bold=True, color=C['white'], fill=col(fill),
                 r=6, name=f'浮动标签 {s}')


def conclusion(cv, s, y=822):
    """底部结论行（ref-16）：红色加粗句。"""
    rtext(cv, s, 40, y - 22, 1520, pt=22, color='rose', bold=True, align='c', name='结论')


def alpha_fill(sp, alpha):
    """给纯色填充加透明度（0–100）。"""
    clr = sp._element.spPr.find(qn('a:solidFill'))[0]
    etree.SubElement(clr, qn('a:alpha'), val=str(int(alpha * 1000)))


def arrow_right(cv, x, y, w=30, h=26, fill='blue'):
    """参考 ref-21 的小实心右箭头。"""
    a = cv.box(x, y - h / 2, w, h, fill=col(fill), shape=dk.MSO_SHAPE.RIGHT_ARROW, name='箭头')
    return a


def left_column(gf, *cols):
    """表格中长文本列左对齐（ref-37 “预期目标”列）。"""
    for row in list(gf.table.rows)[1:]:
        for j in cols:
            for p in row.cells[j].text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT
