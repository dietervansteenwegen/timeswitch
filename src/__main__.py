import gettext
import locale
import os
import signal
import sys
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path

import gi


gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


def _resolve_version() -> str:
    try:
        return package_version("timeswitch")
    except PackageNotFoundError:
        return "dev"


def _try_register_resource() -> None:
    from gi.repository import Gio

    package_dir = Path(__file__).resolve().parent
    project_root = package_dir.parent

    candidates = [
        package_dir / "timeswitch.gresource",
        project_root / "build" / "src" / "timeswitch.gresource",
    ]

    for candidate in candidates:
        if candidate.exists():
            resource = Gio.Resource.load(str(candidate))
            resource._register()
            break


def main() -> int:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    locale.textdomain("timeswitch")
    gettext.install("timeswitch")

    _try_register_resource()

    from . import main as app_main

    return app_main.main(_resolve_version())


if __name__ == "__main__":
    sys.exit(main())
