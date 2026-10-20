"""SVG artwork drawn for this deck, in the reference's style: thin round-capped teal
outline icons (ref-21 flask/brain/layers) with a pale-teal fill accent. Lines and shapes
only; every word is native text placed by build_deck.py."""

T, D, P, R, B = '008380', '064E41', 'D5ECEB', 'C00000', '0070C0'   # teal, deep, pale, red, blue


def _icon(body, stroke=T, sw=1.8):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><g fill="none" stroke="#{stroke}" '
            f'stroke-width="{sw * 2}" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>')


def _pf(d):  # pale filled shape, drawn under strokes
    return f'<path d="{d}" fill="#{P}" stroke="none"/>'


ICONS = {
    # 1.2 observations
    'fork': _icon(_pf('M8 6h14v10H8z') + '<rect x="8" y="6" width="14" height="10" rx="2"/><path d="M15 16v8M15 24l-9 10M15 24l9 10M15 24v10"/>'
                  '<circle cx="6" cy="38" r="3"/><circle cx="15" cy="38" r="3"/><circle cx="24" cy="38" r="3"/><path d="M30 12h12M30 20h8"/>'),
    'growth': _icon(_pf('M30 14h8v28h-8z') + '<path d="M6 42h36"/><rect x="8" y="32" width="6" height="10"/><rect x="19" y="24" width="6" height="18"/>'
                    '<rect x="30" y="14" width="8" height="28"/><path d="M8 22l10-8 8 4 14-12M34 6h6v6"/>'),
    'gauge': _icon(_pf('M8 32a16 16 0 0 1 32 0z') + '<path d="M8 32a16 16 0 0 1 32 0"/><path d="M24 32l8-10"/><circle cx="24" cy="32" r="3"/>'
                   '<path d="M6 40h36M12 22l2 2M24 16v3M36 22l-2 2"/>'),
    # column icons
    'gearchat': _icon(_pf('M6 8h26v18H16l-6 6v-6H6z') + '<path d="M6 8h26v18H16l-6 6v-6H6z"/><circle cx="34" cy="34" r="6"/>'
                      '<path d="M34 24v4M34 40v4M24 34h4M40 34h4M27 27l3 3M38 38l3 3M41 27l-3 3M30 38l-3 3M12 15h14M12 20h9"/>'),
    'weights': _icon(_pf('M6 6h36v36H6z') + '<rect x="6" y="6" width="36" height="36" rx="3"/><circle cx="15" cy="15" r="3"/><circle cx="33" cy="15" r="3"/>'
                     '<circle cx="15" cy="33" r="3"/><circle cx="33" cy="33" r="3"/><circle cx="24" cy="24" r="3"/>'
                     '<path d="M17 17l5 5M31 17l-5 5M17 31l5-5M31 31l-5-5"/>'),
    'flask': _icon(_pf('M12 36l7-12h10l7 12z') + '<path d="M19 6h10M21 6v12L9 40a2 2 0 0 0 2 3h26a2 2 0 0 0 2-3L27 18V6"/>'
                   '<path d="M13 32h22"/><circle cx="22" cy="36" r="1.5"/><circle cx="28" cy="33" r="1"/>'),
    'docs': _icon(_pf('M14 12h22v30H14z') + '<path d="M10 6h20l6 6v30H10z" transform="translate(4 0)"/><path d="M8 10v34h24"/>'
                  '<path d="M20 20h12M20 26h12M20 32h8"/>'),
    # hypotheses
    'steps': _icon(_pf('M6 42h12V30h12V18h12v24z') + '<path d="M6 42h12V30h12V18h12v24H6"/><path d="M10 22l4 4 8-8"/>'),
    'coins': _icon(_pf('M10 30h20v8H10z') + '<ellipse cx="20" cy="38" rx="10" ry="4"/><path d="M10 38v-8M30 38v-8"/><ellipse cx="20" cy="30" rx="10" ry="4"/>'
                   '<path d="M10 30v-8M30 30v-8"/><ellipse cx="20" cy="22" rx="10" ry="4"/><path d="M36 10v26M32 14l4-4 4 4"/>'),
    'herd': _icon(_pf('M18 42v-8a6 6 0 0 1 12 0v8z') + '<circle cx="24" cy="18" r="5"/><path d="M16 42v-8a8 8 0 0 1 16 0v8"/>'
                  '<circle cx="10" cy="22" r="4"/><path d="M4 40v-6a6 6 0 0 1 9-5"/><circle cx="38" cy="22" r="4"/><path d="M44 40v-6a6 6 0 0 0-9-5"/>'
                  '<path d="M20 6h8M26 4l2 2-2 2"/>'),
    'institution': _icon(_pf('M8 18h32v4H8z') + '<path d="M6 18L24 6l18 12z"/><path d="M8 22h32M10 22v16M18 22v16M30 22v16M38 22v16M6 42h36"/>'),
    'trend': _icon('<path d="M4 44h40M4 44V4"/><path d="M8 40c10-2 14-6 18-14s8-16 16-20"/><circle cx="42" cy="6" r="2.5"/>'),
    # deployment
    'pen': _icon(_pf('M30 8l10 10-20 20H10V28z') + '<path d="M30 8l10 10-20 20H10V28z"/><path d="M26 12l10 10M8 44h32"/>'),
    'bolt': _icon(_pf('M26 4L10 26h12l-2 18 18-24H26z') + '<path d="M26 4L10 26h12l-2 18 18-24H26z"/>'),
    'blocks': _icon(_pf('M6 26h16v16H6z') + '<rect x="6" y="26" width="16" height="16" rx="2"/><rect x="26" y="26" width="16" height="16" rx="2"/>'
                    '<rect x="16" y="6" width="16" height="16" rx="2"/><path d="M20 14h8M10 34h8M30 34h8"/>'),
    # training / failure
    'alert': _icon(_pf('M24 6l20 36H4z') + '<path d="M24 6l20 36H4z"/><path d="M24 20v10"/><circle cx="24" cy="36" r="1.2"/>', stroke=R),
    'mirror': _icon(_pf('M10 10h12v28H10z') + '<path d="M24 4v40" stroke-dasharray="3 4"/><rect x="10" y="10" width="12" height="28" rx="2"/>'
                    '<path d="M30 14c8 0 10 8 10 10s-2 10-10 10M34 30l-4 4 4 4"/>', stroke=R),
    'collapse': _icon(_pf('M4 40c8 0 10-26 20-26s12 26 20 26z') + '<path d="M4 40c8 0 10-26 20-26s12 26 20 26"/>'
                      '<path d="M16 40c3 0 5-30 8-30s5 30 8 30" stroke-dasharray="3 3"/><path d="M4 44h40"/>', stroke=R),
    'converge': _icon(_pf('M20 20h8v8h-8z') + '<circle cx="8" cy="8" r="3"/><circle cx="40" cy="8" r="3"/><circle cx="8" cy="40" r="3"/>'
                      '<circle cx="40" cy="40" r="3"/><circle cx="24" cy="4" r="2"/><path d="M11 11l7 7M37 11l-7 7M11 37l7-7M37 37l-7-7"/>'
                      '<rect x="20" y="20" width="8" height="8" rx="2"/>', stroke=R),
    # process vs result
    'notebook': _icon(_pf('M12 6h28v36H12z') + '<rect x="12" y="6" width="28" height="36" rx="2"/><path d="M8 12h8M8 20h8M8 28h8M8 36h8"/>'
                      '<path d="M20 16h14M20 23h14M20 30l3 3 6-6"/>'),
    'receipt': _icon(_pf('M10 4h28v40l-5-4-4 4-5-4-5 4-4-4-5 4z') + '<path d="M10 4h28v40l-5-4-4 4-5-4-5 4-4-4-5 4z"/><path d="M16 14h16M16 21h16M16 28h10"/>'),
    'toolbox': _icon(_pf('M4 18h40v24H4z') + '<rect x="4" y="18" width="40" height="24" rx="3"/><path d="M16 18v-6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6"/>'
                     '<path d="M4 28h40M20 26h8v6h-8z"/>'),
    # auto research
    'dna': _icon(_pf('M14 20h20v8H14z') + '<path d="M14 4c0 12 20 16 20 28s-0 12 0 12M34 4c0 12-20 16-20 28v12"/>'
                 '<path d="M17 12h14M15 20h18M15 28h18M17 36h14"/>'),
    'lens': _icon(_pf('M8 6h18v26H8z') + '<path d="M8 6h18v14M8 6v30h10M12 14h10M12 20h6"/><circle cx="30" cy="30" r="9"/><path d="M37 37l7 7"/>'),
    # limits
    'layers': _icon(_pf('M24 6l18 9-18 9-18-9z') + '<path d="M24 6l18 9-18 9-18-9z"/><path d="M6 24l18 9 18-9M6 33l18 9 18-9"/>'),
    'scurve': _icon('<path d="M4 44h40M4 44V4"/><path d="M8 40c12 0 12-30 32-30" /><path d="M8 6h36" stroke-dasharray="3 4"/>'),
    'chip': _icon(_pf('M10 10h20v20H10z') + '<rect x="10" y="10" width="20" height="20" rx="2"/><path d="M15 4v6M25 4v6M15 30v6M25 30v6M4 15h6M4 25h6M30 15h4"/>'
                  '<circle cx="40" cy="30" r="4"/><path d="M33 44v-2a7 7 0 0 1 14 0v2"/>'),
    'wave': _icon('<path d="M4 24c4-16 6-16 8 0s4 14 6 0 4-10 6 0 3 6 5 0 3-4 5 0 3 2 4 0 2-1 4 0"/><path d="M4 42h40"/>'),
    # safety
    'scope': _icon(_pf('M6 22l26-10 4 10-26 10z') + '<path d="M6 22l26-10 4 10-26 10z"/><path d="M36 22l6-2-3-8-6 2M18 30l-6 14M22 29l6 15"/>'),
    'lock': _icon(_pf('M10 22h28v20H10z') + '<rect x="10" y="22" width="28" height="20" rx="3"/><path d="M16 22v-6a8 8 0 0 1 16 0v6"/><path d="M24 30v5"/>'),
    'ruler': _icon(_pf('M4 16h40v16H4z') + '<rect x="4" y="16" width="40" height="16" rx="2"/><path d="M10 16v6M16 16v9M22 16v6M28 16v9M34 16v6M40 16v9"/>'),
    'pin': _icon(_pf('M24 44S10 28 10 18a14 14 0 0 1 28 0c0 10-14 26-14 26z') +
                 '<path d="M24 44S10 28 10 18a14 14 0 0 1 28 0c0 10-14 26-14 26z"/><circle cx="24" cy="18" r="5"/>', stroke=R),
    # conclusion
    'shield': _icon(_pf('M24 4l16 6v12c0 10-7 18-16 22C15 40 8 32 8 22V10z') +
                    '<path d="M24 4l16 6v12c0 10-7 18-16 22C15 40 8 32 8 22V10z"/><path d="M16 24l6 6 10-12"/>'),
    'frame': _icon(_pf('M14 14h20v20H14z') + '<rect x="14" y="14" width="20" height="20" rx="2"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M20 8l4-4 4 4M20 40l4 4 4-4M8 20l-4 4 4 4M40 20l4 4-4 4"/>'),
}


