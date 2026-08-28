"""Local desktop command handlers."""

import datetime
import platform
import shutil
import subprocess

import pyscreenshot

from data import FATHER_RELATED_QUESTIONS
from speech import bot_speak

_SYSTEM = platform.system()


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
        bot_speak(f"Thik hai Maalik! , Mai {app_name} ko open kar deti hu")
    except Exception:
        bot_speak(f"Maalik, {app_name} naam ka koi software hai hi nahi system mai!")


def handle_close_command(app_name):
    """Close an application and report the outcome."""
    try:
        _close_application(app_name)
        bot_speak(f"Maalik, {app_name} Ko Band Kar deti hu !")
    except Exception:
        bot_speak(f"Maalik, {app_name} naam ka koi software open nahi hai toh chinta mat kijiye")


def is_father_query(command):
    """Return whether command is a supported creator query."""
    return command.strip().casefold() in FATHER_RELATED_QUESTIONS


def take_screenshot():
    image = pyscreenshot.grab()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image.save(f"screenshot_{timestamp}.png")
