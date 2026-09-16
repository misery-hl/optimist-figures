"""Check palette routing, readable defaults, export geometry and legacy behavior."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import xml.etree.ElementTree as ET

from PIL import Image
from okit import Fig, NAVY, WHITE, DARK_ARTICLE, PALETTE


class PaletteTests(unittest.TestCase):
    def test_selection_and_legacy_imports(self):
        self.assertEqual(Fig().palette_name, 'white')
        self.assertEqual(Fig(' Navy ').palette_name, 'navy')
        self.assertEqual(Fig('dark').palette_name, 'navy')
        self.assertEqual(Fig('standard').palette_name, 'white')
        self.assertEqual(Fig('light').palette_name, 'white')
        self.assertIs(DARK_ARTICLE, NAVY)
        self.assertEqual(PALETTE['bg'], WHITE['background'])
        with self.assertRaises(ValueError):
            Fig('naavy')
        f = Fig('navy')
        f.colors['text'] = '#FFFFFF'
        self.assertEqual(Fig('navy').colors['text'], '#F0F3F6')

    def test_export_and_defaults_for_both_palettes(self):
        with TemporaryDirectory() as directory:
            for name, colors in [('navy', NAVY), ('white', WHITE)]:
                with self.subTest(palette=name):
                    f = Fig(name)
                    f.header('Palette test', 'Title and subtitle align with the Optimist O')
                    f.text(127, 200, 'Default body')
                    f.text(127, 250, 'Explicit color', fill=colors['exception'])
                    f.line(127, 280, 400, 280)
                    f.arrow(127, 320, 400, 320)
                    f.node(500, 320)
                    f.arc_arrow(700, 320, 50, 0, 90)
                    f.lead(127, 430, 'Lead', ' body')
                    f.container(800, 240, 300, 180, 'card')
                    f.text(950, 340, 'Inside', anchor='middle', grp='card')
                    f.footer('Example', 'Renderer test', 'Colors follow the selected palette.')
                    self.assertTrue(f.check())
                    self.assertTrue(f.check_containment())
                    path = Path(directory) / name
                    f.save(path)
                    root = ET.parse(path.with_suffix('.svg')).getroot()
                    ns = {'s': 'http://www.w3.org/2000/svg'}
                    labels = {e.text: e for e in root.findall('s:text', ns)}
                    self.assertEqual(labels['Default body'].get('fill'), colors['text'])
                    self.assertEqual(labels['Explicit color'].get('fill'), colors['exception'])
                    self.assertEqual(labels['Lead'].get('fill'), colors['focus'])
                    self.assertEqual(labels['body'].get('fill'), colors['text'])
                    self.assertEqual(labels['Palette test'].get('y'), '65')
                    self.assertEqual(labels['Palette test'].get('x'), '127')
                    subtitle = labels['Title and subtitle align with the Optimist O']
                    self.assertEqual(subtitle.get('y'), '112')
                    self.assertEqual(labels['Palette test'].get('font-size'), '40' if name == 'navy' else '42')
                    paths = root.findall('s:path', ns)
                    self.assertEqual(paths[0].get('transform'), 'translate(19 35) scale(.56)')
                    self.assertIn((19, 35, 103, 119, 'O', 'header'), f.box)
                    self.assertEqual(root.findall('s:line', ns)[0].get('stroke'), colors['grid'])
                    self.assertEqual(root.find('s:circle', ns).get('fill'), colors['focus'])
                    self.assertEqual(paths[1].get('stroke'), colors['focus'])
                    for p in root.findall('s:polygon', ns):
                        self.assertEqual(p.get('fill'), colors['focus'])
                    self.assertEqual(root.findall('s:rect', ns)[1].get('fill'), colors['surface'])
                    lockup = root.find('s:svg', ns)
                    self.assertEqual(lockup.get('width'), '170' if name == 'navy' else '240')
                    self.assertEqual(lockup.find('s:path', ns).get('fill'), colors['heading'])
                    with Image.open(path.with_suffix('.png')) as image:
                        self.assertEqual(image.size, (3200, 1800))
                        expected = tuple(bytes.fromhex(colors['background'][1:]))
                        self.assertEqual(image.convert('RGB').getpixel((0, 0)), expected)

    def test_palette_asset_matches_renderer(self):
        asset = Path(__file__).resolve().parents[1] / 'assets/optimist-palettes.json'
        data = json.loads(asset.read_text())
        self.assertEqual(data, {'default': 'white', 'palettes': {'white': WHITE, 'navy': NAVY}})


if __name__ == '__main__':
    unittest.main()