def stairs(heights, w, dashed_last=True):
    """Rising staircase of len(heights) treads (bottom-aligned); the last one dashed (not yet reached)."""
    n, H = len(heights), max(heights)
    sw = w / n
    parts = []
    for i, th in enumerate(heights):
        x, y = i * sw, H - th
        last = dashed_last and i == n - 1
        fill = 'none' if last else (f'#{P}' if i < n - 2 else '#BFE2DF')
        dash = ' stroke-dasharray="10 8"' if last else ''
        parts.append(f'<rect x="{x + 3:.0f}" y="{y + 3:.0f}" width="{sw - 6:.0f}" height="{th - 6:.0f}" rx="8" '
                     f'fill="{fill}" stroke="#{T}" stroke-width="3"{dash}/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}">{"".join(parts)}</svg>'


def converge_loop(w=300, h=220):
    """Closed loop orbiting a fixed anchor square (bounded refinement)."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" '
            f'markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#{T}"/></marker></defs>'
            f'<path d="M150 22 A130 88 0 0 1 280 110" fill="none" stroke="#{T}" stroke-width="5" marker-end="url(#a)"/>'
            f'<path d="M150 198 A130 88 0 0 1 20 110" fill="none" stroke="#{T}" stroke-width="5" marker-end="url(#a)"/>'
            f'<rect x="78" y="82" width="144" height="56" rx="8" fill="#{T}"/></svg>')


def diverge_spiral(w=300, h=220):
    """Outward spiral with the improvement machinery riding inside the loop (open-ended RSI)."""
    import math
    pts = []
    for k in range(0, 260):
        t = k / 259 * 3.2 * math.pi
        r = 12 + t * 9.5
        pts.append(f'{150 + r * math.cos(t):.1f},{110 + r * 0.7 * math.sin(t):.1f}')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" '
            f'markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#{R}"/></marker></defs>'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="#{R}" stroke-width="4" marker-end="url(#a)"/>'
            f'<circle cx="150" cy="110" r="10" fill="#{R}"/></svg>')


def ring(cx, cy, rx, ry, n, w, h, color=T, gap_deg=22, sw=4):
    """n arc arrows around an ellipse, leaving gaps where the nodes sit (nodes at 90° + k*360/n)."""
    import math
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><marker id="a" viewBox="0 0 10 10" refX="6" refY="5" '
           f'markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#{color}"/></marker></defs>']
    for k in range(n):
        a0 = math.radians(-90 + k * 360 / n + gap_deg)
        a1 = math.radians(-90 + (k + 1) * 360 / n - gap_deg)
        p0 = (cx + rx * math.cos(a0), cy + ry * math.sin(a0))
        p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
        out.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{rx} {ry} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="#{color}" '
                   f'stroke-width="{sw}" stroke-linecap="round" marker-end="url(#a)"/>')
    out.append('</svg>')
    return ''.join(out)


def persistence_axis(w=1400, h=60):
    """Three segments of growing weight on one time axis; the last ends in an arrowhead."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<line x1="10" y1="48" x2="{w - 30}" y2="48" stroke="#{D}" stroke-width="3"/>'
            f'<path d="M{w - 34} 40 L{w - 10} 48 L{w - 34} 56z" fill="#{D}"/>'
            f'<rect x="120" y="14" width="160" height="8" rx="4" fill="#{T}"/>'
            f'<rect x="560" y="12" width="300" height="12" rx="6" fill="#{T}"/>'
            f'<rect x="990" y="9" width="340" height="18" rx="9" fill="#{T}"/>'
            f'<path d="M1330 4 L1370 18 L1330 32z" fill="#{T}"/></svg>')


