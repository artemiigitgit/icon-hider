"""
hotkey.py
---------
Регистрация глобальной горячей клавиши через WinAPI (RegisterHotKey)
и прослушивание её в отдельном потоке.
"""

import ctypes
import threading

user32 = ctypes.windll.user32

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
WM_HOTKEY = 0x0312


class GlobalHotkey:
    """Слушает одну глобальную комбинацию клавиш и вызывает callback при срабатывании."""

    def __init__(self, callback, modifiers=MOD_CONTROL | MOD_ALT, vk_code=0x48, hotkey_id=1):
        # vk_code=0x48 -> клавиша "H" по умолчанию (Ctrl+Alt+H)
        self.callback = callback
        self.modifiers = modifiers
        self.vk_code = vk_code
        self.hotkey_id = hotkey_id
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def _listen(self):
        if not user32.RegisterHotKey(None, self.hotkey_id, self.modifiers, self.vk_code):
            return
        msg = ctypes.wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == WM_HOTKEY and msg.wParam == self.hotkey_id:
                    self.callback()
        finally:
            user32.UnregisterHotKey(None, self.hotkey_id)
