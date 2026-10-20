"""Extract inspectable design evidence from a reference PPTX.

This is evidence for a human/agent design decision, not an automatic template.
Includes component vocabulary: cards, arrows, icons, grids.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt
from zipfile import ZipFile
from lxml import etree


def shapes_with_bounds(shapes, transform=(1, 1, 0, 0)):
    """Map group child coordinates to slide coordinates; rotations need visual QA."""
    sx, sy, dx, dy = transform
    for shape in shapes:
        if shape.left is None or shape.width is None:   # inherited placeholder geometry
            continue
        bounds = (shape.left * sx + dx, shape.top * sy + dy,
                  shape.width * sx, shape.height * sy)
        yield shape, bounds
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            xfrm = shape._element.find(qn('p:grpSpPr')).find(qn('a:xfrm'))
            off, ext = xfrm.find(qn('a:chOff')), xfrm.find(qn('a:chExt'))
            child_sx = shape.width / max(1, int(ext.get('cx')))
            child_sy = shape.height / max(1, int(ext.get('cy')))
            yield from shapes_with_bounds(shape.shapes, (
                sx * child_sx, sy * child_sy,
                dx + sx * (shape.left - int(off.get('x')) * child_sx),
                dy + sy * (shape.top - int(off.get('y')) * child_sy)))


def analyze_components(prs):
    """Extract component library: cards (rounded rects), arrows, icons, grids."""
    cards = []  # rounded rectangles that look like content containers
    arrows = []
    icons = []  # small graphics (< 100px) with simple shapes

    for slide_num, slide in enumerate(prs.slides, 1):
        for shape, bounds in shapes_with_bounds(slide.shapes):
            w_px = int(bounds[2] / prs.slide_width * 1600)
            h_px = int(bounds[3] / prs.slide_height * 900)

            # Detect cards: AUTO_SHAPE rectangles with rounded corners, medium-large size
            if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                try:
                    auto_type = shape.auto_shape_type
                except (ValueError, AttributeError):
                    # Skip shapes with unsupported auto_shape_type (like 'line')
                    continue
                try:
                    # ROUNDED_RECTANGLE or RECTANGLE with adjusted corner
                    if auto_type == MSO_SHAPE.ROUNDED_RECTANGLE or auto_type == MSO_SHAPE.RECTANGLE:
                        if 150 < w_px < 800 and 80 < h_px < 600:  # card-sized
                            card_info = {
                                'slide': slide_num,
                                'width_px': w_px,
                                'height_px': h_px,
                                'shape_name': shape.name
                            }
                            # Get stroke and fill
                            try:
                                if shape.line.width:
                                    card_info['stroke_pt'] = round(shape.line.width.pt, 1)
                                if shape.line.color and shape.line.color.rgb:
                                    card_info['stroke_color'] = str(shape.line.color.rgb)
                            except (AttributeError, TypeError):
                                pass
                            try:
                                if shape.fill.type and shape.fill.fore_color.rgb:
                                    card_info['fill_color'] = str(shape.fill.fore_color.rgb)
                            except (AttributeError, TypeError):
                                pass
                            # Try to get corner radius (not directly exposed by python-pptx)
                            try:
                                sp_pr = shape._element.find(qn('p:spPr'))
                                if sp_pr is not None:
                                    prst_geom = sp_pr.find(qn('a:prstGeom'))
                                    if prst_geom is not None and prst_geom.get('prst') in ('roundRect', 'round2SameRect'):
                                        av_lst = prst_geom.find(qn('a:avLst'))
                                        if av_lst is not None:
                                            gd = av_lst.find(qn('a:gd'))
                                            if gd is not None:
                                                card_info['corner_radius_pct'] = gd.get('fmla', '').replace('val ', '')
                            except (AttributeError, TypeError):
                                pass
                            cards.append(card_info)

                    # Detect arrows: specific arrow auto shapes
                    if 'ARROW' in str(auto_type):
                        arrow_info = {
                            'slide': slide_num,
                            'type': str(auto_type),
                            'width_px': w_px,
                            'height_px': h_px
                        }
                        try:
                            if shape.line.width:
                                arrow_info['stroke_pt'] = round(shape.line.width.pt, 1)
                            if shape.line.color and shape.line.color.rgb:
                                arrow_info['color'] = str(shape.line.color.rgb)
                        except (AttributeError, TypeError):
                            pass
                        arrows.append(arrow_info)
                except (AttributeError, TypeError):
                    pass

            # Detect icons: small pictures or small auto shapes with fill
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                if w_px < 120 and h_px < 120:  # icon-sized
                    icons.append({
                        'slide': slide_num,
                        'type': 'picture',
                        'size_px': max(w_px, h_px),
                        'name': shape.name
                    })
            elif shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                if w_px < 100 and h_px < 100:  # small graphic
                    try:
                        if shape.fill.type:
                            icons.append({
                                'slide': slide_num,
                                'type': 'auto_shape',
                                'shape': str(shape.auto_shape_type),
                                'size_px': max(w_px, h_px),
                                'name': shape.name
                            })
                    except (AttributeError, TypeError):
                        pass

    # Summarize
    summary = {
        'cards': {
            'count': len(cards),
            'avg_width_px': int(sum(c['width_px'] for c in cards) / len(cards)) if cards else 0,
            'avg_height_px': int(sum(c['height_px'] for c in cards) / len(cards)) if cards else 0,
            'common_strokes': Counter(c.get('stroke_pt', 0) for c in cards).most_common(3),
            'common_stroke_colors': Counter(c.get('stroke_color', 'none') for c in cards).most_common(3),
            'examples': cards[:5]  # first 5 for inspection
        },
        'arrows': {
            'count': len(arrows),
            'types': Counter(a['type'] for a in arrows).most_common(5),
            'common_strokes': Counter(a.get('stroke_pt', 0) for a in arrows).most_common(3),
            'examples': arrows[:5]
        },
        'icons': {
            'count': len(icons),
            'avg_size_px': int(sum(i['size_px'] for i in icons) / len(icons)) if icons else 0,
            'types': Counter(i['type'] for i in icons).most_common(3),
            'examples': icons[:5]
        }
    }
    return summary


def inspect(path):
    prs = Presentation(path)
    colors, fonts, sizes = Counter(), Counter(), Counter()
    slides = []
    for number, slide in enumerate(prs.slides, 1):
        kinds = Counter()
        boxes = []
        total = 0
        for shape, bounds in shapes_with_bounds(slide.shapes):
            total += 1
            kinds[str(shape.shape_type)] += 1
            box = [round(bounds[0] / prs.slide_width, 3),
                   round(bounds[1] / prs.slide_height, 3),
                   round(bounds[2] / prs.slide_width, 3),
                   round(bounds[3] / prs.slide_height, 3)]
            frames = [shape.text_frame] if shape.has_text_frame else []
            if shape.has_table:
                frames += [cell.text_frame for row in shape.table.rows for cell in row.cells]
            if shape.has_chart:
                boxes.append({'box': box, 'name': shape.name, 'chart': str(shape.chart.chart_type)})
            for frame in frames:
                if not frame.text.strip():
                    continue
                boxes.append({'box': box, 'name': shape.name, 'text': frame.text[:200]})
                for paragraph in frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.name:
                            fonts[run.font.name] += 1
                        if run.font.size:
                            sizes[round(run.font.size.pt)] += 1
                        try:
                            if run.font.color and run.font.color.rgb:
                                colors[str(run.font.color.rgb)] += 1
                        except (AttributeError, TypeError, ValueError):
                            pass
            try:
                if shape.fill.type and shape.fill.fore_color.rgb:
                    colors[str(shape.fill.fore_color.rgb)] += 1
            except (AttributeError, TypeError, ValueError):
                pass
        slides.append({'slide': number, 'shape_types': dict(kinds),
                       'text_boxes': boxes, 'shape_count': total})
    layouts = []
    for layout in prs.slide_layouts:
        deco = []
        for owner in (layout.slide_master, layout):
            for shape, b in shapes_with_bounds(owner.shapes):
                if shape.is_placeholder:
                    continue
                deco.append({'from': 'master' if owner is layout.slide_master else 'layout', 'name': shape.name,
                             'box_1600': [round(b[0] / prs.slide_width * 1600), round(b[1] / prs.slide_height * 900),
                                          round(b[2] / prs.slide_width * 1600), round(b[3] / prs.slide_height * 900)]})
        used = sum(1 for s in prs.slides if s.slide_layout == layout)
        layouts.append({'name': layout.name, 'placeholders': len(layout.placeholders),
                        'used_by_slides': used, 'decorations': deco})
    theme_evidence = {}
    with ZipFile(path) as archive:
        for name in archive.namelist():
            if name.startswith('ppt/theme/theme') and name.endswith('.xml'):
                root = etree.fromstring(archive.read(name))
                theme_evidence[name] = {
                    'colors': root.xpath('//*[local-name()="clrScheme"]//*[local-name()="srgbClr"]/@val'),
                    'fonts': root.xpath('//*[local-name()="fontScheme"]//*[@typeface]/@typeface'),
                }
    components = analyze_components(prs)
    return {'reference': str(Path(path).resolve()), 'slide_count': len(prs.slides),
            'aspect_ratio': round(prs.slide_width / prs.slide_height, 4),
            'common_colors': colors.most_common(12),
            'common_fonts': fonts.most_common(8),
            'common_font_sizes_pt': sizes.most_common(12), 'slides': slides,
            'themes': theme_evidence, 'layouts': layouts,
            'component_vocabulary': components,
            'limitations': 'Counts are explicit declarations, not a visual ranking; inherited styles and rotated objects require rendered inspection.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('reference', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    result = inspect(a.reference)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'inspected {result["slide_count"]} slides: {a.output}')


if __name__ == '__main__':
    main()
