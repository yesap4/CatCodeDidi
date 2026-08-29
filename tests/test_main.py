"""Tests for the main program: does each sentence go to the right place?"""

import commands
import gemini_ai
import main
import speech


def test_open_goes_to_the_open_command(monkeypatch):
    opened = []
    monkeypatch.setattr(commands, "open_application",
                        lambda app_name: opened.append(app_name) or "opening")

    assert main.handle_user_input("open Google Chrome") == "opening"
    assert opened == ["Google Chrome"]      # the whole app name, not just one word


def test_close_goes_to_the_close_command(monkeypatch):
    closed = []
    monkeypatch.setattr(commands, "close_application",
                        lambda app_name: closed.append(app_name) or "closing")

    main.handle_user_input("close Safari")
    assert closed == ["Safari"]


def test_screenshot_goes_to_the_screenshot_command(monkeypatch):
    monkeypatch.setattr(commands, "take_screenshot", lambda: "took it")
    assert main.handle_user_input("take a screenshot") == "took it"


def test_a_question_about_the_creator_is_answered_here():
    assert main.handle_user_input("who is your father") == "Mere Papa Anant Hai!"


def test_anything_else_goes_to_gemini(monkeypatch):
    asked = []
    monkeypatch.setattr(gemini_ai, "ask_gemini",
                        lambda message: asked.append(message) or "an answer")

    assert main.handle_user_input("what is the capital of France") == "an answer"
    assert asked == ["what is the capital of France"]


def test_open_without_an_app_name_goes_to_gemini(monkeypatch):
    # "open" on its own is not a command we can carry out.
    monkeypatch.setattr(gemini_ai, "ask_gemini", lambda message: "an answer")
    assert main.handle_user_input("open") == "an answer"


def test_mute_and_unmute(monkeypatch):
    main.handle_user_input("mute")
    assert speech.muted is True

    main.handle_user_input("unmute")
    assert speech.muted is False


def test_show_and_speak_says_the_reply(monkeypatch):
    spoken = []
    monkeypatch.setattr(speech, "speak", lambda text: spoken.append(text))

    main.show_and_speak("Hello Maalik")
    assert spoken == ["Hello Maalik"]


def test_nothing_is_spoken_for_an_empty_reply(monkeypatch):
    spoken = []
    monkeypatch.setattr(speech, "speak", lambda text: spoken.append(text))

    main.show_and_speak("")
    assert spoken == []


def test_empty_input_is_ignored():
    assert main.handle_user_input("") == ""
    assert main.handle_user_input("   ") == ""
