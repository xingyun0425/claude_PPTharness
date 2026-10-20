"""Reference study -> build/render/audit -> verified delivery for a paper deck.

    run_pipeline.py reference --plan slide_plan.json --review-dir review
    run_pipeline.py build     --builder tools/build_deck.py --output deck.pptx --plan slide_plan.json --review-dir review
    run_pipeline.py deliver   --output deck.pptx --plan slide_plan.json --review-dir review

plan.reference may be a .pptx, a .pdf, a single image, or a folder of reference images.
"""
import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

from inspect_reference import inspect
from render_review import IMAGE_EXT, check_review, contact_sheets, density, fingerprint, render, sha256
from validate_deck import validate

BRIEF_MIN_CHARS = 400


def check_errors(errors):
    if errors:
        raise SystemExit('\n'.join('FAIL: ' + item for item in errors))


def load_plan(plan):
    data = json.loads(plan.read_text(encoding='utf-8'))
    ref = Path(data.get('reference') or '')
    if not str(ref) or str(ref) == '.':
        raise SystemExit('FAIL: plan.reference is required')
    ref = (ref if ref.is_absolute() else plan.parent / ref).resolve()
    if not ref.exists():
        raise SystemExit(f'FAIL: reference not found: {ref}')
    return data, ref


def study_reference(ref, out):
    """Render the reference so it can be looked at; record structure where it is a .pptx."""
    out.mkdir(parents=True, exist_ok=True)
    index = {'reference': str(ref), 'reference_sha256': fingerprint(ref)}
    if ref.suffix.lower() == '.pptx':
        audit = inspect(ref)
        (out / 'reference_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
        render(ref, out, prefix='ref', audit=False, record=False)
        images = sorted(out.glob('ref-[0-9]*.png'))
    elif ref.suffix.lower() == '.pdf':
        import fitz
        for old in out.glob('ref-[0-9]*.png'):
            old.unlink()
        with fitz.open(ref) as doc:
            for i, page in enumerate(doc, 1):
                page.get_pixmap(dpi=110).save(out / f'ref-{i:02d}.png')
        images = sorted(out.glob('ref-[0-9]*.png'))
        contact_sheets(images, out / 'ref-contact')
    else:
        files = [ref] if ref.is_file() else [p for p in ref.rglob('*') if p.suffix.lower() in IMAGE_EXT
                                              and 'contact' not in p.stem and '_sheets' not in p.parts]
        images = sorted(files, key=lambda p: (len(p.stem), p.stem))
        if not images:
            raise SystemExit(f'FAIL: no reference images in {ref}')
        contact_sheets(images, out / 'ref-contact')
    index['images'] = [{'image': str(p), 'density': density(p)} for p in images]
    index['density_median'] = statistics.median(x['density'] for x in index['images'])
    index['contact_sheets'] = [str(p) for p in sorted(out.glob('ref-contact-*.png'))]
    (out / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Reference study: {len(images)} page(s) -> {out}')
    print('Look at the contact sheets, then the individual pages you will adapt, before writing design_brief.md.')
    return index


def brief_errors(plan):
    brief = plan.parent / 'design_brief.md'
    if not brief.exists():
        return [f'design_brief.md missing beside the plan ({brief})']
    if len(brief.read_text(encoding='utf-8').strip()) < BRIEF_MIN_CHARS:
        return ['design_brief.md is too thin to record the reference analysis']
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['reference', 'build', 'deliver'])
    parser.add_argument('--builder', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--review-dir', type=Path, required=True)
    args = parser.parse_args()
    plan, review = args.plan.resolve(), args.review_dir.resolve()
    data, reference = load_plan(plan)
    ref_dir = review / 'reference'

    if args.command == 'reference':
        study_reference(reference, ref_dir)
        return
    if args.output is None:
        parser.error(f'{args.command} requires --output')
    output = args.output.resolve()
    index_file = ref_dir / 'index.json'

    if args.command == 'build':
        if args.builder is None:
            parser.error('build requires --builder')
        builder = args.builder.resolve()
        if output == reference:
            raise SystemExit('Output must differ from the read-only reference')
        if not index_file.exists() or json.loads(index_file.read_text(encoding='utf-8')).get('reference_sha256') != fingerprint(reference):
            raise SystemExit('FAIL: study the current reference first: run_pipeline.py reference --plan ... --review-dir ...')
        for warning in brief_errors(plan):
            print('WARN:', warning, '(required for deliver)')
        subprocess.run([sys.executable, str(builder), str(output)], cwd=builder.parent, check=True)
        check_errors(validate(output, plan))
        render(output, review)
        ref_median = json.loads(index_file.read_text(encoding='utf-8'))['density_median']
        rows = json.loads((review / 'review.json').read_text(encoding='utf-8'))['slides']
        sparse = [r['slide'] for r in rows if r['density'] < 0.5 * ref_median]
        print(f'Ink density: reference median {ref_median:.2f}; deck median {statistics.median(r["density"] for r in rows):.2f}'
              + (f'; much emptier than the reference: slides {sparse}' if sparse else ''))
        state = {'deck_sha256': sha256(output), 'plan_sha256': sha256(plan),
                 'reference': str(reference), 'reference_sha256': fingerprint(reference),
                 'builder': str(builder), 'builder_sha256': sha256(builder)}
        (review / 'build.json').write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        print('BUILD COMPLETE = draft. Look at the contact sheet, then every slide PNG next to its reference page; '
              'fix the builder and rebuild until the review is clean, then record it in review.json.')
    else:
        build_file = review / 'build.json'
        if not build_file.exists():
            raise SystemExit('FAIL: no build record; run build first')
        state = json.loads(build_file.read_text(encoding='utf-8'))
        checks = {'deck_sha256': sha256(output), 'plan_sha256': sha256(plan),
                  'reference_sha256': fingerprint(reference),
                  'builder_sha256': sha256(state['builder'])}
        check_errors([f'{key} changed since build; rebuild and review' for key, value in checks.items() if state.get(key) != value])
        check_errors(brief_errors(plan) + validate(output, plan) + check_review(output, review / 'review.json'))
        receipt = {'deck': str(output), 'deck_sha256': sha256(output),
                   'plan_sha256': sha256(plan), 'review_sha256': sha256(review / 'review.json'),
                   'status': 'passed', 'limitations': 'Recorded visual judgment is not an automatic design-quality score.'}
        (review / 'delivery.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        print('PASS: structural checks and current visual review; delivery receipt written.')


if __name__ == '__main__':
    main()
