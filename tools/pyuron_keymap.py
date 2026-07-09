#!/usr/bin/env python3
"""Small helper for checking and editing Pyuron ZMK keymaps."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KEYMAP = ROOT / "config" / "Pyuron.keymap"
DEFAULT_LAYOUT = ROOT / "config" / "Pyuron.json"


@dataclass
class Layer:
    name: str
    bindings: list[str]
    bindings_start: int
    bindings_end: int


def tokenize_bindings(text: str) -> list[str]:
    return [match.group(0).strip() for match in re.finditer(r"&[^\s]+(?:\s+(?!&)[^\s]+)*", text)]


def parse_layers(text: str) -> list[Layer]:
    layers: list[Layer] = []
    pattern = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*$")
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        match = pattern.match(lines[index])
        if not match:
            index += 1
            continue

        name = match.group(1)
        cursor = index + 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        if cursor >= len(lines) or "bindings = <" not in lines[cursor]:
            index += 1
            continue

        start = cursor + 1
        end = start
        while end < len(lines) and ">;" not in lines[end]:
            end += 1
        if end >= len(lines):
            raise ValueError(f"{name}: bindings block is not closed with `>;`")

        bindings = tokenize_bindings("\n".join(lines[start:end]))
        layers.append(Layer(name=name, bindings=bindings, bindings_start=start, bindings_end=end))
        index = end + 1

    return layers


def load_layout_key_count(path: Path) -> int:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    try:
        return len(data["layouts"]["LAYOUT"]["layout"])
    except KeyError as exc:
        raise ValueError(f"{path}: layouts.LAYOUT.layout is missing") from exc


def format_bindings(bindings: list[str], columns: int = 10) -> list[str]:
    rows = [bindings[index : index + columns] for index in range(0, len(bindings), columns)]
    width = max((len(binding) for binding in bindings), default=0)
    return ["".join(binding.ljust(width + 2) for binding in row).rstrip() for row in rows]


def check_keymap(keymap_path: Path, layout_path: Path) -> int:
    text = keymap_path.read_text(encoding="utf-8")
    layers = parse_layers(text)
    expected_keys = load_layout_key_count(layout_path)
    problems: list[str] = []

    if not layers:
        problems.append("No keymap layers were found.")

    for index, layer in enumerate(layers):
        if len(layer.bindings) != expected_keys:
            problems.append(
                f"{layer.name}: expected {expected_keys} bindings, found {len(layer.bindings)}."
            )

        for position, binding in enumerate(layer.bindings):
            if binding.count("(") != binding.count(")"):
                problems.append(f"{layer.name}[{position}]: unbalanced parentheses in `{binding}`.")

    defines = dict(re.findall(r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(\d+)\s*$", text, re.MULTILINE))
    for name, value in defines.items():
        layer_index = int(value)
        if name in {layer.name for layer in layers}:
            actual_index = [layer.name for layer in layers].index(name)
            if layer_index != actual_index:
                problems.append(f"#define {name} is {layer_index}, but layer `{name}` is index {actual_index}.")
        elif layer_index >= len(layers):
            problems.append(f"#define {name} points to missing layer index {layer_index}.")

    combo_positions = re.findall(r"key-positions\s*=\s*<([^>]*)>", text)
    for combo_index, raw_positions in enumerate(combo_positions, start=1):
        for raw in raw_positions.split():
            if raw.isdigit() and int(raw) >= expected_keys:
                problems.append(f"combo #{combo_index}: key position {raw} is outside 0-{expected_keys - 1}.")

    if problems:
        print("Problems found:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"OK: {len(layers)} layers, {expected_keys} keys per layer.")
    for index, layer in enumerate(layers):
        print(f"{index}: {layer.name}")
    return 0


def print_layers(keymap_path: Path) -> int:
    layers = parse_layers(keymap_path.read_text(encoding="utf-8"))
    for index, layer in enumerate(layers):
        print(f"{index}: {layer.name} ({len(layer.bindings)} keys)")
    return 0


def set_binding(keymap_path: Path, layer_name: str, row: int, column: int, binding: str, in_place: bool) -> int:
    text = keymap_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    layers = parse_layers(text)
    layer = next((item for item in layers if item.name == layer_name), None)
    if layer is None:
        print(f"Layer `{layer_name}` was not found.", file=sys.stderr)
        return 1

    if row < 0 or column < 0 or column >= 10:
        print("Row and column must be zero-based; column must be 0-9.", file=sys.stderr)
        return 1

    position = row * 10 + column
    if position >= len(layer.bindings):
        print(f"{layer_name}: position row={row}, col={column} is outside this layer.", file=sys.stderr)
        return 1

    layer.bindings[position] = binding.strip()
    replacement = format_bindings(layer.bindings)
    updated_lines = lines[: layer.bindings_start] + replacement + lines[layer.bindings_end :]
    updated = "\n".join(updated_lines) + "\n"

    if in_place:
        keymap_path.write_text(updated, encoding="utf-8")
        print(f"Updated {keymap_path}: {layer_name}[{row},{column}] = {binding.strip()}")
    else:
        print(updated)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check and lightly edit the Pyuron ZMK keymap.")
    parser.add_argument("--keymap", type=Path, default=DEFAULT_KEYMAP, help="Path to Pyuron.keymap")
    parser.add_argument("--layout", type=Path, default=DEFAULT_LAYOUT, help="Path to Pyuron.json")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("check", help="Validate layer sizes, references, and simple syntax.")
    subparsers.add_parser("layers", help="List keymap layers.")

    set_parser = subparsers.add_parser("set", help="Set one binding by layer, row, and column.")
    set_parser.add_argument("layer", help="Layer name, for example MAC_BASE")
    set_parser.add_argument("row", type=int, help="Zero-based row number")
    set_parser.add_argument("column", type=int, help="Zero-based column number")
    set_parser.add_argument("binding", help='Binding text, for example "&kp A"')
    set_parser.add_argument("--in-place", action="store_true", help="Write the change back to the keymap file.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command in {None, "check"}:
            return check_keymap(args.keymap, args.layout)
        if args.command == "layers":
            return print_layers(args.keymap)
        if args.command == "set":
            return set_binding(args.keymap, args.layer, args.row, args.column, args.binding, args.in_place)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
