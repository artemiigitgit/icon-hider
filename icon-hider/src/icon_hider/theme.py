"""
theme.py
--------
Единая цветовая палитра приложения, чтобы весь UI был согласован.
"""

BG = "#12141c"
CARD = "#1a1d29"
CARD_ALT = "#2a2d3d"
CARD_ALT_HOVER = "#343747"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#9377ff"
ACCENT_ON = "#2fd889"
ACCENT_ON_HOVER = "#3ee89f"
TEXT = "#f2f2f7"
SUBTEXT = "#8b8fa3"
DANGER = "#ff5c7a"

FONT_FAMILY = "Segoe UI"


def hex_to_rgba(hex_color: str, alpha: int = 255):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return (r, g, b, alpha)