def pyramid(rows, w, row_h, gap, top_dashed=True):
    """Stacked rungs, narrow at the top and widening downward (centred)."""
    parts = []
    n = len(rows)
    for i, rw in enumerate(rows):
        x, y = (w - rw) / 2, i * (row_h + gap)
        if i == 0 and top_dashed:
            parts.append(f'<rect x="{x + 2}" y="{y + 2}" width="{rw - 4}" height="{row_h - 4}" rx="8" fill="#FFFFFF" '
                         f'stroke="#{D}" stroke-width="3" stroke-dasharray="10 7"/>')
        else:
            shade = ['DDEFEE', 'E6F3F2', 'EEF7F6', 'F5FAFA'][min(i - 1, 3)]
            parts.append(f'<rect x="{x + 2}" y="{y + 2}" width="{rw - 4}" height="{row_h - 4}" rx="8" fill="#{shade}" '
                         f'stroke="#{T}" stroke-width="2.5"/><rect x="{x + 2}" y="{y + 2}" width="12" height="{row_h - 4}" rx="4" fill="#{T}"/>')
    H = n * row_h + (n - 1) * gap
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}">{"".join(parts)}</svg>'


def vline_arrow(h, color=T, up=True, w=30):
    y0, y1 = (h - 4, 14) if up else (4, h - 14)
    head = f'M{w/2 - 10} 18 L{w/2} 2 L{w/2 + 10} 18z' if up else f'M{w/2 - 10} {h - 18} L{w/2} {h - 2} L{w/2 + 10} {h - 18}z'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><line x1="{w/2}" y1="{y0}" x2="{w/2}" y2="{y1}" '
            f'stroke="#{color}" stroke-width="4"/><path d="{head}" fill="#{color}"/></svg>')


