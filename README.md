# CatCodeDidi

CatCodeDidi is a friendly, Hindi-speaking voice assistant you run in the
terminal. You talk to her, she opens apps, takes screenshots, or answers your
question using Google's Gemini AI — and replies out loud.

This project is written to be **easy to read**. Every file is short, there are
no classes, and the whole program flow fits on one screen.

---

## What she can do

| Say this | What happens |
|---|---|
| `open Google Chrome` | opens the app |
| `close Google Chrome` | closes the app |
| `take a screenshot` | saves a picture of your screen |
| `who is your father` | she tells you who made her |
| `mute` / `unmute` | turns her voice off and on |
| `shutdown`, `bye`, `good night` | quits |
| anything else | Gemini AI answers it |

---

## Installing

You need **Python 3.10 or newer** and an internet connection.

**1. Install the sound library your computer needs**

```bash
brew install portaudio                                # macOS
sudo apt install python3-venv portaudio19-dev         # Ubuntu / Debian
sudo dnf install portaudio-devel                      # Fedora
```

Windows needs nothing extra.

**2. Set up the project**

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**3. Add your Gemini key** (optional — everything except AI answers works without it)

Get a free key from <https://aistudio.google.com/apikey>, then:

```bash
cp .env.example .env
```

Open `.env` and paste your key next to `GEMINI_API_KEY=`.

**4. Run it**

```bash
python main.py
```

---

## How the program works

The whole journey is easy to follow:

```
        you speak
            |
            v
   speech.listen_to_user()          turns your voice into text
            |
            v
   main.handle_user_input()         decides what to do
            |
      +-----+------+
      |            |
  a command      not a command
      |            |
      v            v
  commands.py   gemini_ai.ask_gemini()
      |            |
      +-----+------+
            |
            v
   main.show_and_speak()            prints it, then says it out loud
```

### The files

| File | What it does |
|---|---|
| `main.py` | the program flow — listens, decides, replies |
| `speech.py` | listening to the microphone and speaking out loud |
| `commands.py` | opening apps, closing apps, taking screenshots |
| `gemini_ai.py` | asking Gemini AI a question |
| `personality.py` | the greeting, based on the time of day |
| `wakeword.py` | optional: waiting for you to say "Didi" |
| `config.py` | her name and language |
| `data.py` | the lists of words she recognises |

Each file has a few short functions, and each function does one job.

---

## The Gemini AI part

Your key lives in `.env`, which is never committed to git, so it stays private.

```dotenv
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.5-flash-lite     # optional
```

We use **`gemini-3.5-flash-lite`** because it is Google's fastest model. A voice
assistant asks lots of short questions, so answering quickly matters more than
thinking deeply. You can change the model in `.env` without touching any code.

If the key is missing or the internet is down, CatCodeDidi says so politely
instead of crashing.

---

## Wake word (optional)

If you want to say **"Didi"** instead of pressing a key first:

```bash
pip install -r requirements-wake.txt
```

The first time you use it, a speech model (~40 MB) is downloaded. After that it
works **completely offline** — your voice is never uploaded anywhere to check
for the wake word.

It listens for exactly three phrases: **"Cat Code Didi"**, **"Cat Code"** and
**"Didi"**.

> A neat detail worth understanding: the speech library always picks the
> closest phrase from our list, so "what is the weather today" comes back as
> `[unk] didi`. If we only checked whether "didi" appeared *somewhere* in the
> text, she would wake up by accident. That is why `heard_a_wake_word()`
> checks for an **exact** match.

---

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest
```

36 tests. They are written to be readable too — open `tests/test_main.py` to
see how each sentence is sent to the right place.

---

## If something goes wrong

| Problem | Fix |
|---|---|
| `pip install pyaudio` fails | Install PortAudio first (step 1 above). |
| "I cannot use the microphone" | Give your terminal microphone permission in your system settings. |
| "Sorry, I could not understand that" | Background noise, or no internet — speech recognition happens online. |
| The screenshot is blank on macOS | Allow Screen Recording in System Settings > Privacy & Security. |
| "Gemini ki API key nahi mili" | Copy `.env.example` to `.env` and add your key. |
| No sound on Linux | Install `ffmpeg` or GStreamer. |

---

## Which computers this works on

Opening and closing apps works differently on each system, so `commands.py`
checks which one you are using:

| | Windows | macOS | Linux |
|---|---|---|---|
| Open an app | `AppOpener` | `open -a` | runs the command directly |
| Close an app | `AppOpener` | `osascript` | `pkill` |

Tested on macOS with Python 3.13. The Windows and Linux code is written and
covered by tests, but has not been run on those machines yet.
