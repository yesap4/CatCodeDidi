"""Speech input and output for the voice assistant."""

import os
import re
import tempfile
from dataclasses import dataclass

import playsound3
import speech_recognition as sr
from gtts import gTTS

from config import LANGUAGE


@dataclass
class RecognitionResult:
    """Outcome of a single microphone listen + recognition attempt."""

    text: str = ""
    error: str = ""

    @property
    def ok(self):
        return bool(self.text) and not self.error


def clean_for_speech(text):
    """Strip Markdown punctuation that sounds wrong when read aloud."""
    return re.sub(r"[*:;/\\|]", "", text)


def play_audio(file_path):
    """Play an audio file through the current playback library."""
    playsound3.playsound(file_path)


def bot_speak(text):
    """Convert text to Hindi speech, play it, and clean up the temporary file."""
    temp_file_path = None
    try:
        # Create a unique temporary MP3, then close it so Windows can write to it.
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_file_path = temp_audio.name

        tts = gTTS(text=text, lang=LANGUAGE)
        tts.save(temp_file_path)
        play_audio(temp_file_path)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def recognize_once():
    """Listen through the microphone once and return a RecognitionResult.

    Unlike voice_input(), this never speaks on failure; the caller decides
    how to surface the error (useful for the GUI).
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
    except OSError as error:
        return RecognitionResult(error=f"Microphone unavailable: {error}")

    try:
        return RecognitionResult(text=recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        return RecognitionResult(error="Samajh nahi aaya, phir se boliye.")
    except sr.RequestError as error:
        return RecognitionResult(error=f"Speech service error: {error}")


def voice_input():
    """Listen through the microphone and return the recognized speech (console flow)."""
    print("\n Listening...")
    result = recognize_once()
    if result.ok:
        print(f"You: {result.text}")
        return result.text
    bot_speak("Maalik, Phir se boliye mai sun nahi paa rahi hu!")
    return ""
