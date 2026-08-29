"""Tests for the wake word."""

import wakeword


def test_the_wake_words_are_accepted():
    assert wakeword.heard_a_wake_word("didi") is True
    assert wakeword.heard_a_wake_word("cat code") is True
    assert wakeword.heard_a_wake_word("cat code didi") is True


def test_capital_letters_and_spaces_do_not_matter():
    assert wakeword.heard_a_wake_word("  DIDI  ") is True


def test_other_sentences_are_ignored():
    # Vosk always picks the closest phrase from our list, so a normal
    # sentence comes back with "[unk]" in it. Those must not wake us up.
    assert wakeword.heard_a_wake_word("[unk] didi") is False
    assert wakeword.heard_a_wake_word("didi [unk]") is False
    assert wakeword.heard_a_wake_word("[unk]") is False
    assert wakeword.heard_a_wake_word("") is False
