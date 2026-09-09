#!/usr/bin/env python3
"""Render the Pyuron keymap cheatsheet (JPG + HTML + Markdown).

Source of truth: config/Pyuron.keymap + config/Pyuron.json.
All three outputs are built from the same parsed layer data so they
cannot drift from each other or from the keymap.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
KEYMAP = ROOT / "config" / "Pyuron.keymap"
LAYOUT = ROOT / "config" / "Pyuron.json"
HTML_TEMPLATE = ROOT / "tools" / "templates" / "keymap-cheatsheet.template.html"
OUTPUT_JPG = ROOT / "docs" / "keymap-cheatsheet.jpg"
OUTPUT_MD = ROOT / "docs" / "keymap-cheatsheet.md"
OUTPUT_HTML = ROOT / "docs" / "keymap-cheatsheet.html"


@dataclass
class Label:
    primary: str
    hint: str = ""
    kind: str = ""


COLORS = {
    "bg": "#f6f7f9",
    "card": "#ffffff",
    "line": "#d7dde7",
    "text": "#1d2430",
    "muted": "#6b7280",
    "key": "#fbfcfe",
    "letter": "#e9f7f2",
    "mod": "#edf2ff",
    "layer": "#fff4d8",
    "system": "#ffe8e5",
    "mouse": "#f1e8ff",
    "transparent": "#eef1f5",
    "token": "#ffffff",
}

KEY_NAMES = {
    "AT_SIGN": "@",
    "ASTERISK": "*",
    "BACKSPACE": "Bspc",
    "BSPC": "Bspc",
    "COMMA": ",",
    "DELETE": "Del",
    "DOT": ".",
    "DOWN": "Down",
    "DOWN_ARROW": "Down",
    "END": "End",
    "ENTER": "Enter",
    "EQUAL": "=",
    "ESC": "Esc",
    "ESCAPE": "Esc",
    "FSLH": "/",
    "HOME": "Home",
    "INSERT": "Ins",
    "LANG1": "Kana",
    "LANG2": "Eisu",
    "LBKT": "[",
    "LEFT": "Left",
    "LEFT_ARROW": "Left",
    "LEFT_BRACKET": "[",
    "LEFT_ALT": "Alt",
    "LEFT_SHIFT": "Shift",
    "LCTRL": "Ctrl",
    "LGUI": "Cmd",
    "RCTRL": "Right Ctrl",
    "MINUS": "-",
    "N0": "0",
    "N1": "1",
    "N2": "2",
    "N3": "3",
    "N4": "4",
    "N5": "5",
    "N6": "6",
    "N7": "7",
    "N8": "8",
    "N9": "9",
    "PAGE_DOWN": "PgDn",
    "PAGE_UP": "PgUp",
    "PLUS": "+",
    "PRINTSCREEN": "PrtSc",
    "RBKT": "]",
    "RIGHT": "Right",
    "RIGHT_ARROW": "Right",
    "RIGHT_BRACKET": "]",
    "RIGHT_SHIFT": "RShift",
    "SLASH": "/",
    "SPACE": "Space",
    "TAB": "Tab",
    "TILDE": "~",
    "UP": "Up",
    "UP_ARROW": "Up",
}

MOUSE_BUTTONS = {
    "MB1": "LClick",
    "MB2": "RClick",
}

# Function-name labels for OPS-layer shortcuts, keyed by [layer_name][key-code
# string] (the key-code string is what label_kp() would otherwise display,
# e.g. "Cmd+Shift+4"). Layer-scoped because the same key code can mean
# different things on different layers (e.g. F2 is unmapped on MAC_OPS but
# "名前変更" on WIN_OPS). Only shortcuts explicitly reviewed and confirmed
# get an entry; anything missing falls back to showing the raw key code.
SHORTCUT_LABELS: dict[str, dict[str, str]] = {
    "MAC_OPS": {
        "Ctrl+Cmd+Space": "絵文字/記号",
        "Cmd+Shift+Tab": "前のアプリ",
        "Cmd+Tab": "アプリ切替",
        "Ctrl+Up": "Mission Control",
        "Cmd+[": "戻る",
        "Cmd+]": "進む",
        "Ctrl+Cmd+F": "フルスクリーン",
        "Cmd+Ctrl+Q": "画面ロック",
        "Cmd+Shift+3": "全画面スクショ",
        "Cmd+Shift+4": "範囲スクショ",
        "Alt+Cmd+Esc": "強制終了",
        "Cmd+M": "最小化",
        "Cmd+Q": "終了",
        "Ctrl+Left": "デスクトップ移動",
        "Ctrl+Right": "デスクトップ移動",
        "Shift+Cmd+T": "閉じたタブを復元",
        "Cmd+Left": "行頭",
        "Ctrl+Down": "App Exposé",
        "Cmd+Right": "行末",
    },
    "WIN_OPS": {
        "Alt+Tab": "アプリ切替",
        "Win+Tab": "タスクビュー",
        "Alt+Left": "戻る",
        "Alt+Right": "進む",
        "Win+Up": "最大化",
        "Win+L": "画面ロック",
        "Win+Shift+S": "範囲スクショ",
        "Ctrl+Shift+Esc": "タスクマネージャ",
        "Win+Down": "最小化",
        "Alt+F4": "終了",
        "Ctrl+Win+Left": "デスクトップ移動",
        "Ctrl+Win+Right": "デスクトップ移動",
        "Ctrl+Home": "先頭",
        "Ctrl+End": "末尾",
        "PrtSc": "スクショ",
        "Win+.": "絵文字/記号",
        "Shift+Alt+Tab": "前のアプリ",
        "Win+D": "デスクトップ表示",
        "Ctrl+Shift+T": "閉じたタブを復元",
        "F2": "名前変更",
    },
}

LAYER_NAMES = {
    "0": "Mac",
    "1": "Mac Ops",
    "2": "Win",
    "3": "Win Ops",
    "4": "Num",
    "5": "Sys",
    "6": "Mouse",
}

LAYER_NOTES = {
    "MAC_BASE": "default",
    "MAC_OPS": "Enter hold",
    "WIN_BASE": "default",
    "WIN_OPS": "Enter hold",
    "NUM_SYS": "Space hold",
    "SYSTEM": "Esc hold",
    "MOUSE": "right trackball move (auto, 1s)",
}

LAYER_GROUP = {
    "MAC_BASE": "mac",
    "MAC_OPS": "mac",
    "WIN_BASE": "win",
    "WIN_OPS": "win",
    "NUM_SYS": "utility",
    "SYSTEM": "utility",
    "MOUSE": "utility",
}

LAYER_DESCRIPTIONS = {
    "MAC_BASE": "Mac用の通常入力",
    "MAC_OPS": "Mac用操作レイヤー。`MAC_BASE` の `Enter` 長押し",
    "WIN_BASE": "Windows用の通常入力",
    "WIN_OPS": "Windows用操作レイヤー。`WIN_BASE` の `Enter` 長押し",
    "NUM_SYS": "数字・記号・カーソル。Baseの `Space` 長押し",
    "SYSTEM": "Bluetooth・OS切替・Bootloader。Baseの `Esc` 長押し",
    "MOUSE": "マウスクリック用。右トラックボールを動かすと1秒間自動で有効",
}

# Cards are placed on this grid; None renders the legend card.
LAYER_GRID = [
    ["MAC_BASE", "WIN_BASE"],
    ["MAC_OPS", "WIN_OPS"],
    ["NUM_SYS", "SYSTEM"],
    ["MOUSE", None],
]

# Sequential order used by the Markdown/HTML documents (linear reading, unlike the JPG's 2-column grid).
DOC_LAYER_ORDER = ["MAC_BASE", "MAC_OPS", "WIN_BASE", "WIN_OPS", "NUM_SYS", "SYSTEM", "MOUSE"]

MARGIN = 50
COLUMN_GAP = 40
ROW_GAP = 28
KEY_W = 96
KEY_H = 76
KEY_GAP = 10
HEAD_H = 64
BOARD_PAD_X = 28
BOARD_PAD_TOP = 26
BOARD_PAD_BOTTOM = 28
BOARD_W = 13 * KEY_W + 12 * KEY_GAP
BOARD_H = 4 * KEY_H + 3 * KEY_GAP
CARD_W = BOARD_W + 2 * BOARD_PAD_X
CARD_H = HEAD_H + BOARD_PAD_TOP + BOARD_H + BOARD_PAD_BOTTOM
TITLE_H = 108
WIDTH = 2 * MARGIN + 2 * CARD_W + COLUMN_GAP
HEIGHT = TITLE_H + len(LAYER_GRID) * CARD_H + (len(LAYER_GRID) - 1) * ROW_GAP + 36


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # Hiragino comes first: it covers both Japanese function-name labels
    # (e.g. "範囲スクショ") and Latin key names in one consistent family.
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc" if bold else "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSMono.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


FONTS = {
    "title": load_font(48, bold=True),
    "subtitle": load_font(20),
    "layer": load_font(30, bold=True),
    "note": load_font(20),
    "key": load_font(22, bold=True),
    "key_small": load_font(16, bold=True),
    "key_tiny": load_font(13, bold=True),
    "hint": load_font(15, bold=True),
    "hint_small": load_font(12, bold=True),
    "hint_tiny": load_font(10, bold=True),
    "token": load_font(14, bold=True),
}


def tokenize_bindings(text: str) -> list[str]:
    return [match.group(0).strip() for match in re.finditer(r"&[^\s]+(?:\s+(?!&)[^\s]+)*", text)]


def parse_layers(text: str) -> list[tuple[str, list[str]]]:
    layers: list[tuple[str, list[str]]] = []
    pattern = re.compile(
        r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*\n\s*bindings\s*=\s*<\n([\s\S]*?)^\s*>;",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        layers.append((match.group(1), tokenize_bindings(match.group(2))))
    return layers


def parse_combos(text: str) -> list[tuple[list[int], str, list[str]]]:
    combos: list[tuple[list[int], str, list[str]]] = []
    layer_names = [name for name, _ in parse_layers(text)]
    for block in re.finditer(r"combo_\w+\s*\{([^}]*)\}", text, re.DOTALL):
        body = block.group(1)
        position_match = re.search(r"key-positions\s*=\s*<([^>]*)>", body)
        binding_match = re.search(r"bindings\s*=\s*<([^>]*)>", body)
        if not position_match or not binding_match:
            continue
        combo_positions = [int(value) for value in position_match.group(1).split()]
        scope_match = re.search(r"layers\s*=\s*<([^>]*)>", body)
        scope = [layer_names[int(value)] for value in scope_match.group(1).split()] if scope_match else []
        combos.append((combo_positions, binding_match.group(1).strip(), scope))
    return combos


def display_primary(label: "Label") -> str:
    return "trns" if label.kind == "transparent" else label.primary


def combo_description(combo_positions: list[int], target_binding: str, base_labels: list["Label"], scope: list[str]) -> str:
    key_names = [display_primary(base_labels[position]) for position in combo_positions]
    target = label_for(target_binding, scope[0] if scope else "MAC_BASE")
    suffix = f" ({', '.join(scope)})" if scope else " (all layers)"
    return f"{' + '.join(key_names)} -> {display_primary(target)}{suffix}"


def key_name(raw: str, layer_name: str) -> str:
    if raw == "LC":
        return "Ctrl"
    if raw in {"LG", "LGUI"}:
        return "Cmd" if layer_name.startswith("MAC") else "Win"
    if raw == "LS":
        return "Shift"
    if raw == "LA":
        return "Alt"
    return KEY_NAMES.get(raw, raw.removeprefix("NUMBER_"))


def split_wrappers(expr: str) -> tuple[list[str], str]:
    wrappers: list[str] = []
    while match := re.match(r"^([A-Z]+)\((.*)\)$", expr):
        wrappers.append(match.group(1))
        expr = match.group(2)
    return wrappers, expr


def label_kp(raw_key: str, layer_name: str) -> str:
    wrappers, inner = split_wrappers(raw_key)
    mods = [key_name(wrapper, layer_name) for wrapper in wrappers]
    key = key_name(inner, layer_name)
    return "+".join(mods + [key]) if mods else key


def is_shortcut(primary: str) -> bool:
    return "+" in primary and len(primary) > 1


def label_for(binding: str, layer_name: str) -> Label:
    parts = binding.split()
    if not parts:
        return Label("")
    behavior = parts[0]

    if behavior == "&trans":
        return Label("", kind="transparent")
    if behavior == "&bootloader":
        return Label("Boot", kind="system")
    if behavior == "&mac_mode":
        return Label("Mac", hint="mode", kind="layer")
    if behavior == "&win_mode":
        return Label("Win", hint="mode", kind="layer")
    if behavior == "&mkp" and len(parts) > 1:
        return Label(MOUSE_BUTTONS.get(parts[1], parts[1]), kind="mouse")
    if behavior == "&bt":
        if len(parts) > 2 and parts[1] == "BT_SEL":
            return Label(f"BT {parts[2]}", kind="system")
        if len(parts) > 1 and parts[1] == "BT_CLR_ALL":
            return Label("BT All", kind="system")
        if len(parts) > 1 and parts[1] == "BT_CLR":
            return Label("BT Clr", kind="system")
    if behavior == "&to" and len(parts) > 1:
        return Label(f"To {LAYER_NAMES.get(parts[1], f'L{parts[1]}')}", kind="layer")
    if behavior == "&lt" and len(parts) > 2:
        return Label(key_name(parts[2], layer_name), hint=f"hold {LAYER_NAMES.get(parts[1], f'L{parts[1]}')}", kind="layer")
    if behavior == "&mt" and len(parts) > 2:
        return Label(key_name(parts[2], layer_name), hint=f"hold {key_name(parts[1], layer_name)}", kind="layer")
    if behavior == "&kp" and len(parts) > 1:
        primary = label_kp(parts[1], layer_name)
        function_name = SHORTCUT_LABELS.get(layer_name, {}).get(primary)
        if function_name:
            return Label(function_name, hint=primary, kind="mod")
        if is_shortcut(primary):
            return Label(primary, kind="mod")
        if re.fullmatch(r"[A-Z]", primary):
            return Label(primary, kind="letter")
        if primary in {"Ctrl", "Cmd", "Win", "Shift", "Alt", "RShift"}:
            return Label(primary, kind="mod")
        return Label(primary)

    return Label(binding.removeprefix("&"), kind="system")


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def rounded(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str = COLORS["line"], radius: int = 12, width: int = 2) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def centered_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str, font: ImageFont.ImageFont, fill: str) -> None:
    w, h = text_size(draw, text, font)
    x1, y1, x2, y2 = xy
    draw.text((x1 + (x2 - x1 - w) / 2, y1 + (y2 - y1 - h) / 2 - 1), text, font=font, fill=fill)


CJK_PATTERN = re.compile(r"[぀-ヿ㐀-鿿＀-￯]")


def text_units(text: str) -> list[str]:
    """Split text into wrap units: one per CJK character, whole runs for Latin words."""
    units: list[str] = []
    buf = ""
    for ch in text:
        if CJK_PATTERN.match(ch):
            if buf:
                units.append(buf)
                buf = ""
            units.append(ch)
        elif ch == " ":
            if buf:
                units.append(buf)
                buf = ""
        else:
            buf += ch
    if buf:
        units.append(buf)
    return units


def _joins_without_space(left: str, right: str) -> bool:
    return not (left[-1:].isascii() and left[-1:].isalnum() and right[:1].isascii() and right[:1].isalnum())


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    units = text_units(text)
    if not units:
        return []
    lines: list[str] = []
    current = ""
    for unit in units:
        if not current:
            candidate = unit
        else:
            sep = "" if _joins_without_space(current, unit) else " "
            candidate = current + sep + unit
        width, _ = text_size(draw, candidate, font)
        if width <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = unit
    if current:
        lines.append(current)
    return lines


def fit_primary_lines(
    draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int
) -> tuple[list[str], ImageFont.ImageFont, int]:
    """Pick the largest font (key -> key_small -> key_tiny) that lets `text`
    fit within max_width, wrapping to at most 2 lines if a single line
    doesn't fit."""
    font_names = ["key", "key_small", "key_tiny"]
    for font_name in font_names:
        font = FONTS[font_name]
        line_h = text_size(draw, "Agあ", font)[1] + 2
        width, _ = text_size(draw, text, font)
        if width <= max_width:
            return [text], font, line_h
        lines = wrap_text(draw, text, font, max_width)
        fits_width = all(text_size(draw, line, font)[0] <= max_width for line in lines)
        if len(lines) <= 2 and fits_width and line_h * len(lines) <= max_height:
            return lines, font, line_h

    font = FONTS["key_tiny"]
    line_h = text_size(draw, "Agあ", font)[1] + 2
    return wrap_text(draw, text, font, max_width), font, line_h


