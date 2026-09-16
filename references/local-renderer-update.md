# Build or update your local renderer

This repository distributes instructions, brand assets and visual references. It does
**not distribute Python or other executable scripts**. Each person's agent maintains
their own local renderer. Matching behavior and appearance is the goal; identical source
code, filenames, dependencies or internal APIs are not required.

Read this when installing the skill, updating an older copy, or when the local renderer
does not support both named palettes. If it already satisfies this contract, use it.

## Update an existing installation

1. Locate the installed skill and the renderer its figure generators actually import.
   It may be named `scripts/okit.py`, but inspect the local files instead of assuming that
   path, a `Fig` class, or any particular helper already exists. Read existing imports and
   call sites before changing their interfaces.
2. Back up local scripts and customizations outside the checkout before refreshing the
   skill from `main`. Preserve those files when installing the new Markdown, palette JSON,
   fonts, logos and examples. Do not replace a locally generated renderer with someone
   else's implementation or delete it because the shared repository has no scripts.
3. Adapt the existing renderer to the behavior below. Preserve established method names,
   positional arguments, explicit color overrides and working white figures. Add a small
   adapter if needed. If no renderer exists, create one locally using the construction
   contract later in this document.
4. Run the acceptance checks below and inspect both PNGs. Report what was updated and
   where the local renderer lives. Keep generated scripts and test harnesses local;
   repository updates should contain instructions and reference assets only.

## Named palette behavior

- Accept `navy` and `white`, ignoring surrounding whitespace and capitalization. Map
  `dark` and `dark-article` to navy; map `light`, `lavender` and `standard` to white.
  Report an unknown name instead of silently choosing a palette.
- An explicit user request wins. Preserve the existing palette on edits unless a switch
  is requested. Use white for new figures when no palette is specified.
- Read the exact roles from [optimist-palettes.json](../assets/optimist-palettes.json).
  Give each figure its own palette configuration. Creating a navy figure must not change
  the defaults of a later white figure.
- A Python renderer using `Fig` should support `Fig(palette="navy")` and
  `Fig(palette="white")`, expose the selected role map as `f.colors`, and keep `Fig()`
  equivalent to white. With another API, implement the same behavior in its configuration
  and document the local entry point. Do not assume these new interfaces exist before
  completing the update.
- Preserve legacy white constants and imports where present, including `BG`, `BLK` and
  `PALETTE`. If callers import `DARK_ARTICLE`, retain it as a navy alias. Do not change a
  global `BG` or `BLK` to switch one figure to navy.

## Apply the palette throughout the figure

Resolve defaults from the current figure when drawing, rather than freezing light colors
in function default arguments. An explicitly supplied color still wins.

| Element | Default role |
|---|---|
| Canvas | `background` |
| Body text | `text` |
| Subtitle, axis labels and legend detail | `secondary` |
| Header title and both brand marks | `heading` |
| Generic rules and gridlines | `grid` |
| Zero baseline and ticks | `baseline` |
| Arrows, nodes and a bold lead phrase | `focus` |
| Remainder of a lead phrase | `text` |
| Container fill, when enclosure is needed | `surface` |
| Historical/context data | `historical` |
| Principal/recent data | `focus` |
| Exceptional periods | `exception` |
| Faint event-window shading | `event_band` |
| Footer values | `muted` |

Raw SVG elements, chart generators and helper defaults can all contain hard-coded light
colors. Inspect those call sites too; changing only the canvas is insufficient. Replace
implicit light defaults with palette roles without changing explicitly chosen encodings,
source data, wording, windows or calculations. Only use an event color/band when the
current figure has a supported event; do not copy the preview's narrative into research.

## Header, footer and plot treatment

Both palettes keep the supplied O path at **84 × 84**, top-left **(19, 35)**. Its native
viewBox is 150 × 150, so `translate(19 35) scale(.56)` is the correct path transform.
Never substitute a circle. One-line titles and subtitles start at **x=127**, with
baselines **65** and **112**. The palette must not move them lower.

| Element | White | Navy |
|---|---|---|
| Title | Inter 42 Bold, `heading` | Inter 40 SemiBold, `heading` |
| Subtitle | Inter 24 Regular, `secondary` | Inter 22 Regular, `secondary` |
| Footer rule | y=808, x=50–1550, `#C6CDD1` at 60%, 1.5px | y=810, x=50–1550, `grid`, 1px |
| Footer row baselines | 835 / 857 / 879 | 836 / 858 / 880 |
| Footer labels | 12 Bold, `secondary` | 12 SemiBold, `secondary` |
| Footer values | 12 Regular, `muted` | 12 Regular, `muted` |
| Full lockup | (1315,815), 240 × 77 | (1380,828), 170 × 54.2 |
| Plot | White surface with hairline, dashed grid | Continuous navy canvas, thin solid horizontal grid |

