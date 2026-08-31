# Optimist Figures — skill

On-brand Optimist article figures as clean SVG, at 1600×900, delivered as an editable SVG
plus a 2× PNG. Ask for a figure in plain language; the skill handles brand geometry, the
type scale, the palette and two automated layout checks.

![Pons daily protocol revenue by fee leg](examples/pons-revenue-by-leg.png)
![What flows to $AI](examples/ai-buyback-flows.png)
![Only one bucket backs the token](examples/netnet-treasury.png)

*Three figures built with this skill. Full-resolution SVG and PNG of each are produced by
every run; these are downsampled previews.*

## Setup — three steps

**1. Install the skill.** Drop this `optimist-figures/` folder into your Claude skills
directory.

**2. Install Inter.** `apt-get install fonts-inter` (or equivalent). Without it, PNG exports
silently fall back to another typeface while the SVG stays correct — the two files disagree
and nothing warns you.

**3. Have your agent build the toolkit.** Every figure is built on a small Python module,
`scripts/okit.py`. Rather than ship a code file, paste the prompt below to your agent once.
It takes a few seconds and you can read what it writes.

---

<details open>
<summary><b>Copy this prompt to build <code>scripts/okit.py</code></b></summary>

```
Create scripts/okit.py inside the optimist-figures skill folder (make the scripts/
directory — it does not exist yet) — a small Python module for
building Optimist brand figures as SVG. No external deps beyond Pillow and cairosvg. Write
the whole module, then run the self-test at the bottom of this prompt and fix anything that
fails.

CONSTANTS
  W, H = 1600, 900          canvas
  L, R = 50, 1550           content edges
  CLEAR = 12                minimum clear space around text, in px
  BG "#D8DEF1"  SUR "#FFFFFF"  BOR "#C3CBE8"  INK "#141A2E"  BLK "#000000"
  PRI "#5B5BD6"  DARK "#37418C"  LIGHT "#8FA6E8"  AMB "#E8A63C"
  TINT "#F3F5FC"  AMBT "#FFF6E6"
  PALETTE dict with LOWERCASE string keys ("bg","sur","bor","ink","blk","pri",
  "dark","light","amb","tint","ambt") plus:
    "series": [PRI, DARK, LIGHT, "#6FBFA6", "#4E86C4", "#B27BB0"]
    "scale": {50:"#EEEEFC",100:"#DEDFF8",200:"#C0C1F1",300:"#9EA0EA",400:"#7B7BE1",
              500:"#5B5BD6",600:"#4A48B6",700:"#393893",800:"#2B2B6E",900:"#1D1D49"}
    "semantic": {"success":"#4FA98C","warning":"#E0A85B","error":"#D06A6A","info":"#4E86C4"}
    "ink700":"#3A4056"  "slate":"#838AA0"  "divider":"#E7EAF3"  "bg_light":"#E7EBF7"
    "muted": BLK          # the old muted grey is retired; body text is black

TEXT MEASUREMENT — everything depends on this being real, not estimated
  Inter faces: 400 -> Inter-Regular.otf, 600 -> Inter-SemiBold.otf, 700 -> Inter-Bold.otf
  (under /usr/share/fonts/opentype/inter/; fall back to fc-match if absent).
  Weights other than 400/600/700 snap to the nearest of the three.
  measure(text, size, weight=400) -> (width, height): render the string with PIL onto a
  scratch image and return its INK bounding box. Never estimate from character counts.
  BASELINE CONVENTION — measure() returns ink extent only, so fix the box like this: a run
  drawn at baseline y with ink height h registers from (y - h) to (y + size*0.25). The
  0.25*size tail covers descenders, which the ink height of a descender-free string omits.
  Every text box in this module uses that convention; nothing else will line up if you
  change it.

BRAND ASSETS — must work from any working directory
  Resolve assets/ relative to okit.py's own __file__, not the cwd. Read the first d="..."
  attribute out of assets/optimist-o-mark.svg and assets/optimist-logo.svg and cache it.
  Native coordinate spaces, needed to compute the scale: the O mark is viewBox 0 0 150 150
  and its ink fills that square, so 84×84 is a uniform scale of 84/150. The lockup is
  nominally 0 0 240 80 but its ink box is 240×76.5 — see footer() below.

CLASS Fig
  __init__: paints the BG rect. Holds self.el (svg element strings) and self.box (tracked
  boxes). Every box is (x0, y0, x1, y1, name, group).

  add(s)                      append a raw SVG string
  reg(x0,y0,x1,y1,name,grp=None)   register a box; grp defaults to name
  rect(x,y,w,h,fill,r=0,stroke=None,sw=1.5,track=None,grp=None)
  line(x1,y1,x2,y2,col=BOR,sw=1.5,dash=None,track=None,grp=None)
  arrow(x1,y1,x2,y2,col=PRI,sw=3,head=10,track=None,grp=None)
      Line stopping short of the tip, plus a filled triangle. With a = atan2(dy,dx),
      u = (cos a, sin a) and v = (-sin a, cos a): draw the line to (x2,y2) - u*head, and a
      polygon with vertices (x2,y2), (x2,y2) - u*1.8*head + v*0.85*head, and
      (x2,y2) - u*1.8*head - v*0.85*head.
  node(cx,cy,r=34,fill=PRI,...)                                 filled circle
  arc_arrow(cx,cy,R,a0,a1,color=PRI,sw=6,head=True)
      clockwise arc, 0 degrees = top. P(a) = (cx + R*sin(a), cy - R*cos(a)).
      large-arc flag = 1 when (a1-a0) % 360 > 180, sweep flag 1. At a1 the tangent is
      u = (cos a1, sin a1), v = (-sin a1, cos a1); head length 14, half-width 7.5, built
      the same way as arrow()'s triangle.

  text(x,y,t,size=14,w=400,fill=BLK,anchor="start",extra="",track=True,name=None,grp=None)
      Emits <text>. Computes its own ink box via measure() and registers it (respecting
      anchor: start / middle / end) unless track=False.

  lead(x,y,head,rest,size=15,grp=None,anchor="start",name=None)
      Register the box under `name`, defaulting to the first 24 characters of head.
      The house emphasis label: lead phrase PRI bold, remainder BLK regular.
      IMPORTANT — emit TWO separately positioned <text> runs, never one <text> with an
      inner <tspan>. Some renderers re-anchor a tspan under text-anchor="middle" and stack
      it on top of the rest of the line.
      IMPORTANT — XML strips a leading space in text content, so if `rest` starts with a
      space, drop it and insert an explicit gap of size*0.28 between the two runs.
      All three anchors must work. Compute hw = measure(head,size,700)[0],
      rw = measure(rest,size,400)[0], total = hw + gap + rw; then
      x0 = x (start) | x - total/2 (middle) | x - total (end). Draw head at x0, rest at
      x0 + hw + gap, and register one box spanning x0 .. x0+total.

  container(x,y,w,h,name,fill=SUR,**kw)
      Draws a card (white by default) AND registers it so check_containment() can see it. Register the box
      under the name "__box__"+name but with GROUP = the plain name, so the clearance check
      treats the card and its contents as one cluster while containment can still find it.

  sample_arrow(x1,y1,x2,y2,name,src=None,dst=None,n=9)
      Register a DIAGONAL connector as ~9 small boxes sampled along the line — never as a
      bounding box, which for a diagonal is mostly empty space and both misses real
      collisions and invents fake ones. The first two and last two samples take the groups
      of the boxes the arrow connects (src / dst), so a legitimate connection into a card
      does not read as a collision.

  header(title, sub)
      O mark from optimist-o-mark.svg at 84×84, top-left (19, 35), fill INK.
      Title  42 Bold, x=127, baseline y=65, fill INK.
      Subtitle 24 Regular, x=127, baseline y=112, fill BLK.
      Register all three in ONE group named "header" — their fixed baselines can fall under
      12px apart with tall glyphs, and that is the house geometry working, not crowding.

  footer(asof, source, note)
      Hairline #C6CDD1 at 60% opacity, 1.5px, y=808, x from L to R.
      Three rows at 12px, baselines 835 / 857 / 879, each a bold label ("Data as of: ",
      "Source: ", "Note: ") followed by regular value. All in one group "footer".
      Lockup from optimist-logo.svg at 240×77, top-left (1315, 815), fill INK. Its true ink
      box is 240×76.5, so use viewBox="0 0 240 76.5" — the nominal 240×80 letterboxes it.

  check()  -> bool          CLEARANCE
      For every pair of tracked boxes whose GROUPS DIFFER, flag any overlap or gap under
      CLEAR px. Separation between two axis-aligned boxes: ox = min(ax1,bx1) - max(ax0,bx0)
      and oy likewise; the pair is a problem when BOTH ox > -CLEAR and oy > -CLEAR, and the
      number to report is min(-ox, -oy) — negative meaning they actually overlap. Print the count tracked and either "clear" or the worst offenders with
      their actual separation. Same-group pairs are exempt.

  check_containment(pad=12) -> bool          CONTAINMENT
      A separate pass, because clearance cannot catch this: a label shares its card's group,
      so the two never collision-test and text can overflow its own box while check() says
      "clear". Check every tracked box that is NOT itself a container (the data model has no
      type tag, so "not a container" is the workable definition — a node or an arrow sample
      inside a card gets checked too, which is correct). For each, find the "__box__"
      container it sits inside and
      assert >= pad on all four sides. For each offender print the WORST side and its
      actual padding (negative when the text hangs outside the box).

  save(path)
      Write the SVG (viewBox "0 0 1600 900"), and alongside it a PNG at the same basename,
      3200×1800, via cairosvg.svg2png(output_width=3200, output_height=1800).

SELF-TEST — run this and make sure it behaves exactly as described
  f = Fig()
  f.header("Toolkit test", "header, container, both checks")
  f.container(50, 200, 700, 180, "card", r=10, stroke=BOR, sw=2)
  f.text(400, 300, "centred inside its container", 21, 400, anchor="middle", grp="card")
  f.container(820, 200, 300, 180, "tight", r=10, stroke=BOR, sw=2)
  f.text(970, 300, "a line far too long for this narrow box", 21, 400,
         anchor="middle", grp="tight")
  f.footer("Aug. 30, 2026", "self-test", "checks behave independently")
  f.check()              # must print clear — cards and their text are same-group
  f.check_containment()  # must FLAG the second one as overflowing
  f.save("toolkit_test.svg")
Then delete toolkit_test.svg / .png. If check() flags the cards against their own text, the
container grouping is wrong. If check_containment() passes, it is not finding containers.
```

</details>

---

## What's here

    README.md                     this file
    examples/                     three figures built with the skill (previews above)
    SKILL.md                      the spec — geometry, type scale, palette, editorial
                                  rules, the two checks, and how to run permutations
    assets/optimist-o-mark.svg    the "O", header top-left at 84 × 84
    assets/optimist-logo.svg      the lockup, footer lower-right at 240 × 77
    assets/optimist-color-palette.svg   swatch sheet, for humans
    references/figure-patterns.md recipes + coordinate math for timelines, radial cycles,
                                  process flows and stacked charts
    scripts/okit.py               not shipped — your agent writes it in step 3

## Using it

Trigger the skill with "make an Optimist figure", "recreate this chart on brand", or
"visual prompt, 3 permutations". `SKILL.md` is the authority on everything else — read it
before changing any number in it, since most were measured off approved figures rather
than chosen.

Two checks must print clean before any figure ships:

    f.check()              # no text within 12px of anything outside its group
    f.check_containment()  # no text closer than 12px to its own container's edge

They catch different failures, and neither can see vertical padding inside a tall box —
that stays an eyeball job.
