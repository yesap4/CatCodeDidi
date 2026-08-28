"""Personality responses for the voice assistant."""

import datetime

from speech import bot_speak


def greeting():
    """Return the correct time-based greeting text."""
    current_time = int(datetime.datetime.now().strftime("%H"))

    if 5 <= current_time < 12:
        return f"Good Morning Sir, Abhi Subah ke {current_time} baj rahe hai!"
    if current_time == 12:
        return "Good Afternoon Sir, Abhi Dophar ke 12 baj rahe hai!"
    if 13 <= current_time < 17:
        return f"Good Afternoon Sir, Abhi Dophar ke {current_time - 12} baj rahe hai!"
    if 17 <= current_time < 21:
        return f"Good Evening Sir, Abhi Shaam ke {current_time - 12} baj rahe hai!"
    return f"Hello Night Owl, Abhi Raat ke {current_time - 12} baj rahe hai!"


def greet_user():
    """Speak the time-based greeting (console flow)."""
    bot_speak(greeting())
