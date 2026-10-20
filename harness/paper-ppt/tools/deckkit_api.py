"""Print the exact deckkit API (signatures + first docstring line). Read this instead of guessing."""
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import deckkit


def line(obj):
    doc = inspect.getdoc(obj) or ''
    return doc.splitlines()[0] if doc else ''


def main():
    print('Coordinates: 1600x900 deck px (1 px = 0.6 pt). Font sizes: points, minimum', deckkit.MIN_PT)
    print('Colour roles (set via configure_theme):', ', '.join(deckkit.C))
    print('Icons: none built in. Draw this deck'"'"'s artwork as SVG: cv.svg(markup, x, y, w) for one-off art,')
    print('       or configure_theme(icons={key: markup}) + cv.icon_c(key, cx, cy, size) for artwork reused across slides.')
    print('\nModule functions')
    for name in ('new_presentation', 'configure_theme', 'notes', 'measure', 'wrap_lines', 'lighten', 'fpx'):
        fn = getattr(deckkit, name)
        print(f'  {name}{inspect.signature(fn)}  # {line(fn)}')
    print('\nCanvas methods (cv = Canvas(slide.shapes, IconStore(prs, tmp)))')
    for name, fn in inspect.getmembers(deckkit.Canvas, inspect.isfunction):
        if not name.startswith('_'):
            print(f'  cv.{name}{inspect.signature(fn)}  # {line(fn)}'.replace('(self, ', '(').replace('(self)', '()'))


if __name__ == '__main__':
    main()
