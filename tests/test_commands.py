"""Tests for the computer commands."""

import commands


def test_recognises_questions_about_the_creator():
    assert commands.is_creator_question("who is your father") is True
    assert commands.is_creator_question("WHO IS YOUR FATHER") is True
    assert commands.is_creator_question("what is the weather") is False


def test_linux_command_names():
    # On Linux the program is called "google-chrome", not "Google Chrome".
    names = commands.linux_command_names("Google Chrome")
    assert "google-chrome" in names


def test_find_mac_app_returns_none_when_not_installed():
    assert commands.find_mac_app("SomeAppThatDoesNotExist") is None


def test_opening_a_missing_app_gives_a_friendly_reply(monkeypatch):
    def pretend_it_failed(*args, **kwargs):
        raise Exception("no such app")

    monkeypatch.setattr(commands.subprocess, "run", pretend_it_failed)
    monkeypatch.setattr(commands.subprocess, "Popen", pretend_it_failed)

    reply = commands.open_application("Nonesuch")
    assert "nahi" in reply          # the reply says it could not be found


def test_closing_an_app_that_is_not_running_is_handled(monkeypatch):
    def pretend_it_failed(*args, **kwargs):
        raise Exception("not running")

    monkeypatch.setattr(commands.subprocess, "run", pretend_it_failed)
    reply = commands.close_application("Nonesuch")
    assert "chinta mat kijiye" in reply


def test_screenshot_saves_a_file(monkeypatch, tmp_path):
    class PretendImage:
        def convert(self, mode):
            return self

        def getextrema(self):
            return (0, 255)         # not a black picture

        def save(self, path):
            open(path, "w").close()

    monkeypatch.setattr(commands, "SCREENSHOT_FOLDER", str(tmp_path))
    monkeypatch.setattr(commands.pyscreenshot, "grab", lambda: PretendImage())

    reply = commands.take_screenshot()
    assert "Screenshot le liya" in reply
    assert len(list(tmp_path.iterdir())) == 1


def test_a_black_screenshot_asks_for_permission(monkeypatch, tmp_path):
    class BlackImage:
        def convert(self, mode):
            return self

        def getextrema(self):
            return (0, 0)           # completely black = permission refused

        def save(self, path):
            raise AssertionError("should not save a blank screenshot")

    monkeypatch.setattr(commands, "SCREENSHOT_FOLDER", str(tmp_path))
    monkeypatch.setattr(commands.pyscreenshot, "grab", lambda: BlackImage())

    reply = commands.take_screenshot()
    assert "permission" in reply
