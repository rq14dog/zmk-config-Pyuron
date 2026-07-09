# Pyuron キーマップ早見表

正本は [config/Pyuron.keymap](../config/Pyuron.keymap) と [config/Pyuron.json](../config/Pyuron.json) です。
このファイルは `tools/render_keymap_cheatsheet.py` が正本から自動生成します。手動編集しないでください。

役割分担:

- 画像版 [keymap-cheatsheet.jpg](keymap-cheatsheet.jpg): 印刷・全レイヤー一覧用。
- HTML版 [keymap-cheatsheet.html](keymap-cheatsheet.html): 画面で見る用（ダークモード対応、フィルタ・表示密度切替あり）。
- この Markdown: GitHub 上で内容を確認する用。

いずれも `python3 tools/render_keymap_cheatsheet.py` で正本から再生成できます。

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

- `primary / hold Xxx` は短く押すと primary、長押しすると Xxx です。
- `trns` は下のレイヤーを透過します。
- 空欄は物理的なキーがない位置です。
- `Mac / mode` は Bluetooth 0 を選んで `MAC_BASE` へ移動します。
- `Win / mode` は Bluetooth 1 を選んで `WIN_BASE` へ移動します。
- コンボ: `P + Esc -> To Mac`

## MAC_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | Kana |  | Eisu | N | M | , | . | / / hold RShift |
| Tab | Ctrl |  |  | Cmd | Space / hold Num |  | Bspc | Enter / hold Mac Ops |  |  | Cmd | Esc / hold Sys |

## MAC_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ctrl+Cmd+Space | Cmd+Shift+Tab | Ctrl+Up | Cmd+Tab | F11 |  |  |  | trns | Cmd+[ | Cmd+] | Ctrl+Cmd+F | Cmd+Ctrl+Q |
| trns | Ctrl+Left | Shift+Cmd+T | Ctrl+Right | Cmd+Shift+3 |  |  |  | Alt+Cmd+Esc | F2 | Cmd+M | trns | trns |
| trns | Cmd+Left | Ctrl+Down | Cmd+Right | Cmd+Shift+4 | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | Cmd+Q |

## WIN_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | Kana |  | Eisu | N | M | , | . | / / hold RShift |
| Tab | Win |  |  | Ctrl | Space / hold Num |  | Bspc | Enter / hold Win Ops |  |  | Ctrl | Esc / hold Sys |

## WIN_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Win+. | Shift+Alt+Tab | Win+Tab | Alt+Tab | Win+D |  |  |  | trns | Alt+Left | Alt+Right | Win+Up | Win+L |
| trns | Ctrl+Win+Left | Ctrl+Shift+T | Ctrl+Win+Right | Win+Shift+S |  |  |  | Ctrl+Shift+Esc | F2 | Win+Down | Ins | End |
| trns | Ctrl+Home | trns | Ctrl+End | PrtSc | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | Alt+F4 |

## NUM_SYS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PgUp | Up | PgDn | @ | ~ |  |  |  | / | 1 | 2 | 3 | - |
| Left | Down | Right | [ | ] |  |  |  | * | 4 | 5 | 6 | + |
| F6 | F7 | F8 | F9 | F10 | trns |  | trns | 0 | 7 | 8 | 9 | = |
| trns | trns |  |  | To Mac | trns |  | Del | trns |  |  | . | RShift |

## SYSTEM

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | Mac / mode | Win / mode | BT 2 | BT 3 | BT 4 |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns | trns |  | Boot | trns | trns | trns | BT Clr | BT All |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## MOUSE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | LClick | RClick | trns |
| trns | trns | trns | trns | trns | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |
