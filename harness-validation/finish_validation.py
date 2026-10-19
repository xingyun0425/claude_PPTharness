"""Record the two PNGs actually inspected in this task and test final delivery."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
runner = Path("C:/Users/16947/.claude/skills/paper-ppt/tools/run_pipeline.py")
manifest_path = root / "review/review.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
assessments = [
    "Viewed PowerPoint PNG: plum title and teal custom SVG render correctly; native grouped text is legible and remains inside the card; arrow and SVG label are separated without collision. Synthetic integration fixture, not a design benchmark.",
    "Viewed PowerPoint PNG: native table values A=10, B=15, C=12 match the plotted points; axis labels are legible; table and chart have separate space; title and subtitle do not overlap. Synthetic integration fixture, not research evidence."
]
for row, assessment in zip(manifest["slides"], assessments):
    row.update(reviewed=True, assessment=assessment, issues=[])
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
command = [sys.executable, str(runner), "deliver", "--output", str(root / "native-components.pptx"), "--plan", str(root / "slide_plan.json"), "--review-dir", str(root / "review")]
subprocess.run(command, check=True)
plan = root / "slide_plan.json"
original = plan.read_bytes()
try:
    plan.write_bytes(original + b" ")
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode != 0 and "plan_sha256 changed" in (result.stdout + result.stderr)
    print("PASS: changed plan invalidates delivery")
finally:
    plan.write_bytes(original)
subprocess.run(command, check=True)
