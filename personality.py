"""CatCodeDidi's greeting, based on the time of day."""

import datetime


def hour_in_12_hour_clock(hour):
    """Turn a 24-hour number into a 12-hour one (13 becomes 1)."""
    if hour == 0:
        return 12          # midnight is said as "12", not "0"
    elif hour > 12:
        return hour - 12
    else:
        return hour


def say_the_time(now):
    """Describe the time the way people actually say it in Hindi."""
    hour = hour_in_12_hour_clock(now.hour)
    next_hour = hour_in_12_hour_clock(now.hour + 1)
    minute = now.minute

    if minute == 0:
        return f"{hour} baj rahe hai"
    elif minute == 15:
        return f"sawa {hour} baj rahe hai"
    elif minute == 30 and hour == 1:
        return "dedh baj rahe hai"          # 1:30 has its own word
    elif minute == 30 and hour == 2:
        return "dhai baj rahe hai"          # so does 2:30
    elif minute == 30:
        return f"sadhe {hour} baj rahe hai"
    elif minute == 45:
        return f"paune {next_hour} baj rahe hai"
    else:
        return f"{hour} baj kar {minute} minute ho rahe hai"


def get_greeting(now=None):
    """Return a greeting like 'Good Morning Sir, Abhi Subah ke 10 baj rahe hai!'"""
    if now is None:
        now = datetime.datetime.now()

    hour = now.hour
    time_text = say_the_time(now)

    if 5 <= hour <= 11:
        return f"Good Morning Sir, Abhi Subah ke {time_text}!"
    elif 12 <= hour <= 16:
        return f"Good Afternoon Sir, Abhi Dopahar ke {time_text}!"
    elif 17 <= hour <= 20:
        return f"Good Evening Sir, Abhi Shaam ke {time_text}!"
    else:
        return f"Hello Night Owl, Abhi Raat ke {time_text}!"
