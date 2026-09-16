# Figure Patterns (recipes + coordinate math)

Build computed-geometry figures with a small Python generator using `scripts/okit.py`.
Always render to PNG and eyeball before delivering. The color examples below describe
`white`; for `navy`, use the same geometry with the roles and plot treatment in
[navy-palette.md](navy-palette.md). Never carry white surfaces or black labels into navy
by copying a recipe literally.

<a id="open-editorial-grid"></a>
## Open editorial grid

Use for a few prominent rates, totals or comparisons followed by a related scenario row.

- **Structure:** lavender ground, open columns, large numbers, black section rules and
  restrained periwinkle accents. Remove decorative card backgrounds and rounded corners.
  Use enclosure only when it adds meaning.
- **Grid:** for three columns across x = 50–1550 with 30px gutters, column width is
  `(1500 - 2*30)/3 = 480`; origins are `[50, 560, 1070]`. Calculate origins once and reuse
  them for headings, values, descriptions, rules and later scenario columns. Adapt the
  column count to the content; do not force unrelated subjects into three columns.
- **Alignment:** left-align text and share baselines across peer rows. Use one measured
  type size for each row, including ranges of unequal length. Keep units attached to
  values. Avoid independent centering or per-column font sizes.
- **Hierarchy:** use 22–24 Bold headings, 80–128 Bold lead values, 18–21 descriptions, and
  42–64 Bold secondary amounts. Choose sizes from the available width and vertical budget.
  Separate sections with 1.5–2px ink rules; short 2–3px periwinkle rules can introduce
  scenario columns. These structural rules have no arrowhead or process semantics.
- **Spacing:** place label baselines using measured glyph bounds plus the toolkit's
  descender allowance. Keep at least 12px between large values and their descriptions.
  Allocate one vertical rhythm for all columns, then reflow the body when copy is added
  or removed. Preserve the footer band.
- **QA:** assert every text run stays within its column bounds, check overlap among text
  runs inside each group, then run clearance and containment and inspect the rendered PNG.
  Compare SVG text before and after a style-only edit to verify approved content survives.

## 1) Timeline (horizontal)
- Axis: horizontal line at `y_axis`, from left margin to right; arrowhead at the end (periwinkle).
- N markers evenly spaced: `x_i = x_start + i*(x_end - x_start)/(N-1)`. Each is a white dot with periwinkle ring (r≈6, sw 3).
- Cards alternate **above / below** the axis. Card = white rounded rect + centered multi-line text (ink), thin dashed periwinkle connector from marker to card.
- Date label sits on the **opposite** side of the axis from its card (keeps it uncluttered), Inter SemiBold 14 black.

## 2) Radial cycle / loop
- Centre `C=(cx,cy)`, radius `R`. Node i at angle `a_i = i*360/N` degrees (0 = top, clockwise).
- Point on circle: `P(a) = (cx + R*sin(a°), cy − R*cos(a°))`.
- Arc arrow between consecutive nodes: draw an SVG arc on radius R from `a_i+gap` to `a_{i+1}−gap` (gap ≈ 16–17°), `A R R 0 0 1 x2 y2` (sweep 1 = clockwise). Arrowhead tangent direction `u=(cos a_end°, sin a_end°)`.
- Node = periwinkle circle (r≈34) with a white line icon. Label radially outside: top→centered above, bottom→centered below, right→left-anchored, left→right-anchored. Vertically centre multi-line labels on the node.
- Centre label: short thesis line(s), lead word periwinkle.
- Optional feeder row (e.g. "mandate accelerants"): a row of white chips + periwinkle arrows below, with a short dashed up-arrow into the ring.
- `okit.Fig.arc_arrow(cx,cy,R,a0,a1,color)` does the arc + head.

## 3) Process flow
- Row of white chips (rounded, `#C3CBE8` border), centered 1–2 line labels, joined by periwinkle arrows (line + triangle). Optional left-side group label.

## 4) Stacked area / bar
- Light lavender ground. Series in the categorical order from the design system; order so adjacent bands alternate light/dark.
- Legend as swatch + name + value. Axis lines/gridlines in `#C3CBE8`; axis text black.

## 5) Two-series area + line
- Fill area = periwinkle `#5B5BD6` (the primary metric).
- Overlaid line = amber `#E8A63C`, 3px. Warm-over-cool keeps the line legible on the purple fill. (A cool line like teal muddies against purple — only use it for line-only charts.)

## Header and logo
Use `Fig(palette="white")` or `Fig(palette="navy")`, then `f.header()` and `f.footer()`.
Both methods select the matching type, colors and geometry. Both palettes retain the
canonical 84 × 84 O at (19, 35), with title/subtitle baselines at 65/112 and x=127.
Never use the retired lower-left logo recipe. See the [navy reference](navy-palette.md)
for its smaller footer lockup and continuous plot ground.
