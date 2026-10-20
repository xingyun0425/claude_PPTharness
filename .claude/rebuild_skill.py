"""Rebuild the paper-ppt skill as it was when RSI_Survey_Deck_23slides.pptx was built.

The good deck was built 2026-10-19 09:53Z-12:46Z. All skill edits before 09:53Z are kept;
everything after (13:51Z onward) is dropped. Sources, in order of preference:
  1. exact file copies taken from the skill during the good session (power_paper_ppt/tools)
  2. Write tool inputs / Edit replays from the session transcripts
  3. the line-numbered dump of the Codex version printed at 09:00Z (buyfpw4qj.txt)
"""
import glob
import json
import os
import re
import shutil

CUTOFF = '2026-10-19T09:53:00'
PROJ = r'C:\Users\16947\.claude\projects\C--Users-16947-Downloads-claude-trail-2'
SKILL = r'C:\Users\16947\.claude\skills\paper-ppt'
GOOD_COPY = r'C:\Users\16947\Downloads\claude_trail_2\power_paper_ppt\tools'
DUMP = os.path.join(PROJ, '6993ddff-4152-4363-b8a5-d3f3afd03416', 'tool-results', 'buyfpw4qj.txt')
OUT = r'C:\Users\16947\Downloads\claude_trail_2\.claude\skill_rebuilt'


def codex_dump():
    """Split the 'cat -n' dump into {relative path: text}."""
    files, cur, lines = {}, None, []
    for raw in open(DUMP, encoding='utf-8').read().split('\n'):
        m = re.match(r'^=== (.+)$', raw)
        if m:
            if cur:
                files[cur] = '\n'.join(lines) + '\n'
            cur, lines = m.group(1).strip(), []
            continue
        m = re.match(r'^\s*\d+\t(.*)$', raw)
        if cur and m:
            lines.append(m.group(1))
        elif cur and re.match(r'^\s*\d+$', raw):
            lines.append('')
    if cur:
        files[cur] = '\n'.join(lines) + '\n'
    return files


def skill_ops():
    """All Write/Edit calls on skill files before the cutoff, deduplicated, time-ordered."""
    ops, seen = [], set()
    for path in glob.glob(os.path.join(PROJ, '*.jsonl')):
        for line in open(path, encoding='utf-8', errors='ignore'):
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = d.get('timestamp', '')
            if d.get('type') != 'assistant' or not ts or ts >= CUTOFF:
                continue
            for c in d.get('message', {}).get('content', []):
                if not (isinstance(c, dict) and c.get('type') == 'tool_use'):
                    continue
                if c.get('name') not in ('Write', 'Edit') or c.get('id') in seen:
                    continue
                inp = c.get('input') or {}
                fp = str(inp.get('file_path') or '').replace('/', '\\')
                if '\\skills\\paper-ppt\\' not in fp:
                    continue
                seen.add(c['id'])
                rel = fp.split('\\skills\\paper-ppt\\', 1)[1].replace('\\', '/')
                ops.append((ts, rel, c['name'], inp))
    return sorted(ops, key=lambda o: o[0])


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, 'tools'))
    base = codex_dump()
    state = {rel: text for rel, text in base.items()}
    log = []
    for ts, rel, name, inp in skill_ops():
        if name == 'Write':
            state[rel] = inp['content']
            log.append(f'{ts} Write {rel}')
        else:
            text = state.get(rel)
            old, new = inp.get('old_string', ''), inp.get('new_string', '')
            if text is None or old not in text:
                log.append(f'{ts} Edit {rel} SKIPPED (base missing or old_string not found)')
                continue
            state[rel] = text.replace(old, new, 1)
            log.append(f'{ts} Edit {rel}')
    # Files only edited via shell scripts before the cutoff: take exact copies from the good run
    for rel in ('tools/deckkit.py', 'tools/render_review.py', 'tools/build_deck_template.py'):
        state[rel] = open(os.path.join(GOOD_COPY, os.path.basename(rel)), encoding='utf-8').read()
        log.append(f'copy  {rel} from power_paper_ppt/tools (taken during the good run)')
    # Files untouched since before the cutoff (mtime earlier than 09:53Z): keep current versions
    for rel in ('tools/deckkit_api.py', 'tools/integration_fixture.py', 'tools/ppt_render.ps1',
                'tools/regression_checks.py'):
        state[rel] = open(os.path.join(SKILL, rel), encoding='utf-8').read()
        log.append(f'keep  {rel} (unchanged since before the good run)')
    for rel, text in sorted(state.items()):
        dest = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    print('\n'.join(log))
    print('\nrebuilt:', ', '.join(sorted(state)))


if __name__ == '__main__':
    main()
