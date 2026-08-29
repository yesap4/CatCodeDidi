"""Tests for the greeting."""

import datetime

import personality


def at_time(hour, minute=0):
    """Build a date/time we can use in a test."""
    return datetime.datetime(2026, 8, 29, hour, minute)


def test_greeting_changes_through_the_day():
    assert "Good Morning" in personality.get_greeting(at_time(8))
    assert "Good Afternoon" in personality.get_greeting(at_time(14))
    assert "Good Evening" in personality.get_greeting(at_time(19))
    assert "Night Owl" in personality.get_greeting(at_time(23))
    assert "Night Owl" in personality.get_greeting(at_time(2))


def test_the_minutes_are_included():
    # This used to be broken: 10:33 was announced as just "10".
    assert "33" in personality.get_greeting(at_time(10, 33))


def test_special_ways_of_saying_the_time():
    assert "sawa 10" in personality.get_greeting(at_time(10, 15))
    assert "sadhe 10" in personality.get_greeting(at_time(10, 30))
    assert "paune 11" in personality.get_greeting(at_time(10, 45))
    assert "dedh" in personality.get_greeting(at_time(1, 30))
    assert "dhai" in personality.get_greeting(at_time(2, 30))


def test_midnight_is_called_twelve():
    assert "12" in personality.get_greeting(at_time(0, 0))


def test_the_hour_is_never_negative():
    # This used to be broken: 2am was announced as "-10".
    for hour in range(24):
        assert "-" not in personality.get_greeting(at_time(hour, 20))


def test_the_12_hour_clock():
    assert personality.hour_in_12_hour_clock(0) == 12
    assert personality.hour_in_12_hour_clock(9) == 9
    assert personality.hour_in_12_hour_clock(13) == 1
    assert personality.hour_in_12_hour_clock(23) == 11
