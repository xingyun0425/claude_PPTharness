"""Preserve historical entry files and replace them with explicit migration stubs."""
from pathlib import Path
import shutil

root = Path("C:/Users/16947/.claude/ppt-harness")
backup = root / "legacy-entry-backup"
backup.mkdir(exist_ok=True)
for name in ("harness.py", "generate_paper_ppt.py"):
    target = root / name
    saved = backup / name
    if not saved.exists():
        shutil.copy2(target, saved)
    target.write_text('"""Retired placeholder entry. See the active paper-ppt workflow."""\n\nif __name__ == "__main__":\n    raise SystemExit("This placeholder entry is retired. Read C:/Users/16947/.claude/skills/paper-ppt/WORKFLOW.md and use its tools/run_pipeline.py build/deliver commands.")\n', encoding="utf-8")
    print("Retired:", target)
