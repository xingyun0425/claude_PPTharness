# Paper PPT: reference-led native PowerPoint workflow

The paper supplies facts; the reference supplies visual grammar; the agent designs each page. HarnessDev (harnessdev-deck-native.pptx) is the quality bar for craft and editability, not a palette, icon set or layout to repeat. A different reference must produce a visibly different deck.

## What made HarnessDev good (transfer these practices, not its palette or icons)

- Every slide makes one claim (conclusion-style title) and shows the evidence for it: a figure, table, chart, or a diagram drawn for that relationship. No slide is just headed boxes with two lines in each.
- **Diagrams and icons were drawn for each deck's content.** A loop drawn as a loop, 64 switches as 64 squares, a diagnostic chain as a chain. The bundled robot/lock/gear icons fit papers about agents and harnesses; a different domain needs its own icons in the reference's visual style. Drawing page-specific illustrations is a required practice; the specific style follows the reference.
- Illustrations shared the deck's type, colors and line weights, so they read as part of the page, not pasted on. Text labels stay native and sit on top of or beside the SVG artwork.
- Pages were filled to the reference's density with real content; the grid, margins and conclusion band were consistent across the deck.
- One representative page was calibrated first and approved; then the deck was built; then every page was rendered in PowerPoint, looked at, and fixed, over several rounds.

## Why the RSI deck failed (do not repeat)

- The reference was used only for two colors. Its header/logo master, numbered section titles, red keyword emphasis, teal tab headers and 3-column density were ignored.
- **Slides were large pale cards with a few 16 pt lines; illustrations were minimal.** HarnessDev averaged 4.6 SVG elements per content page (74 across 16 pages); RSI had 0.5 (8 across 16 pages). Pages with zero illustrations, zero charts, zero tables and zero pictures are usually underworked.
- Rendering was skipped or not acted on: the cover title was clipped, titles ran off the slide, text overlapped. The PowerPoint audit now finds 23 such defects in that deck and 0 in HarnessDev.
- After an API error the agent switched to PptxGenJS instead of fixing the call. Never switch generators.

## Sequence

1. **Paper.** Read it fully. Record claims, numbers, figure/table ids with page numbers. Never invent values; if extraction fails, stop and say what is missing.
2. **Reference study.** Write `slide_plan.json` with `paper` and `reference` (a .pptx, .pdf, image, or folder of images), then run
   `run_pipeline.py reference --plan slide_plan.json --review-dir review`.
   It renders every reference page to `review/reference/`, writes contact sheets, ink density, and for a .pptx `reference_audit.json` (fonts, sizes, colors, `component_vocabulary` with card/arrow/icon statistics, and `layouts[].decorations`: logo/header/footer boxes in 1600×900 coordinates). Look at the contact sheets and then the individual pages. For a .pptx reference, read `component_vocabulary` to understand what components are available. Statistics support, never replace, looking.
3. **design_brief.md** (required for delivery). Record concretely, citing reference page ids:
   - Title position/size/color and any numbering scheme.
   - Header/footer/logo: reuse the master or not, and why.
   - Content grid and margins; body size and density (lines per page, columns).
   - Emphasis device: color keywords, bold, tags.
   - **Component vocabulary** (extracted from reference pages):
     - **Cards:** corner radius, stroke weight/color, shadow style, padding, typical dimensions
     - **Arrows:** stroke weight, head style (triangle/circle/none), color, types seen (straight/curved/branching)
     - **Icons:** stroke weight, fill vs outline, background shape (circle/square/none), typical sizes (inline/header/accent)
     - **Column grids:** widths and gutters for 2-col, 3-col, 4-col layouts observed
     - **Text emphasis:** bold, color highlighting, pill tags, underlines
   - **Layout patterns** observed in reference (as vocabulary, not templates to copy):
     - Three-column cards, left-right split, process flow, single large visual, data table, vertical stack
     - For each pattern: which reference page demonstrates it, when it works (parallel concepts, comparison, sequence, etc.)
   - **Icons and illustrations style:** linear (stroked outlines), flat/solid, or full-color; line weight; whether icons sit on circular/rounded backgrounds; how the reference's palette is used in artwork (accent color for active elements, neutral for structure, etc.); treatment of photos and screenshots if any.
   - Diagram, picture and chart treatment.
   - Palette roles mapped to deckkit roles (navy, blue, rose, pale, zone, line, text).
   Separate the user's explicit requirements from incidental features of the reference.
