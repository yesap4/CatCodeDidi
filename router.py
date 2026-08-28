"""Command router: turn recognized text into a response + activity log.

This module owns no I/O beyond calling the existing handlers. It never
speaks and never touches the GUI.
"""

from dataclasses import dataclass, field

from commands import (
    handle_close_command,
    handle_open_command,
    is_father_query,
    take_screenshot,
)
from data import exit_commands
from gemini_ai import ask_gemini

FATHER_ANSWER = "Mere Papa Anant Hai!"
GEMINI_FALLBACK = "Maalik, Mere System mein kuch dikkat aa rahi hai!"


@dataclass
class RouteResult:
    """Result of routing one utterance."""

    user_text: str
    response_text: str = ""
    log_lines: list = field(default_factory=list)
    is_exit: bool = False


def route(said):
    """Route recognized speech to the right handler and return a RouteResult."""
    result = RouteResult(user_text=said)
    words = said.split()
    if not words:
        return result

    if is_father_query(said):
        result.response_text = FATHER_ANSWER
        result.log_lines.append("Creator query answered")
        return result

    if said.strip().lower() in exit_commands:
        result.response_text = "Good Bye, Maalik!, Sulululu"
        result.is_exit = True
        result.log_lines.append("Exit command received")
        return result

    verb = words[0].lower()
    if len(words) > 1 and verb in ("open", "close"):
        app_name = " ".join(words[1:])
        handler = handle_open_command if verb == "open" else handle_close_command
        command_result = handler(app_name)
        result.response_text = command_result.speech
        result.log_lines.append(command_result.log)
        return result

    if "screenshot" in (w.lower() for w in words):
        command_result = take_screenshot()
        result.response_text = command_result.speech
        result.log_lines.append(command_result.log)
        return result

    # Anything else goes to Gemini.
    result.log_lines.append(f"AI request: {said}")
    try:
        result.response_text = ask_gemini(said)
    except Exception as error:
        result.response_text = GEMINI_FALLBACK
        result.log_lines.append(f"AI error: {error}")
    return result
