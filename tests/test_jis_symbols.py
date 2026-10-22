"""Regression checks for the simplified shared US layout."""
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

    def test_layer_routes(self):
        self.assertEqual(list(self.layers), ['MAC_BASE', 'WIN_BASE', 'MAC_MOUSE', 'WIN_MOUSE', 'NUM_SYS', 'NAVIGATION', 'MAC_FUNCTION', 'WIN_FUNCTION', 'SYSTEM', 'SCROLL'])
        for name in ('MAC_BASE', 'WIN_BASE'):
            for position, binding in {25: '&kp LEFT_SHIFT', 26: '&mo_mouse MOUSE', 35: '&lt 5 SPACE', 36: '&lt 4 BSPC', 37: ('&lt 6 ENTER' if name == 'MAC_BASE' else '&lt 7 ENTER')}.items():
                self.assertEqual(self.layers[name][position], binding)
        self.assertIn('<&to 1>', self.source)
        self.assertIn('#define MOUSE 2', self.source)
        self.assertIn('<&zip_temp_layer 2 1000>', (ROOT / 'config/boards/shields/Pyuron/Pyuron.dtsi').read_text())

    def test_combos_follow_base_layers(self):
        for name, positions, key in [('esc', '0 1', '&kp ESC'), ('eisu', '13 14', '&eisu_input'), ('kana', '15 16', '&kana_input')]:
            body = re.search(r'combo_' + name + r' \{(.*?)\};', self.source, re.S)[1]
            for expected in [f'key-positions = <{positions}>;', f'bindings = <{key}>;', ('layers = <0 1>;' if name == 'esc' else 'layers = <0 1 2 3>;'), 'timeout-ms = <50>;']:
                self.assertIn(expected, body)

    def test_number_and_symbol_correspondence(self):
        for left, right, number in [(1,6,1),(2,7,2),(3,8,3),(11,16,4),(12,17,5),(13,18,6),(21,28,7),(22,29,8),(23,30,9),(24,31,0)]:
            self.assertEqual(self.layers['NUM_SYS'][left], f'&kp N{number}')
            self.assertEqual(self.layers['NUM_SYS'][right], f'&kp LS(N{number})')
        for position in (25,26,36,37):
            self.assertEqual(self.layers['NUM_SYS'][position], '&trans')

    def test_numeric_operators(self):
        for position,key in {0:'EQUAL',4:'MINUS',10:'DOT',14:'PLUS',20:'COMMA',32:'FSLH',33:'ASTERISK'}.items():
            self.assertEqual(self.layers['NUM_SYS'][position], '&kp '+key)

    def test_navigation_and_system(self):
        for position,key in {5:'PAGE_UP',6:'UP_ARROW',7:'PAGE_DOWN',8:'INSERT',9:'PAUSE_BREAK',15:'LEFT',16:'DOWN_ARROW',17:'RIGHT',18:'HOME',19:'END',36:'DELETE'}.items():
            self.assertEqual(self.layers['NAVIGATION'][position], '&kp '+key)
        self.assertEqual(self.layers['NAVIGATION'][25], '&kp LEFT_SHIFT')
        for name in ('NAVIGATION','SYSTEM'):
            self.assertEqual(self.layers[name][37], '&mo 8')

    def test_navigation_symbols(self):
        expected = {0:'SINGLE_QUOTE',1:'LS(SINGLE_QUOTE)',2:'SEMICOLON',3:'LS(SEMICOLON)',4:'GRAVE',10:'LBKT',11:'RBKT',12:'LS(LBKT)',13:'LS(RBKT)',14:'LS(GRAVE)',20:'BACKSLASH',21:'LS(BACKSLASH)'}
        for position, key in expected.items():
            self.assertEqual(self.layers['NAVIGATION'][position], '&kp '+key)
        for position in (22,23,24):
            self.assertEqual(self.layers['NAVIGATION'][position], '&trans')

    def test_controls_and_function_keys(self):
        self.assertEqual(self.layers['WIN_BASE'][38:40], ['&kp TAB','&kp RCTRL'])
        self.assertEqual(self.layers['MAC_BASE'][39], '&none')
        for position,number in zip([6,7,8,9,16,17,18,19,28,29,30,31],range(1,13)):
            for name in ('MAC_FUNCTION', 'WIN_FUNCTION'):
                self.assertEqual(self.layers[name][position], f'&kp F{number}')

    def test_base_tab_and_modifiers(self):
        for name in ('MAC_BASE', 'WIN_BASE'):
            self.assertEqual(self.layers[name][38], '&kp TAB')
        self.assertEqual(self.layers['WIN_BASE'][32], '&kp LEFT_ALT')
        self.assertEqual(self.layers['WIN_BASE'][34], '&kp LCTRL')
        self.assertEqual(self.layers['MAC_BASE'][32], '&kp LEFT_ALT')
        self.assertEqual(self.layers['MAC_BASE'][34], '&kp LGUI')

    def test_function_left_column_empty(self):
        for position in (5,15,27):
            for name in ('MAC_FUNCTION', 'WIN_FUNCTION'):
                self.assertEqual(self.layers[name][position], '&trans')

    def test_function_shortcuts(self):
        expected = {
            'MAC_FUNCTION': {0:'LC(LG(F))',1:'LG(LEFT_ARROW)',2:'LC(UP_ARROW)',3:'LG(RIGHT_ARROW)',4:'LG(M)',10:'LG(LC(Q))',11:'LC(LEFT)',12:'LS(LG(T))',13:'LC(RIGHT)',14:'LG(LS(NUMBER_4))',21:'LC(DOWN_ARROW)'},
            'WIN_FUNCTION': {0:'LG(UP)',1:'HOME',2:'LG(TAB)',3:'END',4:'LG(DOWN)',10:'LG(L)',11:'LC(LG(LEFT_ARROW))',12:'LC(LS(T))',13:'LC(LG(RIGHT_ARROW))',14:'LG(LS(S))',22:'LG(D)'},
        }
        left_positions = set(range(5)) | set(range(10,15)) | set(range(20,25))
        for name, shortcuts in expected.items():
            for position in left_positions:
                binding = '&kp ' + shortcuts[position] if position in shortcuts else '&trans'
                if position == 24:
                    binding = '&exit_hold ' + ('LG(Q)' if name == 'MAC_FUNCTION' else 'LA(F4)') + ' 0'
                self.assertEqual(self.layers[name][position], binding)

    def test_mouse_os_routes_and_positions(self):
        for name, back, forward in [('MAC_MOUSE','LG(LBKT)','LG(RBKT)'),('WIN_MOUSE','LA(LEFT)','LA(RIGHT)')]:
            expected = {8:'&kp '+back,9:'&kp '+forward,18:'&mkp MB1',19:'&mkp MB2'}
            for position, binding in enumerate(self.layers[name]):
                self.assertEqual(binding, expected.get(position, '&trans'))
        self.assertRegex(self.source, r'if-layers = <1 2>;\s*then-layer = <3>;')
        self.assertRegex(self.source, r'excluded-positions = <\s*8 9 18 19 25 26 32 33 34 39\s*>;')
        self.assertIn('require-prior-idle-ms = <200>;', self.source)

    def test_dedicated_shift_and_guarded_exit(self):
        for name in ('MAC_BASE', 'WIN_BASE'):
            self.assertEqual(self.layers[name][20], '&kp Z')
            self.assertEqual(self.layers[name][31], '&kp SLASH')
            self.assertEqual(self.layers[name][25], '&kp LEFT_SHIFT')
        for name in ('MAC_FUNCTION','WIN_FUNCTION'):
            self.assertEqual(self.layers[name][20], '&trans')
            self.assertEqual(self.layers[name][25], '&trans')
        behavior = re.search(r'exit_hold:.*?\n        };', self.source, re.S)[0]
        for expected in ['tapping-term-ms = <1000>;', 'flavor = "tap-preferred";', 'bindings = <&kp>, <&none>;']:
            self.assertIn(expected, behavior)
        from render_keymap_cheatsheet import label_for
        self.assertEqual(label_for('&exit_hold LG(Q) 0','MAC_FUNCTION').hint, 'hold 1s')
        self.assertEqual(label_for('&exit_hold LA(F4) 0','WIN_FUNCTION').primary, '閉じる')

    def test_mouse_hold_lock_and_language_exit(self):
        behavior = re.search(r'mo_mouse:.*?\n        };', self.source, re.S)[0]
        self.assertIn('compatible = "zmk,behavior-momentary-layer";', behavior)
        self.assertIn('locking;', behavior)
        for name, key in [('eisu_input', 'LANG2'), ('kana_input', 'LANG1')]:
            body = re.search(name + r':.*?\n        };', self.source, re.S)[0]
            self.assertIn('<&macro_tap &kp ' + key + '>', body)
            self.assertIn('<&macro_release &mo MOUSE>', body)
            self.assertNotIn('&mo_mouse', body)
            self.assertNotIn('&to ', body)
            self.assertNotIn('&tog ', body)
        from render_keymap_cheatsheet import label_for
        self.assertEqual(label_for('&mo_mouse MOUSE','MAC_BASE').primary, 'Mouse')
        self.assertEqual(label_for('&eisu_input','MAC_BASE').primary, 'Eisu')
        self.assertEqual(label_for('&kana_input','WIN_BASE').primary, 'Kana')

    def test_mouse_priority_cannot_enable_combos_over_utilities(self):
        names = list(self.layers)
        mouse_index = max(names.index('MAC_MOUSE'), names.index('WIN_MOUSE'))
        for name in ('NUM_SYS','NAVIGATION','MAC_FUNCTION','WIN_FUNCTION','SYSTEM'):
            self.assertGreater(names.index(name), mouse_index)
        excluded = set(map(int, re.search(r'excluded-positions = <([^>]+)>;', self.source)[1].split()))
        self.assertTrue({8,9,18,19,25,26,32,33,34,39} <= excluded)
        self.assertTrue({13,14,15,16,20,31,35,36,37,38}.isdisjoint(excluded))

    def test_scroll_combo_only_while_both_clicks_held(self):
        body = re.search(r'combo_scroll \{(.*?)\};', self.source, re.S)
        self.assertIsNotNone(body)
        for expected in ('key-positions = <18 19>;', 'layers = <2 3>;',
                         'bindings = <&mo 9>;', 'timeout-ms = <50>;'):
            self.assertIn(expected, body[1])
        self.assertNotIn('slow-release', body[1])
        self.assertEqual(self.layers['SCROLL'], ['&trans'] * 40)

    def test_right_scroll_replaces_cursor_and_blocks_horizontal(self):
        source = (ROOT / 'config/boards/shields/Pyuron/Pyuron.dtsi').read_text()
        listener = source.split('trackball_listener_R:')[1].split('default_transform:')[0]
        override = re.search(r'scroll_mode \{(.*?)\};', listener, re.S)
        self.assertIsNotNone(override)
        body = override[1]
        self.assertIn('layers = <9>;', body)
        self.assertNotIn('process-next', body)
        processors = ['<&zip_xy_transform (INPUT_TRANSFORM_XY_SWAP)>',
                      '<&zip_xy_scaler 1 16>', '<&zip_xy_to_scroll_mapper>',
                      '<&zip_scroll_transform (INPUT_TRANSFORM_X_INVERT | INPUT_TRANSFORM_Y_INVERT)>',
                      '<&horizontal_scroll_blocker 0 1>', '<&zip_temp_layer 2 1000>']
        offsets = [body.index(processor) for processor in processors]
        self.assertEqual(offsets, sorted(offsets))
        self.assertIn('<&zip_xy_scaler 3 4>', listener.split('scroll_mode')[0])

    def test_guarded_clear(self):
        self.assertEqual(self.layers['SYSTEM'][31], '&bt_clear_hold 0 0')
        behavior = re.search(r'bt_clear_hold:.*?\n        };', self.source, re.S)[0]
        for expected in ['tapping-term-ms = <1500>;', 'flavor = "tap-preferred";', 'bindings = <&clear_all_bonds>, <&none>;']:
            self.assertIn(expected, behavior)

    def test_renderer_matches_layers(self):
        from render_keymap_cheatsheet import DOC_LAYER_ORDER, LAYER_NAMES, label_for
        self.assertEqual(DOC_LAYER_ORDER, list(self.layers))
        self.assertEqual(LAYER_NAMES['4'], 'Num')
        self.assertEqual(LAYER_NAMES['5'], 'Nav')
        for number,symbol in enumerate(')!@#$%^&*('):
            self.assertEqual(label_for(f'&kp LS(N{number})','NUM_SYS').primary,symbol)
        self.assertEqual(label_for('&none','WIN_BASE').primary, '')


if __name__ == '__main__':
    unittest.main()
