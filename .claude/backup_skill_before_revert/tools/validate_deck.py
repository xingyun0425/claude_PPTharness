"""Fail closed when a generated deck lacks its reference and slide design record."""
import argparse
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from zipfile import ZipFile
from lxml import etree


def walk_shapes(shapes):
    for shape in shapes:
        yield shape
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk_shapes(shape.shapes)


def count_visuals(slide):
    """Return (svg_count, chart_count, table_count, picture_count) for one slide."""
    svg = sum(1 for s in walk_shapes(slide.shapes) if s.shape_type == MSO_SHAPE_TYPE.PICTURE
              and hasattr(s, 'image') and s.image.content_type == 'image/svg+xml')
    chart = sum(1 for s in walk_shapes(slide.shapes) if s.has_chart)
    table = sum(1 for s in walk_shapes(slide.shapes) if s.has_table)
    pic = sum(1 for s in walk_shapes(slide.shapes) if s.shape_type == MSO_SHAPE_TYPE.PICTURE
              and hasattr(s, 'image') and s.image.content_type != 'image/svg+xml')
    return svg, chart, table, pic


def validate(deck_path, plan_path):
    plan = json.loads(Path(plan_path).read_text(encoding='utf-8'))
    if not isinstance(plan, dict):
        return ['plan must be a JSON object']
    prs = Presentation(deck_path)
    errors = []
    if not plan.get('paper'):
        errors.append('plan.paper is required')
    if not plan.get('reference'):
        errors.append('plan.reference is required')
    slides = plan.get('slides', [])
    if not isinstance(slides, list):
        return ['plan.slides must be a list']
    def is_hidden(s):
        return s.shapes and s.shapes[0].has_text_frame and not s.shapes[0].text.strip()
    hidden = sum(1 for s in prs.slides if is_hidden(s))
    expected = [s for s in slides if not s.get('component_library')]
    if len(expected) != len(prs.slides) - hidden:
        errors.append(f'deck has {len(prs.slides)} slides ({hidden} hidden); plan records {len(expected)} content slides')
    for number, slide in enumerate(prs.slides, 1):
        is_lib = number > len(expected)
        if not is_lib and (not slide.has_notes_slide or not slide.notes_slide.notes_text_frame.text.strip()):
            errors.append(f'slide {number}: speaker notes missing')
        entry = slides[number - 1] if number <= len(slides) else {}
        if not isinstance(entry, dict):
            errors.append(f'slide {number}: plan entry must be an object')
            entry = {}
        if not is_lib:
            for key in ('purpose', 'source', 'reference_slide', 'adaptation', 'visual'):
                if not entry.get(key):
                    errors.append(f'slide {number}: missing plan.{key}')
        shapes = list(walk_shapes(slide.shapes))
        if not any(s.has_text_frame and s.text.strip() for s in shapes):
            errors.append(f'slide {number}: no editable text')
        for shape in shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                coverage = shape.width * shape.height / (prs.slide_width * prs.slide_height)
                if coverage > 0.8:
                    errors.append(f'slide {number}: full-slide picture ({coverage:.0%})')
            if shape.has_text_frame:
                text_len = len(shape.text.strip())
                # Warn on high character density (likely to cause overflow or cramped layout)
                if text_len > 200 and shape.width and shape.height:
                    area_ratio = text_len / (shape.width * shape.height / 10000)  # chars per 100x100 px
                    if area_ratio > 8:  # Empirical threshold for CJK text
                        print(f'NOTE: slide {number}: text box with {text_len} chars may be overcrowded ({area_ratio:.1f} chars/100px²)', file=sys.stderr)
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size and run.font.size.pt < 16:
                            errors.append(f'slide {number}: text below 16 pt')
    # Read explicit font declarations independently of Canvas, including table
    # cells, grouped objects, and chart labels. Inherited sizes still need render QA.
    with ZipFile(deck_path) as archive:
        for name in archive.namelist():
            if name.startswith(('ppt/slides/slide', 'ppt/charts/chart')) and name.endswith('.xml'):
                root = etree.fromstring(archive.read(name))
                small = [int(value) / 100 for value in root.xpath('//@sz') if str(value).isdigit() and int(value) < 1600]
                if small:
                    errors.append(f'{name}: explicit font below 16 pt (min {min(small):g})')
    vis_notes = []
    for i, slide in enumerate(prs.slides, 1):
        svg, chart, table, pic = count_visuals(slide)
        if svg == chart == table == pic == 0:
            vis_notes.append(i)
    if vis_notes:
        print(f'NOTE: {len(vis_notes)}/{len(prs.slides)} slides lack visuals; confirm design in plan.visual or review.assessment', file=sys.stderr)
    # Check for adjacent slides with similar purpose (possible redundancy or need to merge/resplit)
    import re
    from collections import Counter
    for i in range(len(expected) - 1):
        p1 = expected[i].get('purpose', '')
        p2 = expected[i + 1].get('purpose', '')
        if not p1 or not p2:
            continue
        words1 = Counter(re.findall(r'\w+', p1.lower()))
        words2 = Counter(re.findall(r'\w+', p2.lower()))
        common = sum((words1 & words2).values())
        total = sum(words1.values()) + sum(words2.values())
        if total > 0 and common / total > 0.35:
            print(f'NOTE: slides {i+1}/{i+2} have similar purpose wording; confirm they cover distinct ideas', file=sys.stderr)
    return list(dict.fromkeys(errors))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('deck', type=Path)
    parser.add_argument('plan', type=Path)
    a = parser.parse_args()
    errors = validate(a.deck, a.plan)
    for error in errors:
        print('FAIL:', error)
    if errors:
        raise SystemExit(1)
    print(f'PASS: {len(Presentation(a.deck).slides)} slides have a design record and editable content')


if __name__ == '__main__':
    main()
