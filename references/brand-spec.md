

# Optimist Stylized Figures

Publication-ready figures in Optimist's house style: calm and flat, with an approved
`navy` palette and the original lavender/periwinkle palette, named `white`. Built as
self-contained **SVG** at **1600×900**, and delivered as **both an SVG and a 2× PNG**.

Use `white` for new figures unless another palette is requested; preserve the palette
when editing. With `navy`, the [navy palette](navy-palette.md) overrides the color, header
type, footer lockup and plot treatment below. Both retain the canonical O and export checks.

## Say it once
Every claim gets **one naming plus its encoding** — never a caption restating what a shape,
colour, line style or heading has already said. Before shipping, take each distinction the
figure draws and count where it appears. If the count is above one naming, cut back to one.

A worked failure: a diagram split fees into programmatic and discretionary routes and said
so in the subtitle, again in both column headers, again in the card bodies, again in solid
versus dashed lines — and then again in a pair of labels sitting on the arrows. Five
statements of one idea. The arrow labels went, and nothing was lost.

What this rule cuts, in order of how often it shows up:
- **Labels on connectors** that name the relationship the connector's style already encodes.
- **Tier or group captions** describing what the row visibly is.
- **A caption under the plot** repeating the headline or the legend.
- **A second sentence in the Note** qualifying the first.
- **Axis or series labels** echoing a title that already names the measure.

When a distinction is encoded visually, name it **once** — at the highest level a reader
meets it, usually the subtitle or a column header — and let the encoding work everywhere
else. Deleting a redundant label is never a loss of clarity.

## Every figure ships in two formats
Always produce both, from the same generator run, under the same basename:
- **`<name>.svg`** — the editable master. Imports cleanly into Figma; text stays live.
- **`<name>.png`** — **3200 × 1800** (2×), for dropping straight into a draft or a deck.

Use `Fig.save()` with the packaged Inter faces, preferably via `resvg-py`, as explained
in the skill entrypoint. CairoSVG is an alternative only when its font resolver has been
verified against these faces. The PNG must match the live text in the SVG.

## The two automated checks — both must pass

### 1. Clearance — text is never crowded
Every piece of text keeps **≥ 12px of clear space** from anything that is not part of its own
label group. As the generator emits each label, record its bounding box (measure real text
width with PIL against the Inter faces) with a `group` id; after emitting, compare every
pair whose groups differ and report anything closer than 12px.

**Label groups** — clusters that are *deliberately* close, exempt from each other:
- **The header cluster** — "O" mark, title and subtitle are ONE group. Their fixed baselines
  (65 and 112 for a one-line title) can fall under 12px apart with tall glyphs; that is the
  house geometry working, not crowding. Use the explicit two-line-title geometry below
  when needed, rather than nudging baselines or shrinking the type to satisfy the check.
- A bold label and its sublabel (21px apart) · a legend swatch and its text · the footer rows
  and lockup · a rule or arrow and the label annotating it · a card and its contents.

**Diagonal arrows must not register a bounding box** — a diagonal's bbox is mostly empty
space, so it misses real collisions and invents fake ones. Register ~9 sample points along
the line, with the endpoint samples in the groups of the boxes the arrow connects.

### 2. Containment — text never overflows its own box
The clearance check **cannot** catch this: a label is grouped *with* its card, so the two are
exempt from each other and a text run can hang out of its own container and still print
"clear". A hub subtext once shipped 7px proud of its pad on both sides that way.

So run a **second, separate pass**: for every text run, find the container it sits inside
and assert **≥ 12px of padding on all four sides**. Report the offenders with their actual
padding. Fix by widening the box or shortening the line — never by shrinking the type below
the scale.

Open layouts have no enclosing cards: assert that each text run fits its assigned column
and the usable content band instead of adding invisible card containers. Check text pairs
within each column for overlap too; shared group IDs exempt them from the clearance check.
Include the toolkit's descender allowance below a baseline when placing the next label.
Leave deliberate space between a large number and its description, not just nonoverlap.

