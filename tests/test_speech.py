"""Tests for listening and speaking."""

import speech_recognition as sr

import speech


def test_clean_for_speech_removes_symbols():
    # Gemini writes **bold**, but we do not want to hear "star star".
    assert speech.clean_for_speech("**bold** text") == "bold text"
    assert speech.clean_for_speech("note: it works") == "note it works"


def test_muting_stops_the_voice(monkeypatch):
    spoken = []
    monkeypatch.setattr(speech, "gTTS", lambda **kwargs: spoken.append(1))

    speech.set_muted(True)
    speech.speak("hello")
    assert spoken == []             # nothing was said

    speech.set_muted(False)         # put it back for the other tests


def test_empty_text_is_not_spoken(monkeypatch):
    spoken = []
    monkeypatch.setattr(speech, "gTTS", lambda **kwargs: spoken.append(1))
    speech.speak("   ")
    assert spoken == []


def test_microphone_help_gives_advice():
    advice = speech.microphone_help()
    assert "Microphone" in advice or "microphone" in advice


class PretendMicrophone:
    """Stands in for a real microphone during tests."""

    def __enter__(self):
        return "microphone"

    def __exit__(self, *args):
        return False


def test_listening_returns_what_was_said(monkeypatch):
    class PretendRecognizer:
        def adjust_for_ambient_noise(self, *args, **kwargs):
            pass

        def listen(self, *args, **kwargs):
            return "audio"

        def recognize_google(self, audio):
            return "open google chrome"

    monkeypatch.setattr(speech.sr, "Microphone", lambda: PretendMicrophone())
    monkeypatch.setattr(speech.sr, "Recognizer", lambda: PretendRecognizer())

    assert speech.listen_to_user() == "open google chrome"


def test_listening_returns_empty_text_when_it_cannot_understand(monkeypatch):
    class ConfusedRecognizer:
        def adjust_for_ambient_noise(self, *args, **kwargs):
            pass

        def listen(self, *args, **kwargs):
            return "audio"

        def recognize_google(self, audio):
            raise sr.UnknownValueError()

    monkeypatch.setattr(speech.sr, "Microphone", lambda: PretendMicrophone())
    monkeypatch.setattr(speech.sr, "Recognizer", lambda: ConfusedRecognizer())

    assert speech.listen_to_user() == ""


def test_a_broken_microphone_does_not_crash(monkeypatch):
    class BrokenMicrophone:
        def __enter__(self):
            raise OSError("permission denied")

        def __exit__(self, *args):
            return False

    monkeypatch.setattr(speech.sr, "Microphone", lambda: BrokenMicrophone())
    assert speech.listen_to_user() == ""
