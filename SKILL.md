---
name: optimist-figures
description: Create or restyle Optimist article charts and diagrams as editable SVG and 2x PNG using the supplied brand marks, Inter fonts, measured geometry, and layout checks. Supports named navy and white palettes. Use for an Optimist figure, an on-brand article graphic, or requested variations in this house style.
---

# Optimist figures

Create evidence-backed article figures in Optimist's house style. Deliver an editable
1600 × 900 SVG and matching 3200 × 1800 PNG from one generator. Choose the palette in the request, for example:

- “Use Optimist figures skill with navy palette.”
- “Use Optimist figures skill with white palette.”

## Palette selection

| Requested palette | Treatment | Reference |
|---|---|---|
| `navy` | Dark slate, steel history, teal focus, sand event emphasis | [Navy palette](references/navy-palette.md) |
| `white` | Standard light Optimist: lavender canvas, white surfaces, periwinkle and amber, black body text | [Brand specification](references/brand-spec.md) |

An explicit palette request wins. When editing, preserve the existing palette unless
asked to switch. For a new figure without a palette request, use `white`. “White” names
the established light palette; it does not change the canvas to pure white. Treat “dark”
as `navy`, and “light,” “lavender,” or “standard” as `white`.

Initialize `Fig(palette="navy")` or `Fig(palette="white")`. Read chart colors from
`f.colors`; header, footer and primitive defaults follow that choice automatically.
`Fig()` and legacy constants remain white for compatibility. Do not import legacy
`BG`, `BLK`, or `PALETTE` for a navy figure. Palette selection changes the whole
treatment, including plot framing and typography, while preserving evidence and content.

## Workflow

1. Read [the brand specification](references/brand-spec.md). Its geometry and type scale
   are authoritative, with the [navy overrides](references/navy-palette.md) when selected. Read [figure patterns](references/figure-patterns.md) for the
   relevant chart or diagram. The assets and toolkit are resolved relative to this skill,
   never relative to the user's current directory.
2. Establish the argument from the evidence. For data figures, retain a machine-readable
   table, source URLs, retrieval time, exact window/time zone, units, and calculation.
   Name estimates and missing coverage. A tax-rate-times-volume estimate is not a record
   of executions; an execution is not proof of market impact. A reference figure supplies
   styling, not fresh evidence. Refresh live data before republishing.
3. Write a Python generator importing `scripts/okit.py`. Use bundled Inter faces and
   brand paths. Track every label and meaningful object with honest groups. Use container
   ownership for card contents and sampled boxes for diagonal connectors.
4. Run `f.check()` and `f.check_containment()` and resolve their failures before export.
   Shorten text or change geometry; do not shrink below the brand scale or hide collisions
   by merging unrelated groups. Grouping exemptions cannot replace visual inspection.
5. Call `f.save(path)` and inspect the actual PNG. Check typeface, clipping, text balance,
   label clarity, numeric consistency, and whether the title overstates the evidence.
   Keep each distinction to one naming plus its visual encoding.
6. Deliver both formats, with the data and a concise methodology when data are material.
   Keep intermediate layout JSON and generators available for reproducibility; place
   final assets in the user's requested deliverable location.

## Editorial layout preference

For comparisons built around a few key numbers, prefer an open editorial grid: large
values, shared column origins and baselines, left-aligned labels, and crisp section rules.
Let typography and spacing organize the figure; add a box only when enclosure conveys a
useful relationship. Prefer square corners when a box is needed. This is a layout preference
for editorial comparisons, not a replacement for chart axes, flow nodes, or a requested
reference style. Use the [open editorial grid recipe](references/figure-patterns.md#open-editorial-grid)
for this treatment. Preserve approved wording and data during a visual facelift; reflow the layout to accommodate them.

## Runtime

The toolkit uses Pillow for actual glyph measurements and `resvg-py` for deterministic
PNG rendering with the packaged fonts. Install these in an isolated environment as needed:

```sh
python -m pip install -r requirements.txt
```

`cairosvg` is an alternative when Cairo and these Inter faces are installed and verified
in its font resolver. Prefer the bundled-font renderer to avoid silent font substitution.
Run `python scripts/okit.py` to verify the independent clearance and containment checks:
the deliberate overflow must fail containment while clearance passes. This self-test does
not replace running both checks on the actual figure.

## Requested variations

Only produce multiple options when the user asks. Keep the researched content and brand
fixed, and vary the chart form or decomposition. Give each version a distinct brief and
stable basename. If delegation is requested or otherwise explicitly authorized, each
agent must read this skill and the brand specification; independently inspect its output.
Otherwise generate variants locally. Do not delegate ordinary single-figure requests.

## Resources

- [Renderer and palette previews](README.md#renderer): setup and reproducible examples.
- `scripts/okit.py`: measured primitives, named palettes, checks and export.
- `assets/optimist-palettes.json`: machine-readable color roles for both palettes.
- `assets/fonts/`: bundled Inter Regular, SemiBold and Bold, with their license.
