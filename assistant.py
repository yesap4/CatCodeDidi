"""Assistant orchestration: the 'brain' that runs one voice interaction.

The GUI is a presentation layer on top of this. Every step reports progress
through the `emit` callback passed to the constructor:

    emit("state", "Listening...")
    emit("transcript", "open google chrome")
    emit("message", ("CatCodeDidi", "Thik hai Maalik!"))
    emit("log", "Application opened: google chrome")
    emit("exit", None)

All methods here block; the caller is expected to run them off the UI thread.
"""

import router
import speech
from config import BOT_NAME
from personality import greeting

STATE_READY = "Ready"
STATE_LISTENING = "Listening..."
STATE_PROCESSING = "Processing..."
STATE_SPEAKING = "Speaking..."
STATE_ERROR = "Error"


class Assistant:
    def __init__(self, emit):
        self._emit = emit

    def _speak(self, text):
        self._emit("state", STATE_SPEAKING)
        try:
            speech.bot_speak(speech.clean_for_speech(text))
        except Exception as error:
            self._emit("log", f"Speech playback failed: {error}")

    def startup_greeting(self):
        """Greet the user once when the app launches."""
        text = greeting()
        self._emit("message", (BOT_NAME, text))
        self._speak(text)
        self._emit("state", STATE_READY)

    def run_interaction(self):
        """Run a full listen -> route -> respond -> speak cycle."""
        self._emit("state", STATE_LISTENING)
        heard = speech.recognize_once()

        if not heard.ok:
            self._emit("state", STATE_ERROR)
            self._emit("log", f"Recognition failed: {heard.error}")
            self._emit("message", (BOT_NAME, heard.error or "Kuch samajh nahi aaya."))
            self._emit("state", STATE_READY)
            return

        self._emit("transcript", heard.text)
        self._emit("state", STATE_PROCESSING)

        result = router.route(heard.text)
        for line in result.log_lines:
            self._emit("log", line)

        if result.response_text:
            self._emit("message", (BOT_NAME, result.response_text))
            self._speak(result.response_text)

        self._emit("state", STATE_READY)
        if result.is_exit:
            self._emit("exit", None)