def fit_hint_font(draw: ImageDraw.ImageDraw, text: str, max_width: int) -> ImageFont.ImageFont:
    """Shrink the hint font (e.g. a raw key code like 'Ctrl+Cmd+Space') until
    it fits max_width, so it doesn't bleed into neighboring keys."""
    for font_name in ("hint", "hint_small", "hint_tiny"):
        font = FONTS[font_name]
        width, _ = text_size(draw, text, font)
        if width <= max_width:
            return font
    return FONTS["hint_tiny"]


def draw_multiline_centered(
    draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], lines: list[str], font: ImageFont.ImageFont, line_h: int, fill: str
) -> None:
    total_h = line_h * len(lines)
    y = xy[1] + (xy[3] - xy[1] - total_h) / 2
    for line in lines:
        w, _ = text_size(draw, line, font)
        x = xy[0] + (xy[2] - xy[0] - w) / 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h


def draw_combo(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], label: str) -> None:
    tokens = label.split("+")
    rows: list[list[str]] = [[]]
    row_width = 0
    max_width = xy[2] - xy[0] - 14
    for token in tokens:
        tw, _ = text_size(draw, token, FONTS["token"])
        token_width = tw + 14
        next_width = row_width + (5 if rows[-1] else 0) + token_width
        if rows[-1] and next_width > max_width:
            rows.append([token])
            row_width = token_width
        else:
            rows[-1].append(token)
            row_width = next_width

    token_h = 22
    total_h = len(rows) * token_h + (len(rows) - 1) * 4
    y = xy[1] + (xy[3] - xy[1] - total_h) / 2
    for row in rows:
        widths = [text_size(draw, token, FONTS["token"])[0] + 14 for token in row]
        x = xy[0] + (xy[2] - xy[0] - sum(widths) - 5 * (len(row) - 1)) / 2
        for token, width in zip(row, widths):
            rounded(draw, (int(x), int(y), int(x + width), int(y + token_h)), COLORS["token"], "#aeb7c4", radius=5)
            centered_text(draw, (int(x), int(y), int(x + width), int(y + token_h)), token, FONTS["token"], COLORS["text"])
            x += width + 5
        y += token_h + 4