### Fix the cause, not the symptom
- **Two rules saying the same thing** — draw one and let it do both jobs.
- **A decoration competing for the label's space** — cut the decoration.
- **Two rows too close** — move one; don't shrink the type.
- **A mis-grouped cluster** — if the flag is between things that belong together, fix the
  grouping, not the layout.
Nudging 2px to squeak past a check is never the fix. Both checks still have one blind spot:
content sitting top-heavy inside a tall box. Vertical padding is an eyeball job.

## White palette — standard light defaults
- **Background** `#D8DEF1`. **Optional surfaces/cards** `#FFFFFF` with a `#C3CBE8` hairline.
- **Editorial comparisons:** default to an open grid with aligned type and crisp rules.
  Use enclosure when it clarifies grouping; prefer square corners to rounded cards.
- **Primary accent**: periwinkle `#5B5BD6`.
- **Text is black.** Titles and headings ink `#141A2E`; subtitles, axis labels, date labels,
  legend text, captions and footer rows **`#000000`**. Muted `#5A6072` is retired.
- **Chart accent**: amber `#E8A63C`.
- **Flat only** — no gradients, shadows, glows, textures.
- **Emphasis rule**: lead phrase periwinkle bold, remainder ink.
- **Line style carries meaning.** Solid periwinkle for automatic or guaranteed, dashed amber
  for discretionary or conditional — and once it does, don't also label it.

## White palette geometry — measured, not approximated
| | value |
|---|---|
| Canvas | 1600 × 900 |
| Left / right content edge | **x = 50** and **x = 1550** |
| "O" mark | **84 × 84**, top-left at **(19, 35)** |
| Title | 42 Bold, x = **127**, baseline **y = 65** |
| Subtitle | 24 Regular, x = **127**, baseline **y = 112** |
| Footer divider | `#C6CDD1` @ 60%, 1.5px, **y = 808**, x 50 → 1550 |
| Footer rows | 12px, bold label + regular value, baselines **835 / 857 / 879** |
| Optimist lockup | **240 × 77**, top-left at **(1315, 815)** |

The lockup's true ink box is 240 × 76.5 — render with `viewBox="0 0 240 76.5"` at 240 × 77.
The "O" ink fills its 150 × 150 viewBox, so 84 × 84 is a uniform scale.
**Content must end above y ≈ 790.**

For an approved title that needs two lines, keep 42 Bold at x = 127 with baselines
65 / 111, then place the 24 Regular subtitle at baseline 151. Keep the brand marks and
footer fixed; begin the body below the expanded header and reflow the remaining space.

## White palette type scale
| element | size / weight |
|---|---|
| Title | 42 Bold |
| Subtitle | 24 Regular |
| Axis tick labels, date labels | **14 SemiBold** |
| Y-axis title (rotated) | 20 Regular |
| Card headings | 22–24 Bold |
| Card body / node labels | 17–21 |
| Editorial section / column headings | 22–24 Bold |
| Editorial display values | 80–128 Bold for lead values; 42–64 Bold for secondary amounts |
| Editorial value descriptions / assumptions | 18–21 Regular |
| Legend text | **12 Regular**, swatch 15 × 15, 22px swatch-to-text gap |
| Footer rows | **12** |
| Event annotations | 12 Bold / 12 Regular, 21px apart |

**Size card text to fill its box, but share one scale across sibling cards.** Fit to the
*narrowest* card's longest line and apply that size to all of them. Centre the content in
its box, vertically and horizontally, unless the card is a list. Leave real margin: a line
within ~10px of the inner edge reads as jammed, and under 12px fails the containment check.

For open grids, left-align headings, values and descriptions to the same column origin.
Use one size and baseline per row of peer values, selected to fit the longest value.
Display values are typographic callouts, not proportional chart marks. Do not imply a
quantitative comparison through font size; use a chart when relative magnitude needs encoding.

