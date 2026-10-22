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
| 1 | `WIN_BASE` | Windows用の通常入力 |
| 2 | `NUM_SYS` | Backspace長押し。左に数字・四則演算、右に対応するShift記号 |
| 3 | `NAVIGATION` | Space長押し。左に記号、右に矢印・ページ移動・Delete。Enter位置を保持してSYSTEMへ |
| 4 | `MAC_FUNCTION` | MacのEnter長押し。左にショートカット、右にF1〜F12。アプリ内一覧はApp Exposé |
| 5 | `WIN_FUNCTION` | WindowsのEnter長押し。左にショートカット、右にF1〜F12 |
| 6 | `SYSTEM` | NAVのEnter位置を保持。Bluetooth・OS切替・Bootloader |
| 7 | `MAC_MOUSE` | 右トラックボールで自動有効（1秒）。右内側キーでも開けます。O/Pで戻る/進む、L/−で左/右クリック |
| 8 | `WIN_MOUSE` | Windowsとマウス層が有効なとき自動適用。配置はMacと共通 |

## 読み方

- `primary / hold Xxx` は短く押すと primary、長押しすると Xxx です。
- `trns` は下のレイヤーを透過します。
- 空欄は物理的なキーがない位置です。
- `Mac / mode` は Bluetooth 0 を選んで `MAC_BASE` へ移動します。
- `Win / mode` は Bluetooth 1 を選んで `WIN_BASE` へ移動します。
- 左トラックボールは縦スクロール専用です。横スクロールは出力しません。
- 右トラックボールは常時カーソル移動用です。右トラックボール操作でマウスレイヤーが1秒間自動で有効になります。右内側キーからも開けます。Windowsでは戻る・進むがWindows用になります。
- コンボ: `Q + W -> Esc (MAC_BASE, WIN_BASE)`
- コンボ: `F + G -> Eisu (MAC_BASE, WIN_BASE)`
- コンボ: `H + J -> Kana (MAC_BASE, WIN_BASE)`

## MAC_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | trns |  | Mouse / hold | N | M | , | . | / / hold RShift |
| Option | Ctrl |  |  | Cmd | Space / hold Nav |  | Bspc / hold Num | Enter / hold Mac Fn |  |  | Tab | trns |

## WIN_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z / hold Shift | X | C | V | B | trns |  | Mouse / hold | N | M | , | . | / / hold RShift |
| Alt | Win |  |  | Ctrl | Space / hold Nav |  | Bspc / hold Num | Enter / hold Win Fn |  |  | Tab | Right Ctrl |

## NUM_SYS

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| = | 1 | 2 | 3 | - |  |  |  | trns | ! | @ | # | trns |
| . | 4 | 5 | 6 | + |  |  |  | trns | $ | % | ^ | trns |
| , | 7 | 8 | 9 | 0 | trns |  | trns | trns | &amp; | * | ( | ) |
| / | * |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## NAVIGATION

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ' | " | ; | : | &#96; |  |  |  | PgUp | Up | PgDn | Ins | Pause |
| [ | ] | { | } | ~ |  |  |  | Left | Down | Right | Home | End |
| &#92; | &#124; | trns | trns | trns | Shift |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | Del | Sys / hold |  |  | trns | trns |

## MAC_FUNCTION

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 全画面 / Ctrl+Cmd+F | 行頭 / Cmd+Left | ウィンドウ一覧 / Ctrl+Up | 行末 / Cmd+Right | 最小化 / Cmd+M |  |  |  | trns | F1 | F2 | F3 | F4 |
| 画面ロック / Cmd+Ctrl+Q | 前のデスクトップ / Ctrl+Left | タブ復元 / Shift+Cmd+T | 次のデスクトップ / Ctrl+Right | 範囲スクショ / Cmd+Shift+4 |  |  |  | trns | F5 | F6 | F7 | F8 |
| アプリ終了 / Cmd+Q | アプリ内一覧 / Ctrl+Down | trns | trns | trns | trns |  | trns | trns | F9 | F10 | F11 | F12 |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## WIN_FUNCTION

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 最大化 / Win+Up | 行頭 / Home | ウィンドウ一覧 / Win+Tab | 行末 / End | 復元／最小化 / Win+Down |  |  |  | trns | F1 | F2 | F3 | F4 |
| 画面ロック / Win+L | 前のデスクトップ / Ctrl+Win+Left | タブ復元 / Ctrl+Shift+T | 次のデスクトップ / Ctrl+Win+Right | 範囲スクショ / Win+Shift+S |  |  |  | trns | F5 | F6 | F7 | F8 |
| 閉じる / Alt+F4 | trns | デスクトップ表示 / Win+D | trns | trns | trns |  | trns | trns | F9 | F10 | F11 | F12 |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## SYSTEM

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | Mac / mode | Win / mode | BT 2 | BT 3 | BT 4 |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns | trns |  | Boot | trns | trns | trns | BT Clr | BT All / hold 1.5s |
| trns | trns |  |  | trns | trns |  | trns | Sys / hold |  |  | trns | trns |

## MAC_MOUSE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | 戻る / Cmd+[ | 進む / Cmd+] |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | LClick | RClick |
| trns | trns | trns | trns | trns | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## WIN_MOUSE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | 戻る / Alt+Left | 進む / Alt+Right |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | LClick | RClick |
| trns | trns | trns | trns | trns | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |
