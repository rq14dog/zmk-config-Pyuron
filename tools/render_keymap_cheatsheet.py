#!/usr/bin/env python3
"""Render a readable Pyuron keymap cheatsheet image.

Source of truth: config/Pyuron.keymap + config/Pyuron.json.
Output: docs/keymap-cheatsheet.jpg (landscape, 2-column layer grid).
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
OUTPUT = ROOT / "docs" / "keymap-cheatsheet.jpg"


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
    "LEFT_SHIFT": "Shift",
    "LCTRL": "Ctrl",
    "LGUI": "Cmd",
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

# Cards are placed on this grid; None renders the legend card.
LAYER_GRID = [
    ["MAC_BASE", "WIN_BASE"],
    ["MAC_OPS", "WIN_OPS"],
    ["NUM_SYS", "SYSTEM"],
    ["MOUSE", None],
]

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
    candidates = [
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
    "hint": load_font(15, bold=True),
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
        font = FONTS["key"] if len(label.primary) <= 6 else FONTS["key_small"]
        upper = (xy[0], xy[1] + 4, xy[2], xy[3] - (24 if label.hint else 4))
        centered_text(draw, upper, label.primary, font, COLORS["text"])
    if label.hint:
        centered_text(draw, (xy[0], xy[3] - 28, xy[2], xy[3] - 6), label.hint, FONTS["hint"], COLORS["muted"])


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
        ("", "Esc hold -> System,  right trackball move -> Mouse (1s)"),
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


def main() -> int:
    with LAYOUT.open(encoding="utf-8") as file:
        positions = json.load(file)["layouts"]["LAYOUT"]["layout"]
    layers = dict(parse_layers(KEYMAP.read_text(encoding="utf-8")))
    if not layers:
        print("No layers found.", file=sys.stderr)
        return 1

    missing = [name for row in LAYER_GRID for name in row if name and name not in layers]
    if missing:
        print(f"Layers missing from keymap: {', '.join(missing)}", file=sys.stderr)
        return 1

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

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=92, optimize=True)
    print(f"Wrote {OUTPUT} ({WIDTH}x{HEIGHT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
