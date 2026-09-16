# Navy palette

Select with “Use Optimist figures skill with navy palette.” This is the approved
September 16, 2026 slate/steel/teal/sand treatment. `white` selects the standard light
Optimist palette. Preserve an existing palette unless a switch is requested.

## Palette

After completing the [local renderer update](local-renderer-update.md), select navy
through the local API: conventionally `Fig(palette="navy")` and `f.colors`, or an
equivalent configuration. These interfaces must be implemented locally, not downloaded.
The machine-readable [palettes](../assets/optimist-palettes.json),
[swatch sheet](../assets/optimist-navy-palette.svg) and
[illustrative chart](../examples/palette-navy.png) show the colors together.
If local generators import `DARK_ARTICLE`, preserve it as a navy alias during the update.

| Role | Hex | Use |
|---|---|---|
| `background` | `#151D27` | Continuous canvas and plot ground |
| `text` | `#F0F3F6` | Headline, important labels, brand marks |
| `secondary` | `#B6C1CE` | Subtitle, axes, legend detail |
| `muted` | `#91A0B1` | Source and methodology footer |
| `grid` | `#2C3744` | Thin solid horizontal gridlines and footer rule |
| `baseline` | `#506071` | Zero baseline and restrained tick marks |
| `historical` | `#668097` | Historical/context series |
| `exception` | `#C6A571` | Exceptional periods or event emphasis |
| `focus` | `#55CBB6` | Current period or principal series |
| `event_band` | `#20242A` | Very faint shading behind an event window |
| `surface` | `#20242A` | Enclosure only when needed to communicate a relationship |
| `heading` | `#F0F3F6` | Header and brand marks |

Color roles are not a fixed legend for every subject. Name what they encode in the
current figure. Use only the colors the comparison needs; do not invent a rainbow
or imply that teal always means positive performance.

## Treatment

- Use one continuous dark canvas. Avoid a white plot card, enclosing frame, shadows,
  gradients, decorative badges, and heavy vertical axes.
- Thin solid gridlines, a subtle zero baseline, and generous spacing let data lead.
  For short weekly bar series, bars around 0.55–0.60 of slot width worked well; optional
  2px top rounding should leave the zero baseline square. Use true proportional geometry.
- Keep the title's reference period explicit when claiming growth. Separate a temporary
  spike from the baseline being compared. A sigma label needs the measured variable,
  frequency, baseline window, and calculation; do not borrow a market-return sigma for fees.
- Use the supplied O path at **84 × 84, top-left (19, 35)**. Do not shrink or redraw it.
  On this dark ground, both Optimist marks use `text` rather than black.
- Approved compact header: Inter 40 SemiBold, **x=127, baseline 65**; subtitle 22 Regular,
  **x=127, baseline 112**. Align the title's visible top with the O's top at y=35,
  and keep the subtitle within its y=35–119 height. Reflow a long title instead of squeezing it. These are
  dark-theme alternatives to the light type scale, not instructions to change wording.
- A right-side legend is appropriate when requested. Keep it compact and aligned to the
  plot, without restoring deleted explanatory panels or oversized statistics.
- Use the compact footer with 12px type at baselines 836/858/880 and a small **170 × 54.2** lockup
  at (1380, 828). The O at top left retains its canonical size even with this smaller footer.
- Preserve 1600 × 900 live-text SVG and 3200 × 1800 PNG exports, clearance/containment
  checks, and visual inspection. The reference supplies styling, never reusable data.

The chart preview uses invented, clearly labeled values to demonstrate styling. Never
reuse its claims, dates or data in research. The visual reference demonstrates
layout; it does not require a spike, legend or annotation in every chart.

Use the selected palette for text, rules and marks as well as data series. The
[local renderer contract](local-renderer-update.md) defines default behavior and exact
geometry for each palette, independent of the implementation on any one machine.