def draw_key(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], label: Label) -> None:
    if label.kind == "transparent":
        rounded(draw, xy, COLORS["transparent"], outline="#e4e8ef", width=1)
        return
    fill = COLORS.get(label.kind, COLORS["key"])
    rounded(draw, xy, fill)
    if is_shortcut(label.primary):
        draw_combo(draw, xy, label.primary)
    else:
        pad = 3
        hint_h = 24 if label.hint else 0
        primary_box = (xy[0] + pad, xy[1] + pad, xy[2] - pad, xy[3] - hint_h - pad)
        max_w = primary_box[2] - primary_box[0]
        max_h = primary_box[3] - primary_box[1]
        lines, font, line_h = fit_primary_lines(draw, label.primary, max_w, max_h)
        draw_multiline_centered(draw, primary_box, lines, font, line_h, COLORS["text"])
    if label.hint:
        hint_box = (xy[0] + 3, xy[3] - 27, xy[2] - 3, xy[3] - 5)
        hint_font = fit_hint_font(draw, label.hint, hint_box[2] - hint_box[0])
        centered_text(draw, hint_box, label.hint, hint_font, COLORS["muted"])


def draw_card_frame(draw: ImageDraw.ImageDraw, x: int, y: int, name: str, note: str) -> None:
    rounded(draw, (x, y, x + CARD_W, y + CARD_H), COLORS["card"], radius=14)
    draw.line((x, y + HEAD_H, x + CARD_W, y + HEAD_H), fill=COLORS["line"], width=2)
    draw.text((x + 26, y + 18), name, font=FONTS["layer"], fill=COLORS["text"])
    name_w, _ = text_size(draw, name, FONTS["layer"])
    draw.text((x + 38 + name_w, y + 25), note, font=FONTS["note"], fill=COLORS["muted"])


