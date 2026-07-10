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
- 左トラックボールは縦スクロール専用です。横スクロールは出力しません。
- 右トラックボールはカーソル移動用で、動かすと `MOUSE` が1秒間有効になります。
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
| 絵文字/記号 / Ctrl+Cmd+Space | 前のアプリ / Cmd+Shift+Tab | Mission Control / Ctrl+Up | アプリ切替 / Cmd+Tab | F11 |  |  |  | trns | 戻る / Cmd+[ | 進む / Cmd+] | フルスクリーン / Ctrl+Cmd+F | 画面ロック / Cmd+Ctrl+Q |
| trns | デスクトップ移動 / Ctrl+Left | 閉じたタブを復元 / Shift+Cmd+T | デスクトップ移動 / Ctrl+Right | 全画面スクショ / Cmd+Shift+3 |  |  |  | 強制終了 / Alt+Cmd+Esc | F2 | 最小化 / Cmd+M | trns | trns |
| trns | 行頭 / Cmd+Left | App Exposé / Ctrl+Down | 行末 / Cmd+Right | 範囲スクショ / Cmd+Shift+4 | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | 終了 / Cmd+Q |

## WIN_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | Kana |  | Eisu / hold Alt | N | M | , | . | / / hold RShift |
| Tab | Win |  |  | Ctrl | Space / hold Num |  | Bspc | Enter / hold Win Ops |  |  | Ctrl | Esc / hold Sys |

## WIN_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 絵文字/記号 / Win+. | 前のアプリ / Shift+Alt+Tab | タスクビュー / Win+Tab | アプリ切替 / Alt+Tab | デスクトップ表示 / Win+D |  |  |  | trns | 戻る / Alt+Left | 進む / Alt+Right | 最大化 / Win+Up | 画面ロック / Win+L |
| trns | デスクトップ移動 / Ctrl+Win+Left | 閉じたタブを復元 / Ctrl+Shift+T | デスクトップ移動 / Ctrl+Win+Right | 範囲スクショ / Win+Shift+S |  |  |  | タスクマネージャ / Ctrl+Shift+Esc | 名前変更 / F2 | 最小化 / Win+Down | Ins | End |
| trns | 先頭 / Ctrl+Home | trns | 末尾 / Ctrl+End | スクショ / PrtSc | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | 終了 / Alt+F4 |

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