3.5. **Design each page's composition.** Before writing slide_plan.json:
   - For each slide, analyze the content relationship: parallel concepts? comparison? sequence? hierarchy? data trend?
   - Choose components from the reference vocabulary (cards, arrows, icons, grids, text blocks) that clarify this relationship.
   - Sketch the composition in `slide_plan.json`'s `composition` field:
     - List components: type (card/arrow/icon/text/chart), position (left/right/center/top, rough x/y or grid cell), size
     - Describe connections: arrows between cards, icons above text, labels beside diagrams
     - State why this composition fits the content (not "because reference page 7 used it")
   - You may combine components in ways the reference never showed, as long as each component follows the reference's style (card radius, arrow weight, icon stroke, etc.).
   The reference provides **component vocabulary** and **layout patterns as examples**; the paper's content determines which components each page uses and how they connect.
4. **Page plan.** Plan by cognitive units, not by paper sections. **If the user specifies a target page count, distribute content to meet it exactly.** Otherwise, let content complexity and narrative flow determine the count:
   - **Method chapters:** split into "problem definition" → "core idea" → "technical implementation" → "algorithm flow"; each concept on its own page.
   - **Experiment chapters:** split into "experiment design" → "main results" → "ablation studies" → "case analysis".
   - **One idea per page:** a definition, a comparison, a process, a data set. Avoid cramming "method + results + discussion" onto one slide.
   - **Control density:** 80–120 words of body text, 2–3 bullet points, choose one of formula/chart; exceeding this signals the page covers two ideas and needs splitting.
   For every slide in `slide_plan.json`: `purpose` (the claim this page makes), **`focus`** (optional: why this is a standalone page — what cognitive problem it solves, what context it needs from prior pages, what it sets up for later), `source` (paper pages/figures), `reference_slide` (the reference page whose composition fits this content's relationship and capacity), `adaptation` (what is kept, what changes), **`visual`** (what illustration/chart/table/diagram this page needs; which parts are SVG and which are native shapes/text; if none, state why: "entire page is a table" or "text-only definitions list"). Decide the relationship first: sequence, loop, hierarchy, comparison, matrix, trend, case. Record each page's cognitive focus to ensure it stands alone as a clear step in the argument.
5. **Icon library (icons.py).** Before building content pages, write `tools/icons.py` as a dictionary of this deck's domain-specific icons and reusable illustration elements, following the icon style recorded in design_brief.md. Keys are kebab-case slugs; values are SVG markup strings (viewBox and xmlns required). Include the paper's domain objects (for a power-grid paper: substation, transformer, data-flow; for a biology paper: cell, protein, pathway; for an agent paper: the bundled robot/lock/gear are already provided). Build an `icons_preview.pptx` that shows each icon with its key, render it, compare against reference pages, and refine until the style matches. Import this file in build_deck.py and merge its icons into THEME['icons']. All illustrations must relate to this paper's content; do not draw generic placeholders.

6. **Builder.** Copy `tools/build_deck_template.py` to the project as `tools/build_deck.py` with `deckkit.py` beside it. Run `deckkit_api.py` for the exact API; never guess helpers. Set `THEME` from the brief. If the new deck belongs to the reference's organization or template, set `BASE` to the reference .pptx so its master (logo, header rule, background, page number) is inherited, and keep content out of `layouts[].decorations`. One function per slide. Text, tables, charts and diagram labels are native; draw page-specific artwork with `cv.svg(markup, ...)` or place icons from icons.py with `cv.icon_c(key, cx, cy, size)`. **SVG usage rules:**
   - **Small icons:** semantic markers (a lock for security, a chart for metrics), sized proportional to body text (30–60 deck px for 18 pt body).
   - **Scene illustrations:** cover page or method overview; larger composed artwork (200–400 deck px).
   - **Structure diagrams (loops, flows, hierarchies):** nodes and connecting lines should be native shapes where practical (easier to edit); only use SVG when the shape itself requires custom paths (a curved arrow with specific control points, an irregular boundary).
   Text labels are always native, never baked into SVG. Place them with `cv.text()` or `cv.pill()` on top of or beside the artwork.
7. **Calibrate.** Build 2–3 representative pages first (a concept diagram, an evidence page, the cover if any). Run build, then `render_review.py compare <reference page> <our page> out.png` and look at both side by side. Revise until hierarchy, density, icon style and finish match the reference. Proceed without waiting for approval unless the user asked for a checkpoint.
8. **Whole deck.** `run_pipeline.py build --builder tools/build_deck.py --output deck.pptx --plan slide_plan.json --review-dir review`. The draft is always saved. Build output reports deckkit's estimated layout findings; render adds PowerPoint's measured findings (clipped, overlapping, off-slide text) and an ink-density comparison with the reference.
9. **Review loop.** Look at `review/slide-contact-*.png` for rhythm and consistency, then every `slide-NN.png` at full size. Fix in the builder and rebuild; repeat until clean. **Common text layout issues to check:**
   - **Clipped text:** bullet points or multi-line text cut off at the bottom of the text box
   - **Overflow:** text extends beyond the box border (right or bottom edge)
   - **Uneven spacing:** same-level items have inconsistent vertical gaps or overlap each other
   - **Misaligned elements:** icons, bullets, or labels drift from their intended positions
   
   Then edit `review/review.json` per slide: `reviewed: true`, a specific `assessment` of what you saw (including whether illustrations clarify the content and harmonize with text layout), `issues: []`. Each entry in `auto_issues` must be fixed (it disappears on rebuild) or waived in `waivers` with the concrete reason it is invisible or intended. Pages with no illustration, chart, table or picture warrant a note explaining why (e.g., "definitions list, text-only by design"). Any rebuild resets the review.
10. **Deliver.** `run_pipeline.py deliver --output deck.pptx --plan slide_plan.json --review-dir review` checks hashes, design_brief.md, plan, 16 pt floor, no full-slide pictures, and the review. Hand over the PPTX, plan, brief, builder and icons.py; state approximated values and what was not verified.

## Rules

- 16 pt minimum everywhere, including chart axes and table cells; titles about 32 pt unless the current reference or user says otherwise. If it does not fit, rewrite or split.
- No HTML-to-PPT, whole-slide images, or placeholder content. SVG fallbacks are rasterized by headless Chrome/Edge; slides never pass through HTML.
- Do not read precise numbers off a picture unless the user accepts approximation; keep source caveats.
- Tool error → fix the tool or call site and rerun this path. Report what you changed.
- Editing the PPTX by hand and rebuilding conflict: rebuilding overwrites manual edits.

## Plan shape

```json
{
  "paper": "C:/path/paper.pdf",
  "reference": "C:/path/reference.pptx",
  "slides": [
    {
      "purpose": "The method is a three-stage loop with a verifier gate",
      "source": "paper.pdf p. 4, Fig. 2",
      "reference_slide": "ref-07: left diagram + right key-points column",
      "adaptation": "Keep its tab-header columns and red keyword emphasis; replace its photo with a drawn loop; four nodes instead of three",
      "visual": "Loop diagram: four pill nodes (SVG fills) connected by dashed arc arrows (native curved connectors); gate icon (SVG, 40px) between output and feedback; step labels as native text pills on each node"
    }
  ]
}
```
