"""Asking Google's Gemini AI a question.

Anything that is not a built-in command gets sent here.

The API key is read from a file called ".env" so it never appears in the
code. Copy ".env.example" to ".env" and paste your key in.
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# gemini-3.5-flash-lite is Google's fastest model. A voice assistant sends
# many short questions, so speed matters more than deep reasoning.
# You can pick a different model in .env without changing this file.
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

# This tells Gemini how to behave. Keep it short - it is sent with every
# single question, so a long one makes every answer slower.
PERSONALITY = """
You are Cat Code Didi, a friendly female desktop voice assistant.
Call yourself "Didi". Never say out loud that you are a girl.
If the user writes in English, reply in English.
If the user writes in Hindi or Hinglish, reply in Hinglish using English
letters only - never Devanagari script.
Keep answers short and chatty, because they are read out loud.
"""

# We build the connection to Gemini once and reuse it. Making a new one for
# every question would be slow.
client = None


def ask_gemini(message):
    """Send a question to Gemini and return the answer as text.

    If anything goes wrong we return a friendly sentence instead of
    crashing, so the assistant keeps working.
    """
    global client

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return ("Maalik, Gemini ki API key nahi mili. "
                "Please add GEMINI_API_KEY to your .env file.")

    try:
        if client is None:
            client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=PERSONALITY,
                # "low" thinking keeps simple questions fast and cheap.
                thinking_config=types.ThinkingConfig(thinking_level="low"),
                # We never give Gemini tools to call, and turning this off
                # stops it printing a warning every time we ask something.
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True),
            ),
        )
        return response.text.strip()

    except Exception as error:
        print(f"Gemini error: {error}")
        return "Maalik, mere system mein kuch dikkat aa rahi hai!"
