"""Listening to the user and speaking back.

We use three libraries here:
  - speech_recognition : records the microphone and turns speech into text
  - gTTS               : turns text into an MP3 file (Google Text-to-Speech)
  - playsound3         : plays that MP3 file
"""

import os
import platform
import re
import tempfile

import playsound3
import speech_recognition as sr
from gtts import gTTS

from config import LANGUAGE

# Stop listening after 8 seconds of silence, and never record a single
# sentence for longer than 15 seconds.
LISTEN_TIMEOUT = 8
MAX_SENTENCE_SECONDS = 15

# When this is True, CatCodeDidi still answers but stays quiet.
# The user turns it on and off by saying "mute" or "unmute".
muted = False


def set_muted(should_be_muted):
    """Turn the voice off (True) or back on (False)."""
    global muted
    muted = should_be_muted


def clean_for_speech(text):
    """Remove symbols that sound strange when read out loud.

    Gemini often replies with Markdown like **bold**, and we do not want
    CatCodeDidi to say "star star bold star star".
    """
    return re.sub(r"[*:;/\\|`#]", "", text)


def speak(text):
    """Say the text out loud in Hindi."""
    if muted or not text.strip():
        return

    # gTTS needs a real file to write to, so we make a temporary one.
    # We close it first because Windows will not let two programs write
    # to the same open file.
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    mp3_path = temp_file.name
    temp_file.close()

    try:
        gTTS(text=text, lang=LANGUAGE).save(mp3_path)
        playsound3.playsound(mp3_path)
    except Exception as error:
        print(f"Could not speak: {error}")
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)


def microphone_help():
    """Tell the user where to switch the microphone permission on."""
    system = platform.system()

    if system == "Darwin":          # Darwin is the name macOS reports
        return "Open System Settings > Privacy & Security > Microphone."
    elif system == "Windows":
        return "Open Settings > Privacy & security > Microphone."
    else:
        return "Check your sound settings and that a microphone is plugged in."


def listen_to_user():
    """Record one sentence and return it as text.

    Returns an empty string if we could not understand anything. The reason
    is printed so the user knows what went wrong.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as microphone:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(microphone, duration=0.4)
            audio = recognizer.listen(
                microphone,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=MAX_SENTENCE_SECONDS,
            )
    except sr.WaitTimeoutError:
        print("I did not hear anything. Please try again.")
        return ""
    except Exception as error:
        print(f"I cannot use the microphone. {microphone_help()}")
        print(f"Details: {error}")
        return ""

    # The audio is sent to Google's free speech service, so this step
    # needs an internet connection.
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        return ""
    except sr.RequestError:
        print("I could not reach the speech service. Check your internet.")
        return ""
