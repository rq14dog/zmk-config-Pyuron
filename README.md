# ファームウェア更新手順とキーマップの編集

## キーマップ早見表

現在生成済みの早見表を以下に表示します。拡大する場合は画像をクリックしてください。

Mac／Windowsとも端末側をUS配列に設定して使う構成です。NUM_SYSは共通で、Windows専用のJIS変換レイヤーはありません。

- Spaceは短押しで空白、長押しでNAVIGATION。Backspaceは短押しで文字削除、長押しでNUM_SYSです。Enterは短押しでEnter、長押しでOS別のFUNCTIONです。
- Mac／Windows OPSは削除済み。必要なショートカットをMAC_FUNCTION／WIN_FUNCTIONの左側に配置しました。絵文字・全画面撮影・強制終了画面は配置していません。
- NUM_SYSは左側に数字・四則演算・＝・小数点・カンマ、右側に対応する数字のShift記号を配置しています。左端は上から＝・小数点・カンマ、左下2キーは／・＊です。数字と＋・−の位置は維持しています。NUM保持中は左下2キーの修飾キーが／・＊に置き換わります。0は左下段の右端です。NUM_SYSの専用左右Shiftは外しました。
- NAVIGATIONは左側に引用符・セミコロン・コロン・括弧・バッククォート・波線・バックスラッシュ・パイプ、右側に矢印・PgUp／PgDn・Home／End・Insert・Pauseを配置。Backspace位置がDelete、Enter位置を保持するとSYSTEMです。左内側には範囲選択用のShiftを残しています。
- Enterを長押しするとMacではMAC_FUNCTION、WindowsではWIN_FUNCTION。F1〜F12は右手側の右4列×3行です。左内側は専用左Shiftで、Zとスラッシュの長押しShiftは廃止しています。右内側は専用右Shiftです。
- SYMBOLSを削除しました。数字のShift記号以外の括弧・引用符などはNAVIGATION左側に配置しています。ベースの句読点は維持しています。
- 英数はS＋D、かなはK＋L、EscはQ＋Wのコンボです（50ms判定。Escは両OSのベースのみ、英数・かなはベースとマウス層）。
- Windows右下は右Ctrl、その左はTab。WindowsのSpace左隣は左Ctrl、元Tab位置の左下はAltです。Macも右下の端から2番目がTabで、元Tab位置はOptionです。MacのSpace左隣はCmdを維持しています。Mac右下は無効です。MacのEscはQ＋Wコンボで入力します。
- FUNCTION左側はQ/W/E/R/T＝全画面（Windowsは最大化）／行頭／ウィンドウ一覧／行末／最小化（Windowsは復元・最小化）、A/S/D/F/G＝画面ロック／前のデスクトップ／タブ復元／次のデスクトップ／範囲スクショ。B位置を1秒保持するとMacでアプリ終了、Windowsでウィンドウを閉じます。短押しは無効で、Z位置はベースの通常Zを透過します。MacのXはアプリ内一覧、WindowsのCはデスクトップ表示です。
- マウス操作は右端2列。O＝戻る、P＝進む、L＝左クリック、−＝右クリック。右トラックボール操作で停止後3秒間まで自動で有効になります。戻る・進むはOSに合わせて自動切り替えします。その間O/P/L/−は文字入力になりません。カーソル移動は保持不要です。オートマウスはキー入力後200msの待機条件を維持し、O/P/L/−と専用Shift・Alt/Option・Ctrl・Cmd/Win・右Ctrlは解除対象から除外しています。
- S＋D／K＋Lは英数／かなを送信してオートマウス層を解除します。右内側は右Shiftで、手動Mouseキーはありません。新たにボールを動かすと、200msの待機条件を満たした場合に再び自動で開きます。
- NUM・NAV・FUNCTION・SYSTEMをマウス層より上に配置し、操作中の英数・かなコンボ誤発火を防ぎます。
- マウス層で左クリック＋右クリック（L＋−）を50ms以内に同時押しし、両方を保持している間だけ右トラックボールが縦スクロールになります（従来と上下逆方向）。片方を離すとカーソル移動に戻ります。内部のSCROLLレイヤーで切り替え、左右クリック自体は送信しません。判定時間を超えて押した場合は通常のクリックになります。単独クリックには最大50msの判定待ちが入ります。左ボールのスクロールとオートマウスは維持しています。スクロールの方向・速度・クリックの感触は実機未確認です。
- SYSTEMの「BT All」は1.5秒長押しで全Bluetooth接続設定を消去します。「BT Clr」は単押しです。
- 灰色は透過を示します。ただしMacベース右下の空きキーは無効です。

[![Pyuron キーマップ早見表](docs/keymap-cheatsheet.jpg)](docs/keymap-cheatsheet.jpg)

[HTML版](docs/keymap-cheatsheet.html) / [テキスト版](docs/keymap-cheatsheet.md)

## ZMK Studioによるキーマップの編集
### 手順1. 有線接続でキーマップを変更する場合は[ZMK Studio](https://zmk.studio/)にアクセス
### 手順2. 中央にある"USB"をクリックしてデバイスを選択することでキーマップの編集が可能になります。
### 手順3. 無線接続でキーマップを変更する場合は[ZMK Studioネイティブアプリ](https://zmk.studio/download)にアクセスしてファイルをダウンロード
### 手順4. インストール後に起動、接続中のデバイスが表示されるのでデバイスを選択するとキーマップの編集が可能になります。

## Keymap-Editorによるキーマップの編集 (Githubアカウントが必要になります)
### 手順1. [Pyuronリポジトリ](https://github.com/MeowCatpawkittie/zmk-config-Pyuron) リポジトリをFork
### 手順2. Actionsタブを選択して"I understand my workflows, go ahead and enable them"をクリック
### 手順3. [Keymap-Editor](https://nickcoutsos.github.io/keymap-editor/)にアクセス
### 手順4. Githubでログインをしたあと"Only select repositories"を選択、"Add Repository"をクリック
### 手順5. 再度"Only select repositories"を選択、"Install"をクリック
### 手順6. キーマップが表示され、編集可能になります。
### 手順7. 編集が完了したら左上の"Save"をクリック、ビルドが完了すると"Latest"からダウンロードできます。
### ダウンロードしたファームウェアは以下の手順で書き込んでください。

## ファームウェアの書き込み

### 手順1. PCと右側ボードを接続します。
### 手順2. 表にあるリセットスイッチ用のボタンを2回素早く押すとブートローダーが起動して"XIAO SENSE"として認識されます。
### 手順3. まずは"XIAO SENSE"ドライブに"settings_reset-seeeduino_xiao_ble-zmk.uf2"を書き込みます。
### 手順4. 次に同じ手順でブートローダーを起動し"Pyuron_R rgbled_adapter-seeeduino_xiao_ble-zmk"を書き込みます。
### 手順5. 右側が終わったら左側も同じように"settings_reset-seeeduino_xiao_ble-zmk.uf2"から"Pyuron_L rgbled_adapter-seeeduino_xiao_ble-zmk"を書き込みます。
### 手順6. 書き込みが完了したら念の為1回リセットボタンを押してください。
### 手順7. 左右どちらも電源をオンにしたあとにBlutoothデバイスの追加から"Pyuron"を選択し、接続ができたらファームウェアの書き込みは完了です。


#### ・ファームウェアの書き込みの際エラーが出ていても実際には正常で書き込めています。手順を進めて問題ありません。
#### ・ファームウェアを更新する際は一度PC側のデバイスから削除して再度ペアリングをしてください。
