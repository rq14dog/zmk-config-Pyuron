# Pyuron キーマップ早見表

正本は [config/Pyuron.keymap](../config/Pyuron.keymap) と [config/Pyuron.json](../config/Pyuron.json) です。

役割分担:

- 画像版 [keymap-cheatsheet.jpg](keymap-cheatsheet.jpg): 印刷・全レイヤー一覧用。`python3 tools/render_keymap_cheatsheet.py` で正本から再生成できます。
- HTML版 [keymap-cheatsheet.html](keymap-cheatsheet.html): 画面で見る用（ダークモード対応）。キーデータは手動管理です。
- この Markdown: GitHub 上で内容を確認する用。キーデータは手動管理です。

## レイヤー

| 番号 | レイヤー | 使い方 |
| --- | --- | --- |
| 0 | `MAC_BASE` | Mac用の通常入力 |
| 1 | `MAC_OPS` | Mac用操作レイヤー。`MAC_BASE` の `Enter` 長押し |
| 2 | `WIN_BASE` | Windows用の通常入力 |
| 3 | `WIN_OPS` | Windows用操作レイヤー。`WIN_BASE` の `Enter` 長押し |
| 4 | `NUM_SYS` | 数字・記号・カーソル。Baseの `Space` 長押し |
| 5 | `SYSTEM` | Bluetooth・OS切替・Bootloader。Baseの `Esc` 長押し |
| 6 | `MOUSE` | マウスクリック用。右トラックボールを動かすと1秒間自動で有効 |

## 読み方

- `tap / hold` は短く押すと左側、長押しすると右側です。
- `trns` は下のレイヤーを透過します。
- 空欄は物理的なキーがない位置です。
- `Mac mode` は Bluetooth 0 を選んで `MAC_BASE` へ移動します。
- `Win mode` は Bluetooth 1 を選んで `WIN_BASE` へ移動します。
- コンボ: `P`（右上端）と `Esc`（右下端）の同時押しで `MAC_BASE` に戻ります。

## MAC_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / Shift | X | C | V | B | LANG1 |  | LANG2 | N | M | , | . | / / Shift |
| Tab | Ctrl |  |  | Cmd | Space / NUM_SYS |  | Backspace | Enter / MAC_OPS |  |  | Cmd | Esc / SYSTEM |

## MAC_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ctrl+Cmd+Space | Cmd+Shift+Tab | Ctrl+Up | Cmd+Tab | F11 |  |  |  | trns | Cmd+[ | Cmd+] | Ctrl+Cmd+F | Cmd+Ctrl+Q |
| trns | Ctrl+Left | Cmd+Shift+T | Ctrl+Right | Cmd+Shift+3 |  |  |  | Alt+Cmd+Esc | F2 | Cmd+M | trns | trns |
| trns | Cmd+Left | Ctrl+Down | Cmd+Right | Cmd+Shift+4 | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | Cmd+Q |

## WIN_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / Shift | X | C | V | B | LANG1 |  | LANG2 | N | M | , | . | / / Shift |
| Tab | Cmd |  |  | Ctrl | Space / NUM_SYS |  | Backspace | Enter / WIN_OPS |  |  | Ctrl | Esc / SYSTEM |

## WIN_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Win+. | Shift+Alt+Tab | Win+Tab | Alt+Tab | Win+D |  |  |  | trns | Alt+Left | Alt+Right | Win+Up | Win+L |
| trns | Ctrl+Win+Left | Ctrl+Shift+T | Ctrl+Win+Right | Win+Shift+S |  |  |  | Ctrl+Shift+Esc | F2 | Win+Down | Insert | End |
| trns | Ctrl+Home | trns | Ctrl+End | PrintScreen | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | Alt+F4 |

## NUM_SYS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PageUp | Up | PageDown | @ | ~ |  |  |  | / | 1 | 2 | 3 | - |
| Left | Down | Right | [ | ] |  |  |  | * | 4 | 5 | 6 | + |
| F6 | F7 | F8 | F9 | F10 | trns |  | trns | 0 | 7 | 8 | 9 | = |
| trns | trns |  |  | To MAC_BASE | trns |  | Delete | trns |  |  | . | Right Shift |

## SYSTEM

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | Mac mode | Win mode | BT 2 | BT 3 | BT 4 |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns | trns |  | Bootloader | trns | trns | trns | BT clear | BT clear all |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## MOUSE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | Mouse 1 | Mouse 2 | trns |
| trns | trns | trns | trns | trns | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |
