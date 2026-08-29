"""Waiting for the user to say a wake word.

This is optional. Install it with:

    pip install -r requirements-wake.txt

We use Vosk, which understands speech *offline* - nothing is uploaded to
the internet. We also give it a short list of the only phrases it is
allowed to hear, which makes it fast and accurate.
"""

import json

import pyaudio

# Vosk is optional. If it is not installed the assistant still works fine,
# it just cannot listen for a wake word.
try:
    import vosk
    VOSK_INSTALLED = True
except ImportError:
    VOSK_INSTALLED = False

WAKE_WORDS = ["cat code didi", "cat code", "didi"]

SAMPLE_RATE = 16000       # how many sound measurements per second
CHUNK_SIZE = 4000         # how much audio we read at a time

# We load the speech model once and keep it, because loading is slow.
model = None


def is_wake_word_ready():
    """Return True if the optional Vosk library is installed."""
    return VOSK_INSTALLED


def load_model():
    """Load the Vosk speech model, downloading it the first time."""
    global model

    if model is None:
        vosk.SetLogLevel(-1)          # hide Vosk's very chatty log messages
        print("Getting the wake word ready (this takes a moment)...")
        model = vosk.Model(lang="en-us")

    return model


def heard_a_wake_word(spoken_text):
    """Return True only if the text is exactly one of our wake words.

    Vosk always picks the closest phrase from our list, so "what is the
    weather today" comes back as "[unk] didi". If we just checked whether
    "didi" was somewhere in the text, the assistant would wake up by
    mistake. Checking for an exact match avoids that.
    """
    return spoken_text.strip().lower() in WAKE_WORDS


def wait_for_wake_word():
    """Listen until the user says a wake word, then return True.

    This blocks (waits) until it hears something, which is fine because
    our program has nothing else to do until then.
    """
    speech_model = load_model()

    # Tell Vosk the only phrases it is allowed to recognise. "[unk]" means
    # "something else", which is how we detect that it was not a wake word.
    allowed_phrases = json.dumps(WAKE_WORDS + ["[unk]"])
    recognizer = vosk.KaldiRecognizer(speech_model, SAMPLE_RATE, allowed_phrases)

    microphone = pyaudio.PyAudio()
    stream = microphone.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    print('\nSay "Didi" to wake me up...')

    try:
        while True:
            audio_chunk = stream.read(CHUNK_SIZE, exception_on_overflow=False)

            # AcceptWaveform returns True once it has heard a full phrase.
            if recognizer.AcceptWaveform(audio_chunk):
                result = json.loads(recognizer.Result())
                if heard_a_wake_word(result.get("text", "")):
                    return True
    finally:
        # Always release the microphone, even if something goes wrong,
        # so we can use it again to listen to the actual command.
        stream.stop_stream()
        stream.close()
        microphone.terminate()
