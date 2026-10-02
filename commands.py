"""Things CatCodeDidi can do on the computer itself.

Every function here returns the sentence CatCodeDidi should reply with, so
the main program can simply print it and speak it.

Opening and closing apps works differently on each operating system, so
each function checks which one we are running on.
"""

import datetime
import glob
import os
import platform
import shutil
import pyautogui
import subprocess

import pyscreenshot

from data import FATHER_RELATED_QUESTIONS

# "Windows", "Darwin" (which is macOS) or "Linux"
SYSTEM = platform.system()

# Screenshots go in a folder next to this file, so they are always in the
# same place no matter where the program was started from.
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_FOLDER = os.path.join(PROJECT_FOLDER, "screenshots")


def find_mac_app(app_name):
    """Find the real app name on macOS, or return None.

    The user says "Chrome" but the app is really called "Google Chrome",
    so we look through the Applications folders for a close match.
    """
    folders = ["/Applications", "/Applications/Utilities", "/System/Applications"]
    wanted = app_name.lower()

    for folder in folders:
        for path in glob.glob(os.path.join(folder, "*.app")):
            # "/Applications/Google Chrome.app" -> "Google Chrome"
            name = os.path.basename(path)[:-4]
            if wanted in name.lower():
                return name

    return None


def linux_command_names(app_name):
    """Guess what the app is called on Linux.

    The user says "Google Chrome" but the command is "google-chrome".
    """
    lowercase = app_name.lower()
    return [app_name, lowercase, lowercase.replace(" ", "-")]


def open_application(app_name):
    """Open an app and return what CatCodeDidi should say."""
    try:
        if SYSTEM == "Darwin":
            real_name = find_mac_app(app_name) or app_name
            subprocess.run(["open", "-a", real_name], check=True, capture_output=True)

        elif SYSTEM == "Windows":
            from AppOpener import open as open_windows_app
            open_windows_app(app_name, match_closest=True, throw_error=True)

        else:
            command = None
            for name in linux_command_names(app_name):
                if shutil.which(name):
                    command = name
                    break
            if command is None:
                raise Exception(f"{app_name} is not installed")
            subprocess.Popen([command])

        return f"Thik hai Maalik! Mai {app_name} ko open kar deti hu"

    except Exception as error:
        print(f"Could not open {app_name}: {error}")
        return f"Maalik, {app_name} naam ka koi software hai hi nahi system mai!"


def close_application(app_name):
    """Close an app and return what CatCodeDidi should say."""
    try:
        if SYSTEM == "Darwin":
            real_name = find_mac_app(app_name) or app_name
            subprocess.run(["osascript", "-e", f'quit app "{real_name}"'],
                           check=True, capture_output=True)

        elif SYSTEM == "Windows":
            from AppOpener import close as close_windows_app
            close_windows_app(app_name, match_closest=True)

        else:
            # pkill matches the program's name, which never has spaces,
            # so we try the same name guesses we use for opening.
            closed = False
            for name in linux_command_names(app_name):
                if subprocess.run(["pkill", "-i", name]).returncode == 0:
                    closed = True
                    break
            if not closed:
                raise Exception(f"{app_name} is not running")

        return f"Maalik, {app_name} ko band kar deti hu!"

    except Exception as error:
        print(f"Could not close {app_name}: {error}")
        return f"Maalik, {app_name} naam ka koi software open nahi hai toh chinta mat kijiye"


def take_screenshot():
    """Save a picture of the screen and return what CatCodeDidi should say."""
    try:
        os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{timestamp}.png")

        image = pyscreenshot.grab()

        # On macOS a completely black picture means the Screen Recording
        # permission was refused, so we tell the user instead of saving it.
        if image.convert("L").getextrema() == (0, 0):
            print("The screenshot was blank. On macOS, allow Screen Recording "
                  "in System Settings > Privacy & Security.")
            return "Maalik, screenshot ke liye permission chahiye!"

        image.save(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        return "Screenshot le liya Maalik!"

    except Exception as error:
        print(f"Could not take a screenshot: {error}")
        return "Maalik, screenshot lene mein dikkat aa gayi!"


def is_creator_question(user_input):
    """Return True if the user asked who made CatCodeDidi."""
    return user_input.strip().lower() in FATHER_RELATED_QUESTIONS


def Increase_volume():
    pyautogui.press("volumeup")

def Decrease_volume():
    pyautogui.press("volumedown")


def scroll_up():
    # Scroll up by pressing the Up arrow key five times
    pyautogui.press('up', presses=5)

def scroll_down():
    # Scroll down by pressing the Down arrow key five times
    pyautogui.press('down', presses=5)

def scroll_to_top():
    # Scroll to the top of the page
    pyautogui.hotkey('home')

def scroll_to_bottom():
    # Scroll to the bottom of the page
    pyautogui.hotkey('end')


def open_new_tab():
    pyautogui.hotkey('ctrl', 't')

def close_tab():
    pyautogui.hotkey('ctrl', 'w')

def open_browser_menu():
    pyautogui.hotkey('alt', 'f')

def zoom_in():
    pyautogui.hotkey('ctrl', '+')

def zoom_out():
    pyautogui.hotkey('ctrl', '-')

def refresh_page():
    pyautogui.hotkey('ctrl', 'r')

def switch_to_next_tab():
    pyautogui.hotkey('ctrl', 'tab')

def switch_to_previous_tab():
    pyautogui.hotkey('ctrl', 'shift', 'tab')

def open_history():
    pyautogui.hotkey('ctrl', 'h')

def open_bookmarks():
    pyautogui.hotkey('ctrl', 'b')

def go_back():
    pyautogui.hotkey('alt', 'left')

def go_forward():
    pyautogui.hotkey('alt', 'right')

def open_dev_tools():
    pyautogui.hotkey('ctrl', 'shift', 'i')

def toggle_full_screen():
    pyautogui.hotkey('f11')

def open_private_window():
    pyautogui.hotkey('ctrl', 'shift', 'n')