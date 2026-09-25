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
| 5 | `SYSTEM` | Bluetooth・OS切替・Bootloader。NUM_SYSのDelete右隣を押している間だけ有効。離すと戻る |
| 6 | `SYMBOLS` | 元英数キーを保持。US記号27種類。数字のShift記号を維持し、右側は左詰め |
| 7 | `FUNCTION` | 元かなキーを保持。右手側4列×3行にF1〜F12 |
| 8 | `MOUSE` | マウスクリック用。右トラックボールを動かすと1秒間自動で有効 |

## 読み方

- `primary / hold Xxx` は短く押すと primary、長押しすると Xxx です。
- `trns` は下のレイヤーを透過します。
- 空欄は物理的なキーがない位置です。
- `Mac / mode` は Bluetooth 0 を選んで `MAC_BASE` へ移動します。
- `Win / mode` は Bluetooth 1 を選んで `WIN_BASE` へ移動します。
- 左トラックボールは縦スクロール専用です。横スクロールは出力しません。
- 右トラックボールはカーソル移動用で、動かすと `MOUSE` が1秒間有効になります。
- コンボ: `Q + W -> Esc (MAC_BASE, WIN_BASE)`
- コンボ: `D + F -> Eisu (MAC_BASE, WIN_BASE)`
- コンボ: `J + K -> Kana (MAC_BASE, WIN_BASE)`

## MAC_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | Fn / hold |  | Symbols / hold | N | M | , | . | / / hold RShift |
| Tab | Ctrl |  |  | Cmd | Space / hold Num |  | Bspc | Enter / hold Mac Ops |  |  | Cmd | Esc |

## MAC_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 絵文字/記号 / Ctrl+Cmd+Space | 行頭 / Cmd+Left | Mission Control / Ctrl+Up | 行末 / Cmd+Right | trns |  |  |  | trns | 戻る / Cmd+[ | 進む / Cmd+] | フルスクリーン / Ctrl+Cmd+F | 画面ロック / Cmd+Ctrl+Q |
| trns | デスクトップ移動 / Ctrl+Left | 閉じたタブを復元 / Shift+Cmd+T | デスクトップ移動 / Ctrl+Right | 全画面スクショ / Cmd+Shift+3 |  |  |  | 強制終了 / Alt+Cmd+Esc | trns | 最小化 / Cmd+M | trns | trns |
| trns | trns | App Exposé / Ctrl+Down | trns | 範囲スクショ / Cmd+Shift+4 | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | 終了 / Cmd+Q |

## WIN_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | Fn / hold |  | Symbols / hold | N | M | , | . | / / hold RShift |
| Tab | Win |  |  | Alt | Space / hold Num |  | Bspc | Enter / hold Win Ops |  |  | Ctrl | Right Ctrl |

## WIN_OPS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 絵文字/記号 / Win+. | 行頭 / Home | タスクビュー / Win+Tab | 行末 / End | デスクトップ表示 / Win+D |  |  |  | trns | 戻る / Alt+Left | 進む / Alt+Right | 最大化 / Win+Up | 画面ロック / Win+L |
| trns | デスクトップ移動 / Ctrl+Win+Left | 閉じたタブを復元 / Ctrl+Shift+T | デスクトップ移動 / Ctrl+Win+Right | 範囲スクショ / Win+Shift+S |  |  |  | タスクマネージャ / Ctrl+Shift+Esc | trns | 最小化 / Win+Down | trns | trns |
| trns | trns | trns | trns | スクショ / PrtSc | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | 終了 / Alt+F4 |

## NUM_SYS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| / | 1 | 2 | 3 | - |  |  |  | PgUp | Up | PgDn | Ins | Pause |
| * | 4 | 5 | 6 | + |  |  |  | Left | Down | Right | Home | End |
| = | 7 | 8 | 9 | 0 | Shift |  | RShift | trns | trns | trns | trns | trns |
| . | trns |  |  | trns | trns |  | Del | Sys / hold |  |  | trns | trns |

## SYSTEM

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | Mac / mode | Win / mode | BT 2 | BT 3 | BT 4 |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns | trns |  | Boot | trns | trns | trns | BT Clr | BT All / hold 1.5s |
| trns | trns |  |  | trns | trns |  | trns | Sys / hold |  |  | trns | trns |

## SYMBOLS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ? | ! | @ | # | trns |  |  |  | [ | ] | { | } | &#92; |
| ' | $ | % | ^ | _ |  |  |  | ; | : | &#124; | < | > |
| " | &amp; | * | ( | ) | trns |  | trns | &#96; | ~ | , | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## FUNCTION

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | F1 | F2 | F3 | F4 | trns |
| trns | trns | trns | trns | trns |  |  |  | F5 | F6 | F7 | F8 | trns |
| trns | trns | trns | trns | trns | trns |  | trns | F9 | F10 | F11 | F12 | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## MOUSE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | LClick | RClick | trns |
| trns | trns | trns | trns | trns | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |
