"""Regression checks for the shared US layout (formerly JIS tests)."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from pyuron_keymap import parse_layers


class SharedUsLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'config/Pyuron.keymap').read_text()
        cls.layers = {layer.name: layer.bindings for layer in parse_layers(cls.source)}

    def test_shared_layer_routes(self):
        self.assertEqual(list(self.layers), ['MAC_BASE', 'MAC_OPS', 'WIN_BASE', 'WIN_OPS', 'NUM_SYS', 'SYSTEM', 'SYMBOLS', 'FUNCTION', 'MOUSE'])
        for name in ('MAC_BASE', 'WIN_BASE'):
            self.assertEqual(self.layers[name][35], '&lt 4 SPACE')
        for name in ('NUM_SYS', 'SYSTEM'):
            self.assertEqual(self.layers[name][37], '&mo 5')
        self.assertIn('<&zip_temp_layer 8 1000>', (ROOT / 'config/boards/shields/Pyuron/Pyuron.dtsi').read_text())
        self.assertNotIn('jis', self.source)

    def test_controls_and_escape(self):
        self.assertEqual(self.layers['WIN_BASE'][39], '&kp RCTRL')
        self.assertEqual(self.layers['WIN_BASE'][38], '&kp LCTRL')
        self.assertEqual(self.layers['MAC_BASE'][39], '&kp ESC')
        self.assertEqual(re.findall(r'combo_\w+\s*\{', self.source), ['combo_esc {', 'combo_eisu {', 'combo_kana {'])
        self.assertRegex(self.source, r'(?s)combo_esc \{.*?key-positions = <0 1>;.*?bindings = <&kp ESC>;.*?layers = <0 2>;')

    def test_line_navigation_and_guarded_clear(self):
        self.assertEqual(self.layers['WIN_OPS'][1], '&kp HOME')
        self.assertEqual(self.layers['WIN_OPS'][3], '&kp END')
        self.assertEqual(self.layers['SYSTEM'][31], '&bt_clear_hold 0 0')
        behavior = re.search(r'bt_clear_hold:.*?\n        };', self.source, re.S)[0]
        self.assertIn('tapping-term-ms = <1500>;', behavior)
        self.assertIn('flavor = "tap-preferred";', behavior)
        self.assertIn('bindings = <&clear_all_bonds>, <&none>;', behavior)
        self.assertNotIn('hold-while-undecided', behavior)
        self.assertIn('bindings = <&bt BT_CLR_ALL>;', self.source)

    def test_number_layer_shifts_preserve_base_keys(self):
        numbers = self.layers['NUM_SYS']
        self.assertEqual(numbers[25], '&kp LEFT_SHIFT')
        self.assertEqual(numbers[26], '&kp RIGHT_SHIFT')
        self.assertEqual(numbers[24], '&kp N0')
        self.assertEqual(numbers[20], '&kp EQUAL')
        for position in (33, 34, 38, 39):
            self.assertEqual(numbers[position], '&trans')
        for name in ('MAC_BASE', 'WIN_BASE'):
            self.assertEqual(self.layers[name][25], '&mo 7')
            self.assertEqual(self.layers[name][26], '&mo 6')

    def test_language_combos(self):
        for name, positions, target in [('eisu', '12 13', 'LANG2'), ('kana', '16 17', 'LANG1')]:
            body = re.search(r'combo_' + name + r' \{(.*?)\};', self.source, re.S)[1]
            self.assertIn('key-positions = <' + positions + '>;', body)
            self.assertIn('bindings = <&kp ' + target + '>;', body)
            self.assertIn('layers = <0 2>;', body)
            self.assertIn('timeout-ms = <50>;', body)

    def test_new_layer_contents(self):
        for position, number in [(1, 1), (2, 2), (3, 3), (11, 4), (12, 5), (13, 6), (21, 7), (22, 8), (23, 9), (24, 0)]:
            self.assertEqual(self.layers['SYMBOLS'][position], f'&kp LS(N{number})')
        for position, number in zip([5, 6, 7, 8, 15, 16, 17, 18, 27, 28, 29, 30], range(1, 13)):
            self.assertEqual(self.layers['FUNCTION'][position], f'&kp F{number}')
        self.assertEqual(self.layers['SYMBOLS'][20], '&kp LS(SINGLE_QUOTE)')
        for position in (0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21):
            self.assertEqual(self.layers['FUNCTION'][position], '&trans')
        for name in ('SYMBOLS', 'FUNCTION'):
            for position in (25, 26, 33, 34, 38):
                self.assertEqual(self.layers[name][position], '&trans')

    def test_shifted_number_labels(self):
        from render_keymap_cheatsheet import label_for
        for number, symbol in enumerate(')!@#$%^&*('):
            self.assertEqual(label_for(f'&kp LS(N{number})', 'SYMBOLS').primary, symbol)

    def test_symbol_coverage_and_no_duplicate_function_keys(self):
        import string
        from render_keymap_cheatsheet import label_for
        symbols = [label_for(binding, 'SYMBOLS').primary for binding in self.layers['SYMBOLS'] if binding.startswith('&kp ')]
        self.assertEqual(set(symbols), set(string.punctuation) - set('/-+=.'))
        self.assertEqual(len(symbols), len(set(symbols)))
        for position in (4, 30, 31, 32, 39):
            self.assertEqual(self.layers['SYMBOLS'][position], '&trans')
        for name, bindings in self.layers.items():
            if name != 'FUNCTION':
                self.assertFalse(any(re.fullmatch(r'&kp F[0-9]+', binding) for binding in bindings), name)
        for name in ('MAC_OPS', 'WIN_OPS'):
            for position in (16, 19, 27, 28, 29, 30, 31):
                self.assertEqual(self.layers[name][position], '&trans')
        for position in (27, 28, 29, 30, 31):
            self.assertEqual(self.layers['NUM_SYS'][position], '&trans')

    def test_numeric_operators_and_decimal(self):
        for position, key in {0: 'FSLH', 4: 'MINUS', 10: 'ASTERISK', 14: 'PLUS', 20: 'EQUAL', 32: 'DOT'}.items():
            self.assertEqual(self.layers['NUM_SYS'][position], '&kp ' + key)

    def test_left_symbol_column(self):
        for position, key in {0: 'LS(SLASH)', 10: 'SINGLE_QUOTE', 20: 'LS(SINGLE_QUOTE)'}.items():
            self.assertEqual(self.layers['SYMBOLS'][position], '&kp ' + key)
        for position in (30, 31, 39):
            self.assertEqual(self.layers['SYMBOLS'][position], '&trans')

    def test_packed_right_symbols(self):
        from render_keymap_cheatsheet import label_for
        positions = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 27, 28, 29]
        labels = ''.join(label_for(self.layers['SYMBOLS'][position], 'SYMBOLS').primary for position in positions)
        self.assertEqual(labels, '[]{}' + chr(92) + ';:|<>`~,')

    def test_us_symbols(self):
        self.assertEqual(self.layers['WIN_BASE'][19], '&kp MINUS')
        for position in (19, 27, 28, 29, 30, 31):
            self.assertEqual(self.layers['WIN_OPS'][position], self.layers['MAC_OPS'][position])


if __name__ == '__main__':
    unittest.main()
