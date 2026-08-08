"""
tray.py
-------
Значок в системном трее: сворачивание приложения в фон,
контекстное меню (Открыть / Переключить / Выход).
"""

import threading

import pystray
from PIL import Image, ImageDraw

from . import theme


def make_tray_image(visible: bool) -> Image.Image:
    """Рисует квадратную иконку для трея, цвет зависит от состояния."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    color = theme.hex_to_rgba(theme.ACCENT_ON if visible else theme.DANGER)
    draw.rounded_rectangle([6, 14, 58, 50], radius=10, fill=theme.hex_to_rgba(theme.CARD))
    if visible:
        draw.ellipse([22, 24, 42, 44], fill=color)
    else:
        draw.ellipse([26, 28, 38, 40], fill=color)
    return img


class TrayController:
    """Обёртка над pystray.Icon с удобными callback-ами."""

    def __init__(self, on_open, on_toggle, on_quit, get_visible):
        self.on_open = on_open
        self.on_toggle = on_toggle
        self.on_quit = on_quit
        self.get_visible = get_visible
        self.icon = None

    def show(self):
        if self.icon is not None:
            return
        image = make_tray_image(self.get_visible())
        menu = pystray.Menu(
            pystray.MenuItem("Открыть", lambda: self.on_open(), default=True),
            pystray.MenuItem("Скрыть/показать иконки", lambda: self.on_toggle()),
            pystray.MenuItem("Выход", lambda: self.on_quit()),
        )
        self.icon = pystray.Icon("icon_hider", image, "Icon Hider", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def refresh(self, visible: bool):
        if self.icon is not None:
            self.icon.icon = make_tray_image(visible)

    def stop(self):
        if self.icon is not None:
            self.icon.stop()
            self.icon = None
