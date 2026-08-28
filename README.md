# CatCodeDidi Voice Assistant

CatCodeDidi is a beginner-friendly Hindi-speaking desktop voice assistant. This
project intentionally grows in small, understandable phases.

Since Phase 2 it runs as a **Tkinter desktop app**: press the microphone button,
speak a command, and watch the assistant's state, the recognized command, her
response, and the actions she takes.

## Installation

Use Python 3.10 or newer, then install the dependencies from this folder:

```bash
pip install -r requirements.txt
```

The GUI uses **Tkinter**, which ships with the Python standard library on most
desktop installations. If `import tkinter` fails, install your platform's Tk
package (for example `brew install python-tk` on macOS, or
`sudo apt install python3-tk` on Debian/Ubuntu).

Optional: for AI answers, create a `.env` file with your Gemini key:

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash   # optional override
```

## Run

```bash
python main.py
```

The CatCodeDidi window opens and greets you. Click **🎤 Speak** and say one of:

- `open Google Chrome`
- `close Google Chrome`
- `take a screenshot`
- `who is your father`
- `shutdown` (also `bye`, `good night`, …)

Anything else is sent to Gemini and the answer is shown and spoken.

## How a voice interaction works

```
press 🎤  ->  Listening...  ->  Processing...  ->  Speaking...  ->  Ready
                   |                  |                 |
              speech.py          router.py          speech.py
            recognize_once()   route(text)         bot_speak()
```

Each step updates the **Status** pill. The recognized command and the reply
appear in the **Conversation** area; opened/closed apps, screenshots, AI
requests and errors appear in the **Activity log**. Recognition or Gemini
failures are shown in the GUI and never crash the window.

## Architecture

```
main.py  ->  gui.py  ->  assistant.py  ->  router.py ─┬─ commands.py
          (Tkinter,       (interaction     (routing)  ├─ gemini_ai.py
           threads)        orchestration)             ├─ personality.py
                                                      └─ data.py
```

- `main.py`: entry point; launches the GUI.
- `gui.py`: Tkinter presentation layer. Runs each interaction on a background
  thread and receives progress events through a thread-safe queue drained on
  the Tk main loop, so the window never freezes while listening, recognizing,
  calling Gemini, or speaking.
- `assistant.py`: `Assistant` class — the "brain". Runs one
  listen → route → respond → speak cycle and reports every step via an `emit`
  callback. Contains no GUI code.
- `router.py`: turns recognized text into a response plus activity-log lines by
  calling the existing command handlers or Gemini.
- `speech.py`: microphone input, Google speech recognition (`recognize_once`),
  Hindi text-to-speech (`bot_speak`), audio playback, speech text cleanup.
- `commands.py`: cross-platform open/close application, screenshot, creator-query
  detection. Each handler returns a `CommandResult` (no UI, no speech).
- `personality.py`: time-based greeting text.
- `gemini_ai.py`: Gemini integration; client is configured lazily and honours
  `GEMINI_API_KEY` / `GEMINI_MODEL`.
- `config.py`: `BOT_NAME`, `LANGUAGE`.
- `data.py`: static command / creator-query data.
- `utils.py`: reserved for later phases.

The console flow is still available as library functions (`speech.voice_input`,
`personality.greet_user`) but `python main.py` now opens the GUI.

## Roadmap

1. **Phase 1 — Refactor and make robust.** ✅
2. **Phase 2 — Desktop GUI.** ✅ Tkinter window with status, microphone button,
   conversation view, and activity log; blocking work moved to background
   threads.
3. **Phase 3 — AI:** deepen the modular AI provider.
4. **Phase 4 — Search plus AI:** retrieval, summarisation, and scoped automation.
