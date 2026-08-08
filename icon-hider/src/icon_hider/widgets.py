"""
widgets.py
----------
Кастомные Tkinter-виджеты: скруглённая кнопка на Canvas без
стандартного «квадратного» вида системных кнопок.
"""

import tkinter as tk
from tkinter import font as tkfont

from . import theme


class RoundButton(tk.Canvas):
    """Скруглённая кнопка с hover-эффектом, нарисованная на Canvas."""

    def __init__(self, master, text, command, width=220, height=56,
                 bg=theme.ACCENT, hover=theme.ACCENT_HOVER, fg=theme.TEXT,
                 radius=18, font=None, **kw):
        super().__init__(master, width=width, height=height, bg=theme.CARD,
                          highlightthickness=0, bd=0, **kw)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover
        self.fg = fg
        self.radius = radius
        self.width = width
        self.height = height
        self.font = font or tkfont.Font(family=theme.FONT_FAMILY, size=12, weight="bold")
        self.text = text

        self._draw(bg)
        self.bind("<Enter>", lambda e: self._draw(self.hover_color))
        self.bind("<Leave>", lambda e: self._draw(self.bg_color))
        self.bind("<Button-1>", lambda e: self._on_click())

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kw)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(2, 2, self.width - 2, self.height - 2, self.radius,
                          fill=color, outline="")
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                          fill=self.fg, font=self.font)

    def set_text(self, text):
        self.text = text
        self._draw(self.bg_color)

    def set_colors(self, bg, hover):
        self.bg_color = bg
        self.hover_color = hover
        self._draw(bg)

    def _on_click(self):
        if self.command:
            self.command()
