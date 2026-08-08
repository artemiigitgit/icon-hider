"""
desktop.py
----------
Низкоуровневая работа с рабочим столом Windows через WinAPI:
поиск окна со списком иконок (SysListView32) и переключение
его видимости.
"""

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

SW_HIDE = 0
SW_SHOW = 5


def _find_desktop_listview():
    """Находит хендл окна SysListView32, в котором лежат иконки рабочего стола."""
    # Основной путь (Windows 10/11): Progman -> SHELLDLL_DefView -> SysListView32
    progman = user32.FindWindowW("Progman", None)
    def_view = user32.FindWindowExW(progman, 0, "SHELLDLL_DefView", None)

    if not def_view:
        # Иногда SHELLDLL_DefView лежит в отдельном окне WorkerW
        result = {"hwnd": None}

        @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        def enum_windows_proc(hwnd, lparam):
            p = user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None)
            if p:
                result["hwnd"] = p
                return False
            return True

        user32.EnumWindows(enum_windows_proc, 0)
        def_view = result["hwnd"]

    if not def_view:
        return None

    return user32.FindWindowExW(def_view, 0, "SysListView32", "FolderView")


def set_icons_visible(visible: bool) -> bool:
    """Показывает или скрывает иконки рабочего стола. Возвращает True при успехе."""
    hwnd = _find_desktop_listview()
    if not hwnd:
        return False
    user32.ShowWindow(hwnd, SW_SHOW if visible else SW_HIDE)
    return True


def icons_are_visible() -> bool:
    """Проверяет, видны ли сейчас иконки рабочего стола."""
    hwnd = _find_desktop_listview()
    if not hwnd:
        return True
    return bool(user32.IsWindowVisible(hwnd))
