"""Reproduce the navy/white previews with invented data, plus the navy swatches."""
from pathlib import Path
import json

from okit import Fig, PALETTES

ROOT = Path(__file__).resolve().parents[1]
# Illustrative values only. These are not observations of any company or protocol.
VALUES = [32, 35, 30, 38, 37, 43, 46, 49, 138, 154, 68, 72, 78, 85]


def chart(palette):
    f = Fig(palette=palette)
    c = f.colors
    navy = palette == 'navy'
    f.header('A higher baseline after the spike',
             'Weekly activity index · Illustrative data · 14 weeks')
    x0, x1, y0, y1 = 122, 1276, 213, 731
    pitch = (x1 - x0) / len(VALUES)
    width = pitch * (0.56 if navy else 0.72)
    y = lambda value: y1 - value / 160 * (y1 - y0)
    if not navy:
        f.rect(119, 197, 1160, 544, c['surface'], r=8, stroke=c['grid'])
    f.rect(x0 + 8*pitch, y0, 2*pitch, y1-y0, c['event_band'])
    for value in [0, 40, 80, 120, 160]:
        f.line(x0, y(value), x1, y(value),
               c['baseline'] if value == 0 else c['grid'], 1,
               dash='3 5' if not navy and value else None)
        f.text(99, y(value)+5, str(value), 14, 600, c['secondary'],
               anchor='end', grp=f'axis {value}')
    for i, value in enumerate(VALUES):
        xc = x0 + (i + 0.5) * pitch
        color = c['historical'] if i < 8 else c['exception'] if i < 10 else c['focus']
        f.rect(xc-width/2, y(value), width, y1-y(value), color,
               track=f'bar {i}')
        if i >= 10:
            f.text(xc, y(value)-18, str(value), 16, 600, c['focus'],
                   anchor='middle', grp=f'value {i}')
        if i in [0, 2, 4, 6, 8, 10, 13]:
            f.line(xc, y1, xc, y1+7, c['baseline'], 1)
            f.text(xc, 770, f'W{i+1}', 14, 600, c['secondary'],
                   anchor='middle', grp=f'date {i}')
    baseline = sum(VALUES[:8]) / 8
    f.line(x0, y(baseline), x1, y(baseline), c['secondary'], 1, dash='5 5')
    f.text(1320, y(baseline)-8, 'Weeks 1–8 average', 16, 600,
           c['heading'], grp='reference')
    f.text(1320, y(baseline)+18, f'{baseline:.1f} index points', 15, 400,
           c['secondary'], grp='reference')
    f.rect(1320, 318, 9, 32, c['exception'], track='event swatch', grp='event legend')
    f.text(1347, 331, 'Event window', 16, 600, c['heading'], grp='event legend')
    f.text(1347, 357, 'Weeks 9–10', 15, 400, c['exception'], grp='event legend')
    f.footer('Illustrative example', 'Invented values in scripts/palette_previews.py',
             'Style demonstration only; these values do not describe a real market or protocol.')
    assert f.check()
    assert f.check_containment()
    for b in f.box:
        if b[5] in ['reference', 'event legend']:
            assert 1320 <= b[0] and b[2] <= 1550 and b[3] < 790, b
    f.save(ROOT / 'examples' / f'palette-{palette}')


def swatches():
    f = Fig(palette='navy')
    f.header('Optimist / navy palette', 'Slate ground · Steel context · Teal focus · Sand emphasis')
    for i, (role, color) in enumerate(f.colors.items()):
        x, y = 50 + (i % 6) * 253, 220 + (i // 6) * 235
        group = f'swatch {role}'
        f.rect(x, y, 225, 116, color, stroke=f.colors['baseline'], sw=1,
               track=group, grp=group)
        f.text(x, y+150, role, 17, 600, grp=group)
        f.text(x, y+179, color, 16, fill=f.colors['secondary'], grp=group)
    f.footer('Sep. 16, 2026', 'Optimist figure palette specification',
             'Use the roles the figure needs; colors do not imply positive or negative performance.')
    assert f.check()
    assert f.check_containment()
    f.save(ROOT / 'assets' / 'optimist-navy-palette')


if __name__ == '__main__':
    (ROOT / 'assets' / 'optimist-palettes.json').write_text(
        json.dumps({'default': 'white', 'palettes': PALETTES}, indent=2) + '\n')
    for palette in ['navy', 'white']:
        chart(palette)
    swatches()
