#!/usr/bin/env python3
"""Точка запуска Icon Hider.

Работает как из исходников, так и внутри PyInstaller .exe.
"""
import sys
from pathlib import Path

# В режиме исходников добавляем src в начало пути.
if not getattr(sys, "frozen", False):
    ROOT = Path(__file__).resolve().parent
    SRC = ROOT / "src"
    sys.path.insert(0, str(SRC))

from icon_hider.app import IconHiderApp


def main():
    if sys.platform != "win32":
        print("Icon Hider работает только на Windows.")
        return 1

    IconHiderApp().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
