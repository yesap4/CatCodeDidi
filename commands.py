"""Local desktop command handlers.

Handlers do not speak or touch any UI. Each returns a CommandResult so the
caller (console loop or GUI) decides how to present it.
"""

import datetime
import platform
import shutil
import subprocess
from dataclasses import dataclass

import pyscreenshot

from data import FATHER_RELATED_QUESTIONS

_SYSTEM = platform.system()


@dataclass
class CommandResult:
    """What a command did: text to speak/show, and an activity-log line."""

    speech: str
    log: str
    ok: bool = True


def _open_application(app_name):
    """Open an application on the current platform, raising on failure."""
    if _SYSTEM == "Darwin":
        subprocess.run(["open", "-a", app_name], check=True,
                       capture_output=True, text=True)
    elif _SYSTEM == "Windows":
        from AppOpener import open as open_application
        open_application(app_name, match_closest=True, throw_error=True)
    else:
        launcher = shutil.which(app_name.lower().replace(" ", "-")) or shutil.which(app_name)
        if not launcher:
            raise RuntimeError(f"{app_name} not found")
        subprocess.Popen([launcher])


def _close_application(app_name):
    """Close an application on the current platform, raising on failure."""
    if _SYSTEM == "Darwin":
        subprocess.run(["osascript", "-e", f'quit app "{app_name}"'], check=True,
                       capture_output=True, text=True)
    elif _SYSTEM == "Windows":
        from AppOpener import close as close_application
        close_application(app_name, match_closest=True)
    else:
        subprocess.run(["pkill", "-f", app_name], check=True)


def handle_open_command(app_name):
    """Open an application and report the outcome."""
    try:
        _open_application(app_name)
        return CommandResult(
            speech=f"Thik hai Maalik! , Mai {app_name} ko open kar deti hu",
            log=f"Application opened: {app_name}",
        )
    except Exception:
        return CommandResult(
            speech=f"Maalik, {app_name} naam ka koi software hai hi nahi system mai!",
            log=f"Open failed: {app_name}",
            ok=False,
        )


def handle_close_command(app_name):
    """Close an application and report the outcome."""
    try:
        _close_application(app_name)
        return CommandResult(
            speech=f"Maalik, {app_name} Ko Band Kar deti hu !",
            log=f"Application closed: {app_name}",
        )
    except Exception:
        return CommandResult(
            speech=f"Maalik, {app_name} naam ka koi software open nahi hai toh chinta mat kijiye",
            log=f"Close skipped (not running?): {app_name}",
            ok=False,
        )


def is_father_query(command):
    """Return whether command is a supported creator query."""
    return command.strip().casefold() in FATHER_RELATED_QUESTIONS


def take_screenshot():
    """Grab the screen to a timestamped PNG and report the outcome."""
    try:
        image = pyscreenshot.grab()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        image.save(filename)
        return CommandResult(
            speech="Screenshot le liya Maalik!",
            log=f"Screenshot saved: {filename}",
        )
    except Exception as error:
        return CommandResult(
            speech="Maalik, screenshot lene mein dikkat aa gayi!",
            log=f"Screenshot failed: {error}",
            ok=False,
        )