def draw_layer(draw: ImageDraw.ImageDraw, x: int, y: int, name: str, labels: list[Label], positions: list[dict[str, int]]) -> None:
    draw_card_frame(draw, x, y, name, LAYER_NOTES.get(name, ""))
    board_x = x + BOARD_PAD_X
    board_y = y + HEAD_H + BOARD_PAD_TOP
    for label, position in zip(labels, positions):
        key_x = board_x + position["x"] * (KEY_W + KEY_GAP)
        key_y = board_y + position["y"] * (KEY_H + KEY_GAP)
        draw_key(draw, (key_x, key_y, key_x + KEY_W, key_y + KEY_H), label)


def draw_legend(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw_card_frame(draw, x, y, "Legend", "how to read")

    swatches = [
        ("letter", "Letter / number"),
        ("mod", "Modifier / shortcut"),
        ("layer", "Layer move / tap-hold"),
        ("system", "System / Bluetooth"),
        ("mouse", "Mouse click"),
        ("transparent", "Transparent: base layer key works"),
    ]
    sx = x + BOARD_PAD_X
    sy = y + HEAD_H + BOARD_PAD_TOP + 4
    for kind, text in swatches:
        rounded(draw, (sx, sy, sx + 46, sy + 30), COLORS[kind], radius=8)
        draw.text((sx + 60, sy + 3), text, font=FONTS["note"], fill=COLORS["text"])
        sy += 44

    lines = [
        ("Tap / hold:", "big label = tap, small label = hold"),
        ("Layer access:", "Space hold -> Num,  Enter hold -> Mac/Win Ops"),
        ("", "Esc hold -> System"),
        ("Trackballs:", "left = vertical scroll only,  right = cursor + Mouse (1s)"),
        ("Combo:", "P + Esc together -> back to Mac Base"),
        ("OS switch:", "Mac mode = BT 0 + Mac,  Win mode = BT 1 + Win (SYSTEM layer)"),
    ]
    tx = x + 560
    ty = y + HEAD_H + BOARD_PAD_TOP + 8
    for head, body in lines:
        if head:
            draw.text((tx, ty), head, font=FONTS["note"], fill=COLORS["muted"])
        draw.text((tx + 150, ty), body, font=FONTS["note"], fill=COLORS["text"])
        ty += 40


def render_jpg(layers: dict[str, list[str]], positions: list[dict[str, int]]) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw.text((MARGIN, 34), "Pyuron Keymap", font=FONTS["title"], fill=COLORS["text"])
    subtitle = "generated from config/Pyuron.keymap by tools/render_keymap_cheatsheet.py"
    draw.text((MARGIN + 6, 90 - 4), subtitle, font=FONTS["subtitle"], fill=COLORS["muted"])

    for row_index, row in enumerate(LAYER_GRID):
        y = TITLE_H + row_index * (CARD_H + ROW_GAP)
        for column_index, name in enumerate(row):
            x = MARGIN + column_index * (CARD_W + COLUMN_GAP)
            if name is None:
                draw_legend(draw, x, y)
            else:
                labels = [label_for(binding, name) for binding in layers[name]]
                draw_layer(draw, x, y, name, labels, positions)

    OUTPUT_JPG.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_JPG, quality=92, optimize=True)
    print(f"Wrote {OUTPUT_JPG} ({WIDTH}x{HEIGHT})")


