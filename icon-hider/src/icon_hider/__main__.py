"""Точка входа: python -m icon_hider"""

import sys


def main():
    if sys.platform != "win32":
        print("Icon Hider работает только на Windows.")
        sys.exit(1)

    from .app import IconHiderApp

    app = IconHiderApp()
    app.run()


if __name__ == "__main__":
    main()
