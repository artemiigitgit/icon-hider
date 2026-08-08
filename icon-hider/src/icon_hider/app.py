"""
app.py
------
Главное окно приложения Icon Hider: собирает UI, связывает его
с desktop.py (управление иконками), tray.py (фон / трей) и
hotkey.py (глобальная горячая клавиша).
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont

from . import desktop, theme
from .tray import TrayController
from .hotkey import GlobalHotkey
from .widgets import RoundButton


class IconHiderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Icon Hider")
        self.root.geometry("360x420")
        self.root.configure(bg=theme.BG)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self._set_window_icon()

        self.visible = desktop.icons_are_visible()

        self.tray = TrayController(
            on_open=self._show_window,
            on_toggle=self.toggle_icons,
            on_quit=self.quit_app,
            get_visible=lambda: self.visible,
        )

        self._build_ui()
        self._update_status()

        self.hotkey = GlobalHotkey(callback=lambda: self.root.after(0, self.toggle_icons))
        self.hotkey.start()

    def _set_window_icon(self):
        """Устанавливает иконку окна из assets/icon.ico."""
        if getattr(sys, "frozen", False):
            # PyInstaller кладёт package-data в _MEIPASS/icon_hider/...
            base_dir = Path(sys._MEIPASS) / "icon_hider"
        else:
            base_dir = Path(__file__).resolve().parent

        icon_path = base_dir / "assets" / "icon.ico"
        if icon_path.exists():
            try:
                self.root.iconbitmap(default=str(icon_path))
            except tk.TclError:
                # На некоторых системах/окружениях Tk может не поддерживать ICO.
                pass

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        title_font = tkfont.Font(family=theme.FONT_FAMILY, size=20, weight="bold")
        sub_font = tkfont.Font(family=theme.FONT_FAMILY, size=10)
        status_font = tkfont.Font(family=theme.FONT_FAMILY, size=13, weight="bold")

        header = tk.Frame(self.root, bg=theme.BG)
        header.pack(fill="x", pady=(28, 4), padx=28)

        tk.Label(header, text="\U0001F5A5  Icon Hider", bg=theme.BG, fg=theme.TEXT,
                  font=title_font).pack(anchor="w")
        tk.Label(header, text="Скрывай иконки рабочего стола одним кликом",
                  bg=theme.BG, fg=theme.SUBTEXT, font=sub_font).pack(anchor="w", pady=(4, 0))

        card = tk.Frame(self.root, bg=theme.CARD)
        card.pack(fill="both", expand=False, padx=24, pady=20)

        inner = tk.Frame(card, bg=theme.CARD)
        inner.pack(fill="both", expand=True, padx=24, pady=24)

        self.status_dot = tk.Canvas(inner, width=14, height=14, bg=theme.CARD, highlightthickness=0)
        self.status_dot.pack(pady=(4, 10))

        self.status_label = tk.Label(inner, text="", bg=theme.CARD, fg=theme.TEXT, font=status_font)
        self.status_label.pack()

        self.hint_label = tk.Label(inner, text="", bg=theme.CARD, fg=theme.SUBTEXT,
                                     font=tkfont.Font(family=theme.FONT_FAMILY, size=9))
        self.hint_label.pack(pady=(2, 20))

        self.toggle_btn = RoundButton(inner, "Скрыть иконки", self.toggle_icons,
                                       width=250, height=56)
        self.toggle_btn.pack(pady=(0, 12))

        tray_btn = RoundButton(inner, "Свернуть в трей", self.hide_to_tray,
                                width=250, height=46, bg=theme.CARD_ALT, hover=theme.CARD_ALT_HOVER)
        tray_btn.pack()

        version = tk.Label(self.root, text="Version 1.0.0  •  Windows",
                            bg=theme.BG, fg=theme.SUBTEXT, font=tkfont.Font(family=theme.FONT_FAMILY, size=8))
        version.pack(side="bottom", pady=(0, 2))

        footer = tk.Label(self.root, text="Ctrl+Alt+H — быстрое переключение  •  фон при закрытии",
                            bg=theme.BG, fg=theme.SUBTEXT, font=tkfont.Font(family=theme.FONT_FAMILY, size=8))
        footer.pack(side="bottom", pady=16)

    def _update_status(self):
        color = theme.ACCENT_ON if self.visible else theme.DANGER
        self.status_dot.delete("all")
        self.status_dot.create_oval(2, 2, 12, 12, fill=color, outline="")

        if self.visible:
            self.status_label.config(text="Иконки видны")
            self.hint_label.config(text="Рабочий стол в обычном режиме")
            self.toggle_btn.set_text("Скрыть иконки")
            self.toggle_btn.set_colors(theme.ACCENT, theme.ACCENT_HOVER)
        else:
            self.status_label.config(text="Иконки скрыты")
            self.hint_label.config(text="Рабочий стол очищен от значков")
            self.toggle_btn.set_text("Показать иконки")
            self.toggle_btn.set_colors(theme.ACCENT_ON, theme.ACCENT_ON_HOVER)

    # --------------------------------------------------------------- логика
    def toggle_icons(self):
        new_state = not self.visible
        if desktop.set_icons_visible(new_state):
            self.visible = new_state
        self._update_status()
        self.tray.refresh(self.visible)

    def hide_to_tray(self):
        self.root.withdraw()
        self.tray.show()

    def _show_window(self):
        self.root.after(0, self.root.deiconify)

    def quit_app(self):
        self.tray.stop()
        self.root.after(0, self.root.destroy)

    def run(self):
        self.root.mainloop()