def markdown_cell(label: Label) -> str:
    primary = display_primary(label)
    if not primary:
        return ""
    if label.hint:
        return f"{primary} / {label.hint}"
    return primary


def render_markdown_layer(name: str, labels: list[Label], positions: list[dict[str, int]], max_x: int, max_y: int) -> str:
    grid = {(position["x"], position["y"]): label for label, position in zip(labels, positions)}
    header = "| " + " | ".join(f"x{i}" for i in range(max_x + 1)) + " |"
    separator = "| " + " | ".join("---" for _ in range(max_x + 1)) + " |"
    rows = []
    for y in range(max_y + 1):
        cells = [markdown_cell(grid[(x, y)]) if (x, y) in grid else "" for x in range(max_x + 1)]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([f"## {name}", "", header, separator, *rows])


def render_markdown(layers: dict[str, list[str]], positions: list[dict[str, int]], combos: list[tuple[list[int], str, list[str]]]) -> str:
    max_x = max(position["x"] for position in positions)
    max_y = max(position["y"] for position in positions)
    base_labels = [label_for(binding, "MAC_BASE") for binding in layers["MAC_BASE"]]
    combo_lines = "\n".join(
        f"- コンボ: `{combo_description(combo_positions, target, base_labels, scope)}`" for combo_positions, target, scope in combos
    )

    overview_rows = "\n".join(
        f"| {index} | `{name}` | {LAYER_DESCRIPTIONS.get(name, '')} |" for index, name in enumerate(DOC_LAYER_ORDER)
    )

    layer_sections = "\n\n".join(
        render_markdown_layer(name, [label_for(binding, name) for binding in layers[name]], positions, max_x, max_y)
        for name in DOC_LAYER_ORDER
    )

    return f"""# Pyuron キーマップ早見表

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
{overview_rows}

## 読み方

- `primary / hold Xxx` は短く押すと primary、長押しすると Xxx です。
- `trns` は下のレイヤーを透過します。
- 空欄は物理的なキーがない位置です。
- `Mac / mode` は Bluetooth 0 を選んで `MAC_BASE` へ移動します。
- `Win / mode` は Bluetooth 1 を選んで `WIN_BASE` へ移動します。
- 左トラックボールは縦スクロール専用です。横スクロールは出力しません。
- 右トラックボールはカーソル移動用で、動かすと `MOUSE` が1秒間有効になります。
{combo_lines}

{layer_sections}
"""