The lockup uses the supplied path with **viewBox `0 0 240 76.5`**, filled with `heading`.
Footer rows are Data as of, Source and Note. Measure each label and value separately,
with about 5–6px between them; stop text at least 25px before the logo. Keep body content
above approximately y=790. Reflow long copy instead of shrinking the marks or type.

Use [brand-spec.md](brand-spec.md) for white plot geometry, type scale, and long titles;
use [navy-palette.md](navy-palette.md) for navy styling. Navy removes the white plot card,
enclosing frame and heavy vertical axes. It uses restrained horizontal rules, steel
context, teal focus and sand for exceptions. A compact right-side legend is appropriate
when the chart needs it. Palette selection includes these treatments, not just colors.

## Construction contract when no renderer exists

Create a small local SVG toolkit, conventionally `scripts/okit.py`, or an equivalent
module suited to the environment. Keep it outside version control. The following
capabilities are required; a different existing API can provide equivalent operations.

- **Canvas and assets:** use a 1600 × 900 viewBox, content edges x=50/1550 and 12px minimum
  clearance. Resolve assets relative to the installed skill or module, never the working
  directory or another person's absolute path. Read the provided O and lockup paths.
- **Fonts and measurements:** use the packaged Inter Regular, SemiBold and Bold faces
  for both measurement and raster export. Snap intermediate weights to 400/600/700.
  Measure actual glyph ink bounds, for example with Pillow at 4× size then divided by 4;
  never estimate width from character counts. Track a text run at baseline y from
  y minus its ink height through y plus 0.25×font-size for descenders, and adjust x for
  start/middle/end anchors. XML-escape text.
- **Primitives:** provide text, rectangles, lines, arrows with geometric heads, nodes,
  arcs with tangent arrowheads, and an escape hatch for raw SVG. Respect explicit fill,
  stroke, width, dash and anchor arguments. Use the per-figure defaults above.
- **Tracking:** maintain measured object bounds plus a name and group. Group only objects
  intentionally belonging together. Record diagonal connectors with about nine small
  sample boxes along the actual path; put endpoint samples in the connected groups.
- **Lead phrase:** draw the bold focus-colored lead and regular text-colored remainder
  as separately positioned text runs. Measure their combined width for alignment; add an
  explicit gap of roughly 0.28×font-size when needed. Do not rely on a leading XML space
  or centered nested `tspan` elements.
- **Containers:** register a container with identifiable ownership, such as `__box__name`
  and group `name`, then assign its contents to that group. Ownership must find overflow
  even if the overflowing label's center falls outside the box.
- **Header and footer:** implement the exact palette-specific geometry above using the
  actual brand paths and fonts. Track the header cluster as one group and the footer
  cluster as one group; visually inspect within those groups too.
- **Clearance:** for bounds from different groups, flag a collision or separation under
  12px on both axes, and flag canvas overflow. Intentional same-group relationships are
  exempt. Report offending names and measured gaps.
- **Containment:** separately require at least 12px padding on each side of content owned
  by a container. Report the worst side and actual padding. A clearance pass cannot
  substitute for this check. In open grids, also check assigned column bounds and
  same-column text overlap without inventing containers.
- **Export:** save editable live-text SVG at 1600 × 900 plus a matching 3200 × 1800 PNG
  under one basename, and retain layout measurements locally. `resvg-py` can render
  directly from packaged font files without system-font substitution. CairoSVG or another
  existing renderer is acceptable if it is verified to use the same Inter faces. Install
  needed dependencies locally; no shared requirements file or script download is assumed.

## Acceptance checks

1. Exercise both natural-language requests from `SKILL.md` and confirm they select the
   correct palette configuration. Also check an unspecified new figure defaults to white,
   an existing navy figure stays navy on an unrelated edit, and an explicit switch wins.
2. Render the same clearly illustrative chart in white and navy using the local toolkit.
   The [preview data](../examples/palette-preview-data.json) can reproduce the reference
   comparison; its numbers are invented. Inspect [white](../examples/palette-white.png)
   and [navy](../examples/palette-navy.png) for the intended appearance. Check the bar/line
   colors, text, grids, marks, header alignment, footer and plot surface, not just the
   background. Verify ordinary primitive defaults and explicit color overrides too.
3. Confirm both PNGs are 3200 × 1800, both SVGs retain live text and a 1600 × 900 viewBox,
   Inter is used, both marks are present, and normal figures pass clearance and containment.
4. Render one existing white figure before and after the update. Its intended appearance
   and content should remain unchanged. Create a navy figure followed by a default white
   figure to catch accidental changes to global defaults. Check existing imports still work.
5. Verify that a deliberately overflowing label grouped with its container can pass
   clearance but fails containment. A small local fixture can use a 300px-wide container
   with centered text whose measured width exceeds that width. Do not ship that fixture.
6. Keep scripts, dependencies and generated test output local. Report the checks actually
   completed; do not claim that updating Markdown alone updated or tested a renderer.
