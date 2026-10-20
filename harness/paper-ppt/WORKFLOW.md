# Paper PPT: reference-led native PowerPoint workflow

The paper supplies facts; the reference supplies visual grammar; the agent designs each page. HarnessDev (harnessdev-deck-native.pptx) is the quality bar for craft and editability, not a palette, icon set or layout to repeat. A different reference must produce a visibly different deck.

## What made HarnessDev good (transfer this, not its look)

- Every slide makes one claim (conclusion-style title) and shows the evidence for it: a figure, table, chart, or a diagram drawn for that relationship. No slide is just headed boxes with two lines in each.
- Diagrams were designed per page: a loop drawn as a loop, 64 switches as 64 squares, a diagnostic chain as a chain. Generic "card + icon + bullets" was the exception.
- Illustrations shared the deck's type, colors and line weights, so they read as part of the page, not pasted on.
- Pages were filled to the reference's density with real content; the grid, margins and conclusion band were consistent across the deck.
- One representative page was calibrated first and approved; then the deck was built; then every page was rendered in PowerPoint, looked at, and fixed, over several rounds.

## Why the RSI deck failed (do not repeat)

- The reference was used only for two colors. Its header/logo master, numbered section titles, red keyword emphasis, teal tab headers and 3-column density were ignored.
- Slides were large pale cards with a few 16 pt lines; illustrations were placeholders (four straight arrows for a "loop", a big "?").
- Rendering was skipped or not acted on: the cover title was clipped, titles ran off the slide, text overlapped. The PowerPoint audit now finds 23 such defects in that deck and 0 in HarnessDev.
- After an API error the agent switched to PptxGenJS instead of fixing the call. Never switch generators.

## Sequence

1. **Paper.** Read it fully. Record claims, numbers, figure/table ids with page numbers. Never invent values; if extraction fails, stop and say what is missing.
2. **Reference study.** Write `slide_plan.json` with `paper` and `reference` (a .pptx, .pdf, image, or folder of images), then run
   `run_pipeline.py reference --plan slide_plan.json --review-dir review`.
   It renders every reference page to `review/reference/`, writes contact sheets, ink density, and for a .pptx `reference_audit.json` (fonts, sizes, colors, and `layouts[].decorations`: logo/header/footer boxes in 1600×900 coordinates). Look at the contact sheets and then the individual pages. Statistics support, never replace, looking.
3. **design_brief.md** (required for delivery). Record concretely, citing reference page ids: title position/size/color and any numbering scheme; header/footer/logo (reuse the master or not, and why); content grid and margins; body size and density (lines per page, columns); emphasis device (color keywords, bold, tags); diagram, picture and chart treatment; palette roles mapped to deckkit roles. Hue may shift to suit the paper's content, but keep the reference's light–dark hierarchy: each role keeps roughly its reference lightness and contrast (dark title bands and headers stay dark, tints stay light, the emphasis colour stays the high-contrast highlight); record each reference colour → new colour in the brief. Separate the user's explicit requirements from incidental features of the reference.
4. **Page plan.** For every slide in `slide_plan.json`: `purpose` (the claim), `source` (paper pages/figures), `reference_slide` (the reference page whose composition fits this content's relationship and capacity, not one that merely shares a keyword), `adaptation` (what is kept, what changes for this content). Decide the relationship first: sequence, loop, hierarchy, comparison, matrix, trend, case. Split dense content rather than shrinking type.
5. **Builder.** Copy `tools/build_deck_template.py` to the project as `tools/build_deck.py` with `deckkit.py` beside it. Run `deckkit_api.py` for the exact API; never guess helpers. Set `THEME` from the brief. If the new deck belongs to the reference's organization or template, set `BASE` to the reference .pptx so its master (logo, header rule, background, page number) is inherited, and keep content out of `layouts[].decorations`. One function per slide. Text, tables, charts and diagram labels are native; draw page-specific artwork with `cv.svg(markup, ...)` (lines and shapes only, words as native text on top). Bundled icons are a generic starter set; draw new ones when the content needs them.
6. **Calibrate.** Build 2–3 representative pages first (a concept diagram, an evidence page, the cover if any). Run build, then `render_review.py compare <reference page> <our page> out.png` and look at both side by side. Revise until hierarchy, density and finish match the reference. Proceed without waiting for approval unless the user asked for a checkpoint.
7. **Whole deck.** `run_pipeline.py build --builder tools/build_deck.py --output deck.pptx --plan slide_plan.json --review-dir review`. The draft is always saved. Build output reports deckkit's estimated layout findings; render adds PowerPoint's measured findings (clipped, overlapping, off-slide text) and an ink-density comparison with the reference.
8. **Review loop.** Look at `review/slide-contact-*.png` for rhythm and consistency, then every `slide-NN.png` at full size. Fix in the builder and rebuild; repeat until clean. Then edit `review/review.json` per slide: `reviewed: true`, a specific `assessment` of what you saw, `issues: []`. Each entry in `auto_issues` must be fixed (it disappears on rebuild) or waived in `waivers` with the concrete reason it is invisible or intended. Any rebuild resets the review.
9. **Deliver.** `run_pipeline.py deliver --output deck.pptx --plan slide_plan.json --review-dir review` checks hashes, design_brief.md, plan, 16 pt floor, no full-slide pictures, and the review. Hand over the PPTX, plan, brief and builder; state approximated values and what was not verified.

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
      "adaptation": "Keep its tab-header columns and red keyword emphasis; replace its photo with a drawn loop; four nodes instead of three"
    }
  ]
}
```
