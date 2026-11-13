#!/usr/bin/env python3
"""Export the VS Code palettes to Herdr, Ghostty and Claude Code (standard library only)."""

import json

from theme_source import ROOT, load_colors, load_theme, opaque

ANSI = (
    "Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White",
    "BrightBlack", "BrightRed", "BrightGreen", "BrightYellow", "BrightBlue",
    "BrightMagenta", "BrightCyan", "BrightWhite",
)


def scope_color(theme, scope):
    """Foreground of the first token rule whose scope list names `scope`."""
    for rule in theme["tokenColors"]:
        scopes = rule.get("scope", [])
        if isinstance(scopes, str):
            scopes = [s.strip() for s in scopes.split(",")]
        if scope in scopes and "foreground" in rule.get("settings", {}):
            return rule["settings"]["foreground"].lower()
    raise KeyError(scope)


def scale_alpha(color, factor):
    """Strengthen or soften an RRGGBBAA color before compositing it."""
    alpha = min(255, round(int(color[7:9], 16) * factor))
    return f"{color[:7]}{alpha:02x}"


def shimmer(color):
    """Lighter variant used by Claude Code's animated spinner gradient."""
    return opaque(color + "99", "#ffffff")


def claude_colors(theme):
    c = theme["colors"]
    bg = c["terminal.background"]
    accent = c["terminal.ansiBrightMagenta"]
    orange = scope_color(theme, "variable.parameter")
    inserted = c["diffEditor.insertedTextBackground"]
    removed = c["diffEditor.removedTextBackground"]
    tokens = {
        "claude": accent,
        "text": c["terminal.foreground"],
        "inverseText": bg,
        "inactive": c["terminal.ansiBrightBlack"],
        "subtle": c["gitDecoration.ignoredResourceForeground"],
        "suggestion": c["terminal.ansiBrightBlue"],
        "permission": c["terminal.ansiBrightCyan"],
        "remember": c["terminal.ansiBrightBlue"],
        "success": c["terminal.ansiBrightGreen"],
        "error": c["terminal.ansiBrightRed"],
        "warning": c["terminal.ansiBrightYellow"],
        "merged": c["terminal.ansiMagenta"],
        "promptBorder": c["editorLineNumber.foreground"],
        "planMode": c["terminal.ansiCyan"],
        "autoAccept": c["terminal.ansiMagenta"],
        "bashBorder": c["terminal.ansiBrightRed"],
        "ide": c["terminal.ansiBlue"],
        "fastMode": orange,
        "diffAdded": opaque(inserted, bg),
        "diffRemoved": opaque(removed, bg),
        "diffAddedDimmed": opaque(scale_alpha(inserted, 0.5), bg),
        "diffRemovedDimmed": opaque(scale_alpha(removed, 0.5), bg),
        "diffAddedWord": opaque(scale_alpha(inserted, 2.5), bg),
        "diffRemovedWord": opaque(scale_alpha(removed, 2.5), bg),
        "userMessageBackground": c["editor.selectionHighlightBackground"],
        "userMessageBackgroundHover": c["list.activeSelectionBackground"],
        "selectionBg": opaque(c["terminal.selectionBackground"], bg),
        "composerSidebarBackground": c["sideBar.background"],
        "rate_limit_fill": accent,
        "rate_limit_empty": c["gitDecoration.ignoredResourceForeground"],
        "briefLabelYou": c["terminal.ansiBrightBlue"],
        "briefLabelClaude": accent,
        "red_FOR_SUBAGENTS_ONLY": c["terminal.ansiBrightRed"],
        "blue_FOR_SUBAGENTS_ONLY": c["terminal.ansiBrightBlue"],
        "green_FOR_SUBAGENTS_ONLY": c["terminal.ansiBrightGreen"],
        "yellow_FOR_SUBAGENTS_ONLY": c["terminal.ansiBrightYellow"],
        "purple_FOR_SUBAGENTS_ONLY": c["terminal.ansiBrightMagenta"],
        "orange_FOR_SUBAGENTS_ONLY": orange,
        "pink_FOR_SUBAGENTS_ONLY": c["terminal.ansiRed"],
        "cyan_FOR_SUBAGENTS_ONLY": c["terminal.ansiBrightCyan"],
    }
    for token in ("claude", "warning", "permission", "promptBorder",
                  "inactive", "fastMode"):
        tokens[token + "Shimmer"] = shimmer(tokens[token])
    return {key: value.lower() for key, value in tokens.items()}