def hline_arrow(w, color=T, h=30):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><line x1="2" y1="{h/2}" x2="{w - 14}" y2="{h/2}" '
            f'stroke="#{color}" stroke-width="4"/><path d="M{w - 18} {h/2 - 10} L{w - 2} {h/2} L{w - 18} {h/2 + 10}z" fill="#{color}"/></svg>')


def scenario_path(w=1500, h=70):
    """Three chevron segments, deepening in colour: stall -> compounding efficiency -> full RSI."""
    cols = ['BFE2DF', T, D]
    seg = w / 3
    parts = []
    for i, c in enumerate(cols):
        x = i * seg
        tip = 34
        d = f'M{x} 0 L{x + seg - 6} 0 L{x + seg - 6 + tip} {h/2} L{x + seg - 6} {h} L{x} {h}'
        d += '' if i == 0 else f' L{x + tip} {h/2}'
        parts.append(f'<path d="{d}z" fill="#{c}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 40} {h}">{"".join(parts)}</svg>'


# white variants for icons sitting on solid teal headers
ICONS.update({k + '_w': v.replace(f'stroke="#{T}"', 'stroke="#FFFFFF"').replace(f'fill="#{P}"', 'fill="#FFFFFF" fill-opacity="0.25"')
              for k, v in list(ICONS.items())})


def ring_gaps(cx, cy, rx, ry, gaps, w, h, color=T, sw=4):
    """Arc arrows between len(gaps) nodes at -90° + k*360/n; gaps[k] = half-gap (deg) around node k."""
    import math
    n = len(gaps)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><marker id="a" viewBox="0 0 10 10" refX="6" refY="5" '
           f'markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#{color}"/></marker></defs>']
    for k in range(n):
        a0 = math.radians(-90 + k * 360 / n + gaps[k])
        a1 = math.radians(-90 + (k + 1) * 360 / n - gaps[(k + 1) % n])
        p0 = (cx + rx * math.cos(a0), cy + ry * math.sin(a0))
        p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
        out.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{rx} {ry} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="#{color}" '
                   f'stroke-width="{sw}" stroke-linecap="round" marker-end="url(#a)"/>')
    out.append('</svg>')
    return ''.join(out)