def render_html(layers: dict[str, list[str]], positions: list[dict[str, int]], combos: list[tuple[list[int], str, list[str]]]) -> str:
    base_labels = [label_for(binding, "MAC_BASE") for binding in layers["MAC_BASE"]]
    combo_pill = ", ".join(combo_description(combo_positions, target, base_labels, scope) for combo_positions, target, scope in combos)

    layers_json = [
        {
            "name": name,
            "group": LAYER_GROUP.get(name, "utility"),
            "note": LAYER_NOTES.get(name, ""),
            "keys": [
                [display_primary(label_for(binding, name)), label_for(binding, name).hint, label_for(binding, name).kind]
                for binding in layers[name]
            ],
        }
        for name in DOC_LAYER_ORDER
    ]

    template = HTML_TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("__POSITIONS_JSON__", json.dumps(positions))
    html = html.replace("__LAYERS_JSON__", json.dumps(layers_json, ensure_ascii=False))
    html = html.replace("__KEY_COUNT__", str(len(positions)))
    html = html.replace("__LAYER_COUNT__", str(len(DOC_LAYER_ORDER)))
    html = html.replace("__COMBO_PILL__", combo_pill)
    return html


def main() -> int:
    with LAYOUT.open(encoding="utf-8") as file:
        positions = json.load(file)["layouts"]["LAYOUT"]["layout"]
    layers = dict(parse_layers(KEYMAP.read_text(encoding="utf-8")))
    if not layers:
        print("No layers found.", file=sys.stderr)
        return 1

    required = set(DOC_LAYER_ORDER) | {name for row in LAYER_GRID for name in row if name}
    missing = [name for name in required if name not in layers]
    if missing:
        print(f"Layers missing from keymap: {', '.join(missing)}", file=sys.stderr)
        return 1

    combos = parse_combos(KEYMAP.read_text(encoding="utf-8"))

    render_jpg(layers, positions)

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(render_markdown(layers, positions, combos), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD}")

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(render_html(layers, positions, combos), encoding="utf-8")
    print(f"Wrote {OUTPUT_HTML}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
