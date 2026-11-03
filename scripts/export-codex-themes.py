#!/usr/bin/env python3
"""Export Morelkai to Codex app share strings and CLI TextMate themes."""

import json
import plistlib

from theme_source import ROOT, load_theme, opaque


def app_theme(source, variant):
    c = source["colors"]
    dark = variant == "night"
    # The app only imports registered code theme IDs, not custom token colors.
    return {
        "variant": "dark" if dark else "light",
        "codeThemeId": "monokai" if dark else "one",
        "theme": {
            "accent": c["terminal.ansiBrightMagenta"],
            "accentSource": "custom",
            "contrast": 60 if dark else 45,
            "fonts": {"code": None, "ui": None},
            "ink": c["editor.foreground"],
            "opaqueWindows": True,
            "semanticColors": {
                "diffAdded": c["editorGutter.addedBackground"],
                "diffRemoved": c["editorGutter.deletedBackground"],
                "skill": c["terminal.ansiBrightMagenta"],
            },
            "surface": c["editor.background"],
        },
    }


def cli_theme(source):
    c = source["colors"]
    settings = [{"settings": {
        "background": c["editor.background"],
        "foreground": c["editor.foreground"],
        "caret": c["editorCursor.foreground"],
        "selection": opaque(c["editor.selectionBackground"], c["editor.background"]),
        "lineHighlight": c["editor.lineHighlightBackground"],
        "gutter": c["editorGutter.background"],
        "gutterForeground": c["editorLineNumber.foreground"],
    }}]
    for rule in source["tokenColors"]:
        entry = dict(rule)
        if isinstance(entry.get("scope"), list):
            entry["scope"] = ", ".join(entry["scope"])
        settings.append(entry)
    return {"name": source["name"], "settings": settings}


def main():
    app = ROOT / "codex" / "app"
    cli = ROOT / "codex" / "cli"
    app.mkdir(parents=True, exist_ok=True)
    cli.mkdir(parents=True, exist_ok=True)
    for variant in ("night", "day"):
        source = load_theme(variant)
        payload = json.dumps(app_theme(source, variant), separators=(",", ":"))
        (app / f"morelkai-{variant}.codex-theme").write_text(
            f"codex-theme-v1:{payload}\n")
        (cli / f"morelkai-{variant}.tmTheme").write_bytes(
            plistlib.dumps(cli_theme(source), sort_keys=False))


if __name__ == "__main__":
    main()
