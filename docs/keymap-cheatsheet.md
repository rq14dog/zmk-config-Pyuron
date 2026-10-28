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
| 2 | `MAC_MOUSE` | 右トラックボールで自動有効（停止後3秒）。O/Pで戻る/進む、L/−で左/右クリック |
| 3 | `WIN_MOUSE` | Windowsとマウス層が有効なとき自動適用。配置はMacと共通 |
| 4 | `NUM_SYS` | Backspace長押し。左に数字・四則演算、右に対応するShift記号 |
| 5 | `NAVIGATION` | Space長押し。左に記号、右に矢印・ページ移動・Delete。Enter位置を保持してSYSTEMへ |
| 6 | `MAC_FUNCTION` | MacのEnter長押し。左にショートカット、右にF1〜F12。アプリ内一覧はApp Exposé |
| 7 | `WIN_FUNCTION` | WindowsのEnter長押し。左にショートカット、右にF1〜F12 |
| 8 | `SYSTEM` | NAVのEnter位置を保持。Bluetooth・OS切替・Bootloader |
| 9 | `SCROLL` | マウス層で左右クリックを同時に保持すると右ボールが縦スクロール。片方を離すと解除 |

## 読み方

- `primary / hold Xxx` は短く押すと primary、長押しすると Xxx です。
- `trns` は下のレイヤーを透過します。
- 空欄は物理的なキーがない位置です。
- `Mac / mode` は Bluetooth 0 を選んで `MAC_BASE` へ移動します。
- `Win / mode` は Bluetooth 1 を選んで `WIN_BASE` へ移動します。
- 左トラックボールは縦スクロール専用です。横スクロールは出力しません。
- 右トラックボールは通常カーソル移動用です。右トラックボール操作でマウスレイヤーが停止後3秒間まで自動で有効になります。Windowsでは戻る・進むがWindows用になります。
- マウス層で左右クリック（L＋−）を50ms以内に同時押しし、保持中は右ボールが縦スクロールになります（従来と上下逆方向）。片方を離すとカーソル移動へ戻ります。単独クリックには最大50msの判定待ちが入ります。
- 英数・かなコンボは入力切替後にオートマウス層を解除します。右内側は専用右Shiftです。
- NUM・NAV・FUNCTION・SYSTEMはマウス層より優先され、その間は英数・かなコンボを判定しません。
- コンボ: `Q + W -> Esc (MAC_BASE, WIN_BASE)`
- コンボ: `S + D -> Eisu (base + mouse)`
- コンボ: `K + L -> Kana (base + mouse)`
- コンボ: `L + - -> Scroll (MAC_MOUSE, WIN_MOUSE)`

## MAC_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z | X | C | V | B | Shift |  | RShift | N | M | , | . | / |
| Option | Ctrl |  |  | Cmd | Space / hold Nav |  | Bspc / hold Num | Enter / hold Mac Fn |  |  | Tab | trns |

## WIN_BASE

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q | W | E | R | T |  |  |  | Y | U | I | O | P |
| A | S | D | F | G |  |  |  | H | J | K | L | - |
| Z | X | C | V | B | Shift |  | RShift | N | M | , | . | / |
| Alt | Win |  |  | Ctrl | Space / hold Nav |  | Bspc / hold Num | Enter / hold Win Fn |  |  | Tab | Right Ctrl |

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
| trns | アプリ内一覧 / Ctrl+Down | trns | trns | アプリ終了 / hold 1s | trns |  | trns | trns | F9 | F10 | F11 | F12 |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## WIN_FUNCTION

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 最大化 / Win+Up | 行頭 / Home | ウィンドウ一覧 / Win+Tab | 行末 / End | 復元／最小化 / Win+Down |  |  |  | trns | F1 | F2 | F3 | F4 |
| 画面ロック / Win+L | 前のデスクトップ / Ctrl+Win+Left | タブ復元 / Ctrl+Shift+T | 次のデスクトップ / Ctrl+Win+Right | 範囲スクショ / Win+Shift+S |  |  |  | trns | F5 | F6 | F7 | F8 |
| trns | trns | デスクトップ表示 / Win+D | trns | 閉じる / hold 1s | trns |  | trns | trns | F9 | F10 | F11 | F12 |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |

## SYSTEM

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | Mac / mode | Win / mode | BT 2 | BT 3 | BT 4 |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns | trns |  | Boot | trns | trns | trns | BT Clr | BT All / hold 1.5s |
| trns | trns |  |  | trns | trns |  | trns | Sys / hold |  |  | trns | trns |

## SCROLL

| x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 | x10 | x11 | x12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns |  |  |  | trns | trns | trns | trns | trns |
| trns | trns | trns | trns | trns | trns |  | trns | trns | trns | trns | trns | trns |
| trns | trns |  |  | trns | trns |  | trns | trns |  |  | trns | trns |
