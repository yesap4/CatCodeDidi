"""Tests for the Gemini AI helper."""

import gemini_ai


def test_a_missing_api_key_gives_a_helpful_message(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    reply = gemini_ai.ask_gemini("hello")
    assert "GEMINI_API_KEY" in reply
    assert ".env" in reply


def test_the_answer_is_returned(monkeypatch):
    class PretendResponse:
        text = "  Paris  "

    class PretendModels:
        def generate_content(self, **kwargs):
            return PretendResponse()

    class PretendClient:
        models = PretendModels()

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(gemini_ai, "client", PretendClient())

    assert gemini_ai.ask_gemini("capital of France?") == "Paris"


def test_a_broken_connection_does_not_crash(monkeypatch):
    class BrokenClient:
        class models:
            @staticmethod
            def generate_content(**kwargs):
                raise Exception("no internet")

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(gemini_ai, "client", BrokenClient())

    reply = gemini_ai.ask_gemini("hello")
    assert "dikkat" in reply        # the friendly Hinglish error message


def test_the_api_key_is_never_shown_to_the_user(monkeypatch):
    class LeakyClient:
        class models:
            @staticmethod
            def generate_content(**kwargs):
                raise Exception("bad key: AIzaSySECRET123")

    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSySECRET123")
    monkeypatch.setattr(gemini_ai, "client", LeakyClient())

    reply = gemini_ai.ask_gemini("hello")
    assert "AIzaSy" not in reply