## White palette chart plot box
- Plot rect **x 119 → 1550, y 197 → 741**, white, `#C3CBE8` hairline, r = 8.
- Gridlines dashed `3 5`; tick labels right-aligned at x ≈ 105.
- Date labels every 4th point, baseline ≈ y 765.
- Legend: a single **centred** row under the plot at y ≈ 784–799.
- Bars ≈ 0.72 × slot pitch; stack so adjacent bands alternate light/dark.
- Event rules dashed `5 4`, label 9px right at baseline `Y0+27`, sublabel `Y0+48`.

## Editorial rules
- **The title is an argument, not a description** — or a question the figure answers.
- **No standalone caption in or under the plot.** The explanatory sentence goes in the Note.
- **The Note carries what the chart cannot show.** One sentence.
- **Dates are US style**: "July 13 – Aug 29, 2026"; "Data as of: Aug. 29, 2026".
- **When content is deleted, rescale to fill.**
- **Show the argument, don't narrate it.**
- **Check the arrows against the title.**
- **Keep one word per idea.** If the subtitle says "programmatic", the header doesn't say
  "automatic".

## Workflow
1. **Pick the figure type** and open `references/figure-patterns.md`.
2. **Generate the SVG** with a Python generator over `scripts/okit.py`. Track label boxes.
3. **Run both checks** — clearance and containment. Fix every failure at its cause.
4. **Render and LOOK.** Then read the figure back for repetition.
5. **Export the pair and deliver both** — `<name>.svg` plus `<name>.png` at 3200 × 1800.

## Live data
Figures built from a live dashboard go stale, and past days can be **revised** — the Pons
terminal once moved a settled day by 89%. Re-pull before republishing rather than appending
to a cached series, put the pull date in **Data as of**, and if the newest points are
incomplete, say so in the Note rather than presenting a floor as a measurement. When two
sources disagree, check whether they measure different things — fees paid by traders and
revenue kept by the protocol differ by several times over.

## Reading back an edited figure
Figma exports have **text outlined to paths**. Parse path bounding boxes (`svgelements`),
group into rows by y, and solve each font size by **width-matching** against Inter with PIL.
Width beats ink height, and correct sizes land on round numbers.

## Renderer gotchas
- **No `<tspan>` inside a `text-anchor="middle"` element** — some renderers re-anchor it,
  stacking it on the rest of the line. Emit two separately positioned `<text>` runs.
- **XML strips a leading space** in text content, so adjacent runs butt together. Add the gap
  explicitly as a fraction of the font size.

## Quality bar
- **Nothing is said twice.**
- **Both checks pass** — clearance and containment — with correct grouping. A pass earned by
  mis-grouping is not a pass.
- Both files delivered — SVG and 2× PNG, same basename.
- Nothing clips the canvas or the footer band.
- One consistent theme; use its specified text colors.
- Sibling cards share one type scale, sized to fill, content centred.
- Open-grid columns share left edges, row baselines and type sizes; same-column text does
  not overlap even when it shares a clearance group. Rules end on the grid edges.
- Both brand marks present; preserve the canonical O geometry and the selected theme's lockup size.

## Assets
- `assets/optimist-o-mark.svg` — the "O" icon, header top-left. Never a plain circle.
- `assets/optimist-logo.svg` — the full lockup, footer lower-right at 240 × 77.
- `assets/optimist-color-palette.svg` — the original white palette swatch sheet.
- `assets/optimist-palettes.json` — color roles for `white` and `navy`.
- `scripts/okit.py` — palette, canvas, header/footer at the measured geometry (header as one
  group), text/rect/arrow primitives, a two-run lead-phrase helper, arrow sampling for
  diagonals, the clearance and containment checks, and a `save()` that writes the SVG and
  the 2× PNG together.
