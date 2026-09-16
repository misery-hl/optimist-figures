# Optimist figures

Create editable article charts and diagrams with Optimist marks, Inter typography,
measured layout checks, and two named palettes. Every figure ships as a **1600 × 900
SVG** and a matching **3200 × 1800 PNG**.

## Choose a palette

> Use Optimist figures skill with navy palette.

Navy uses a continuous slate canvas, muted steel for context, teal for focus, and sand
for exceptional periods. It includes the compact article typography and footer, with
the canonical Optimist O and aligned title/subtitle.

[![Navy palette example](examples/palette-navy.png)](examples/palette-navy.svg)

> Use Optimist figures skill with white palette.

White is the familiar light Optimist treatment: **lavender canvas, white surfaces,
periwinkle and amber accents, black body text**. The name preserves that established
palette; it does not replace the canvas with pure white.

[![White palette example](examples/palette-white.png)](examples/palette-white.svg)

Both previews use the same invented values, solely to demonstrate styling.
Explicit palette requests take precedence. Edits keep the existing palette unless a
switch is requested. New figures default to white when no palette is specified.

## Install or update your local skill

This is an **instructions-and-assets repository**. Python files and other executable
scripts are generated and maintained locally by each person's agent; they are not part
of the shared package. The implementation and filenames may differ between colleagues.

Give your agent this update request:

> Update my installed Optimist figures skill from the latest `main` branch of
> https://github.com/misery-hl/optimist-figures. Back up and preserve my local renderer
> and customizations while refreshing the shared instructions and assets. Read `SKILL.md`
> and `references/local-renderer-update.md`, then inspect and adapt my own renderer to
> support the named navy and white palettes. If I have no renderer, build it locally
> from those instructions. Apply the palette to text, lines, charts, header and footer;
> preserve existing white behavior and the canonical Optimist O alignment. Render and
> inspect both palettes and run the specified layout and compatibility checks. Keep all
> generated scripts local. Report the changes and checks actually completed.

An agent doing a fresh installation should place the repository's instructions and
assets together in an `optimist-figures` skill folder, then follow the same local setup
reference. An agent updating an existing installation must inspect its renderer rather
than assume that a shared `okit.py` or a particular Python API exists. Refreshing the
Markdown alone does not implement the palette support in an older renderer.

## Local renderer contract

[Build or update your local renderer](references/local-renderer-update.md) gives the
implementation behavior, exact palette routing, default color roles, header/footer
geometry, compatibility requirements, construction contract and acceptance checks.
It works for a fresh installation and an existing toolkit with different code.

Once adapted, a Python toolkit using `Fig` should accept `Fig(palette="navy")` and
`Fig(palette="white")`; another renderer can expose equivalent configuration. The agent
must verify or implement that interface locally before using it. The repository supplies
no Python implementation or test scripts to download.

- [SKILL.md](SKILL.md): palette selection, setup trigger and figure workflow.
- [Local renderer update](references/local-renderer-update.md): instructions for each agent.
- [Brand specification](references/brand-spec.md): standard white palette, geometry and checks.
- [Navy specification](references/navy-palette.md): navy colors and article treatment.
- [Figure patterns](references/figure-patterns.md): chart and diagram recipes.
- [Palette JSON](assets/optimist-palettes.json) and [navy swatches](assets/optimist-navy-palette.svg).
- [Illustrative preview data](examples/palette-preview-data.json): optional fixture for local verification.
- [Inter license](assets/fonts/LICENSE.txt): license for the bundled fonts.

The SVG and PNG previews are references for appearance. They do not supply research
claims or source data for a new figure. Keep executable scripts out of repository commits;
`.gitignore` excludes the local toolkit directory and Python files.

## Earlier figures

These examples show other chart and diagram forms in the standard light palette.
Their historical data and wording are not a substitute for fresh sources.

![Revenue by leg](examples/pons-revenue-by-leg.png)
![AI buyback flows](examples/ai-buyback-flows.png)
![Treasury comparison](examples/netnet-treasury.png)
