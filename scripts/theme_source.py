"""Read the source VS Code themes with the Python standard library."""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def load_theme(variant):
    path = ROOT / "themes" / f"morelkai-{variant}-color-theme.json"
    # Preserve quoted strings while removing JSONC comments and trailing commas.
    source = re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/',
                    lambda m: m[0] if m[0].startswith('"') else "", path.read_text())
    source = re.sub(r',(?=\s*[}\]])', '', source)
    return json.loads(source)


def load_colors(variant):
    return load_theme(variant)["colors"]


def opaque(color, background):
    """Composite a VS Code RRGGBBAA color over an opaque background."""
    if len(color) == 7:
        return color
    alpha = int(color[7:9], 16) / 255
    channels = [round(int(color[i:i + 2], 16) * alpha
                      + int(background[i:i + 2], 16) * (1 - alpha))
                for i in (1, 3, 5)]
    return "#" + "".join(f"{channel:02x}" for channel in channels)
