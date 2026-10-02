"""CatCodeDidi - a friendly Hindi-speaking voice assistant.

Run it with:   python main.py

How the program works:

    listen to the user
            |
            v
    is it a command we know?
            |
      +-----+------+
      |            |
     yes           no
      |            |
      v            v
  do the thing   ask Gemini AI
      |            |
      +-----+------+
            |
            v
      show the reply
            |
            v
     speak the reply
"""

import commands
import gemini_ai
import personality
import speech
import wakeword
from config import BOT_NAME
from data import (
    exit_commands,
    increase_volume_commands,
    decrease_volume_commands,
    open_new_tab_commands,
    close_tab_commands,
    open_browser_menu_commands,
    zoom_in_commands,
    zoom_out_commands,
    refresh_page_commands,
    next_tab_commands,
    previous_tab_commands,
    open_history_commands,
    open_bookmarks_commands,
    go_back_commands,
    go_forward_commands,
    open_dev_tools_commands,
    toggle_full_screen_commands,
    open_private_window_commands,
    scroll_up_commands,
    scroll_down_commands,
    scoll_to_top_commands,
    scoll_to_end_commands,
)


def handle_user_input(user_input):
    """Work out what the user wants and return CatCodeDidi's reply.

    This is the heart of the program. We check the commands we know how to
    do ourselves, and if it is none of them, we ask Gemini.
    """
    words = user_input.split()
    if not words:
        return ""

    first_word = words[0].lower()

    # "open notepad" -> first word is "open", the rest is the app name
    if first_word == "open" and len(words) > 1:
        app_name = " ".join(words[1:])
        return commands.open_application(app_name)

    elif first_word == "close" and len(words) > 1:
        app_name = " ".join(words[1:])
        return commands.close_application(app_name)

    elif "screenshot" in user_input.lower():
        return commands.take_screenshot()

    elif commands.is_creator_question(user_input):
        return "Mere Papa Anant Hai!"

    elif first_word == "mute":
        speech.set_muted(True)
        print("Voice turned off. Say 'unmute' to turn it back on.")
        return ""                      # nothing to say - we are muted!

    elif first_word == "unmute":
        speech.set_muted(False)
        return "Maalik, ab mai phir se bol sakti hu!"

    elif user_input.strip().lower() in increase_volume_commands:
        commands.Increase_volume()

    elif user_input.strip().lower() in decrease_volume_commands:
        commands.Decrease_volume()

    elif user_input.strip().lower() in open_new_tab_commands:
        commands.open_new_tab()

    elif user_input.strip().lower() in close_tab_commands:
        commands.close_tab()

    elif user_input.strip().lower() in open_browser_menu_commands:
        commands.open_browser_menu()

    elif user_input.strip().lower() in zoom_in_commands:
        commands.zoom_in()

    elif user_input.strip().lower() in zoom_out_commands:
        commands.zoom_out()

    elif user_input.strip().lower() in refresh_page_commands:
        commands.refresh_page()

    elif user_input.strip().lower() in next_tab_commands:
        commands.switch_to_next_tab()

    elif user_input.strip().lower() in previous_tab_commands:
        commands.switch_to_previous_tab()

    elif user_input.strip().lower() in open_history_commands:
        commands.open_history()

    elif user_input.strip().lower() in open_bookmarks_commands:
        commands.open_bookmarks()

    elif user_input.strip().lower() in go_back_commands:
        commands.go_back()

    elif user_input.strip().lower() in go_forward_commands:
        commands.go_forward()

    elif user_input.strip().lower() in open_dev_tools_commands:
        commands.open_dev_tools()

    elif user_input.strip().lower() in toggle_full_screen_commands:
        commands.toggle_full_screen()

    elif user_input.strip().lower() in open_private_window_commands:
        commands.open_private_window()

    elif user_input.strip().lower() in scroll_up_commands:
        commands.scroll_up()

    elif user_input.strip().lower() in scroll_down_commands:
        commands.scroll_down()

    elif user_input.strip().lower() in scoll_to_top_commands:
        commands.scroll_to_top()

    elif user_input.strip().lower() in scoll_to_end_commands:
        commands.scroll_to_bottom()

    # We did not recognise the command, so let the AI answer it.
    else:
        return gemini_ai.ask_gemini(user_input)


def show_and_speak(reply):
    """Print CatCodeDidi's reply and then say it out loud."""
    if not reply:
        return

    print(f"\n{BOT_NAME}: {reply}")
    speech.speak(speech.clean_for_speech(reply))


def main():
    """Greet the user, then answer commands until they say goodbye."""
    print(f"{BOT_NAME} is starting up. Press Ctrl+C to quit.\n")

    # Only use the wake word if the optional library is installed.
    use_wake_word = wakeword.is_wake_word_ready()
    if not use_wake_word:
        print('Tip: install the wake word with "pip install -r requirements-wake.txt"')

    show_and_speak(personality.get_greeting())

    while True:
        if use_wake_word:
            wakeword.wait_for_wake_word()

        user_input = speech.listen_to_user()

        # Nothing was understood, so go around and listen again.
        if not user_input:
            continue

        print(f"\nYou: {user_input}")

        if user_input.strip().lower() in exit_commands:
            show_and_speak("Good Bye, Maalik! Sulululu")
            break

        reply = handle_user_input(user_input)
        show_and_speak(reply)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