def herdr_colors(c):
    return {
        "accent": c["terminal.ansiBrightMagenta"],
        "panel_bg": c["panel.background"],
        "sidebar_bg": c["sideBar.background"],
        "active_row_bg": c["list.activeSelectionBackground"],
        "selection_bg": c["editor.selectionBackground"],
        "surface0": c["editor.selectionHighlightBackground"],
        "surface1": c["button.hoverBackground"],
        "surface_dim": c["editor.lineHighlightBackground"],
        "overlay0": c["editorLineNumber.foreground"],
        "overlay1": c["breadcrumb.foreground"],
        "text": c["editor.foreground"],
        "subtext0": c["activityBar.inactiveForeground"],
        "mauve": c["terminal.ansiBrightMagenta"],
        "green": c["terminal.ansiBrightGreen"],
        "yellow": c["terminal.ansiBrightYellow"],
        "red": c["terminal.ansiBrightRed"],
        "blue": c["terminal.ansiBrightBlue"],
        "teal": c["terminal.ansiBrightCyan"],
        "peach": c["textPreformat.foreground"],
    }


def main():
    herdr = ROOT / "terminal" / "herdr"
    ghostty = ROOT / "terminal" / "ghostty"
    herdr.mkdir(parents=True, exist_ok=True)
    ghostty.mkdir(parents=True, exist_ok=True)
    modes = {"dark": load_colors("night"), "light": load_colors("day")}
    config = ('# Generated by scripts/export-terminal-themes.py.\n'
              '# Merge this theme section into ~/.config/herdr/config.toml.\n'
              '[theme]\nname = "catppuccin"\nauto_switch = true\n'
              'dark_name = "catppuccin"\nlight_name = "catppuccin-latte"\n')
    # Shared dark colors provide a fallback if appearance detection is unavailable.
    for section, colors in (("theme.custom", modes["dark"]),
                            ("theme.custom.dark", modes["dark"]),
                            ("theme.custom.light", modes["light"])):
        config += f"\n[{section}]\n"
        config += "".join(f'{key} = "{value}"\n'
                          for key, value in herdr_colors(colors).items())
    (herdr / "morelkai.toml").write_text(config)
    for mode, c in modes.items():
        name = "morelkai night" if mode == "dark" else "morelkai day"
        values = {
            "background": c["terminal.background"],
            "foreground": c["terminal.foreground"],
            "cursor-color": c["terminalCursor.foreground"],
            "cursor-text": c["terminalCursor.background"],
            "selection-background": opaque(c["terminal.selectionBackground"], c["terminal.background"]),
            "selection-foreground": c["terminal.foreground"],
        }
        text = "# Generated from the matching VS Code theme.\n"
        text += "".join(f"{key} = {value}\n" for key, value in values.items())
        text += "\n" + "".join(f'palette = {i}={c["terminal.ansi" + color]}\n'
                                for i, color in enumerate(ANSI))
        (ghostty / name).write_text(text)
    claude = ROOT / "terminal" / "claude"
    claude.mkdir(parents=True, exist_ok=True)
    for variant, base in (("night", "dark"), ("day", "light")):
        theme = {"name": f"morelkai {variant}", "base": base,
                 "overrides": claude_colors(load_theme(variant))}
        (claude / f"morelkai-{variant}.json").write_text(
            json.dumps(theme, indent=2) + "\n")


if __name__ == "__main__":
    main()
