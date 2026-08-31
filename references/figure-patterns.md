# Figure Patterns (recipes + coordinate math)

Build computed-geometry figures with a small Python generator using `scripts/okit.py`.
Always render to PNG and eyeball before delivering.

## 1) Timeline (horizontal)
- Axis: horizontal line at `y_axis`, from left margin to right; arrowhead at the end (periwinkle).
- N markers evenly spaced: `x_i = x_start + i*(x_end - x_start)/(N-1)`. Each is a white dot with periwinkle ring (r≈6, sw 3).
- Cards alternate **above / below** the axis. Card = white rounded rect + centered multi-line text (ink), thin dashed periwinkle connector from marker to card.
- Date label sits on the **opposite** side of the axis from its card (keeps it uncluttered), Inter Semi Bold 13 muted.

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
- Legend as swatch + name + value. Axis lines/gridlines in `#C3CBE8`; axis text ink/muted.

## 5) Two-series area + line
- Fill area = periwinkle `#5B5BD6` (the primary metric).
- Overlaid line = amber `#E8A63C`, 3px. Warm-over-cool keeps the line legible on the purple fill. (A cool line like teal muddies against purple — only use it for line-only charts.)

## Header & logo (all figures)
- Header: title (Inter Bold 30–34) + subtitle (muted). Optional small "O" mark.
- **Logo lower-left** is required — `okit.Fig.logo(...)` stamps `assets/optimist-logo.svg`.