def persistence_axis2(spans, w=1540, h=60):
    """Time axis with bars of growing weight at the given (x0, x1, thickness) spans; last bar ends in an arrowhead."""
    parts = [f'<line x1="4" y1="50" x2="{w - 26}" y2="50" stroke="#{D}" stroke-width="3"/>',
             f'<path d="M{w - 30} 42 L{w - 4} 50 L{w - 30} 58z" fill="#{D}"/>']
    for i, (a, b, t) in enumerate(spans):
        parts.append(f'<rect x="{a}" y="{24 - t / 2}" width="{b - a}" height="{t}" rx="{t / 2}" fill="#{T}"/>')
    a, b, t = spans[-1]
    parts.append(f'<path d="M{b - 4} {24 - t} L{b + 30} 24 L{b - 4} {24 + t}z" fill="#{T}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{"".join(parts)}</svg>'


def vdivider(h, color=T, w=24):
    """Vertical dashed divider with arrowheads at both ends."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><line x1="{w/2}" y1="16" x2="{w/2}" y2="{h - 16}" '
            f'stroke="#{color}" stroke-width="3" stroke-dasharray="8 7"/><path d="M{w/2 - 9} 18 L{w/2} 2 L{w/2 + 9} 18z" fill="#{color}"/>'
            f'<path d="M{w/2 - 9} {h - 18} L{w/2} {h - 2} L{w/2 + 9} {h - 18}z" fill="#{color}"/></svg>')


