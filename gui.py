"""Tkinter desktop GUI for CatCodeDidi.

The GUI is a thin presentation layer. It owns no assistant logic: it starts
a background worker for each interaction and receives progress events through
a thread-safe queue that is drained on the Tk main loop.
"""

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext

from assistant import (
    STATE_ERROR,
    STATE_LISTENING,
    STATE_PROCESSING,
    STATE_READY,
    STATE_SPEAKING,
    Assistant,
)
from config import BOT_NAME

STATE_COLORS = {
    STATE_READY: "#2e7d32",
    STATE_LISTENING: "#1565c0",
    STATE_PROCESSING: "#e65100",
    STATE_SPEAKING: "#6a1b9a",
    STATE_ERROR: "#c62828",
}

BG = "#f4f4f5"
CARD_BG = "#ffffff"


class CatCodeDidiGUI:
    def __init__(self, root):
        self.root = root
        self.events = queue.Queue()
        self.assistant = Assistant(self._emit)
        self._worker = None

        root.title(BOT_NAME)
        root.geometry("640x620")
        root.configure(bg=BG)
        root.minsize(520, 480)

        self._build_header()
        self._build_status()
        self._build_mic_button()
        self._build_panels()

        self._append(self.conversation, f"{BOT_NAME} is starting up...\n")
        self._drain_events()
        self._run_in_background(self.assistant.startup_greeting)

    # ---------- layout ----------

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=16, pady=(16, 8))
        tk.Label(header, text="🐱", font=("Helvetica", 34), bg=BG).pack(side="left")
        titles = tk.Frame(header, bg=BG)
        titles.pack(side="left", padx=12)
        tk.Label(titles, text=BOT_NAME, font=("Helvetica", 20, "bold"),
                 bg=BG).pack(anchor="w")
        tk.Label(titles, text="Hindi-speaking desktop voice assistant",
                 font=("Helvetica", 10), fg="#666", bg=BG).pack(anchor="w")

    def _build_status(self):
        row = tk.Frame(self.root, bg=BG)
        row.pack(fill="x", padx=16, pady=4)
        tk.Label(row, text="Status:", font=("Helvetica", 10), bg=BG).pack(side="left")
        self.status_label = tk.Label(
            row, text=STATE_READY, font=("Helvetica", 11, "bold"),
            fg="white", bg=STATE_COLORS[STATE_READY], padx=12, pady=3,
        )
        self.status_label.pack(side="left", padx=8)

    def _build_mic_button(self):
        self.mic_button = tk.Button(
            self.root, text="🎤  Speak", font=("Helvetica", 14, "bold"),
            bg="#1565c0", fg="white", activebackground="#0d47a1",
            relief="flat", padx=20, pady=10, command=self._on_mic_click,
        )
        self.mic_button.pack(pady=10)

    def _build_panels(self):
        panels = tk.Frame(self.root, bg=BG)
        panels.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        conv_frame = tk.LabelFrame(panels, text="Conversation", bg=CARD_BG,
                                   font=("Helvetica", 10, "bold"))
        conv_frame.pack(fill="both", expand=True)
        self.conversation = scrolledtext.ScrolledText(
            conv_frame, wrap="word", height=12, font=("Helvetica", 11),
            bg=CARD_BG, relief="flat", state="disabled",
        )
        self.conversation.pack(fill="both", expand=True, padx=6, pady=6)

        log_frame = tk.LabelFrame(panels, text="Activity log", bg=CARD_BG,
                                  font=("Helvetica", 10, "bold"))
        log_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.activity = scrolledtext.ScrolledText(
            log_frame, wrap="word", height=6, font=("Courier", 10),
            bg=CARD_BG, fg="#333", relief="flat", state="disabled",
        )
        self.activity.pack(fill="both", expand=True, padx=6, pady=6)

    # ---------- text helpers ----------

    def _append(self, widget, text):
        widget.configure(state="normal")
        widget.insert("end", text)
        widget.see("end")
        widget.configure(state="disabled")

    # ---------- worker plumbing ----------

    def _emit(self, event_type, payload):
        """Called from the worker thread; hand the event to the UI thread."""
        self.events.put((event_type, payload))

    def _run_in_background(self, target):
        if self._worker and self._worker.is_alive():
            return
        self.mic_button.configure(state="disabled")

        def wrapper():
            try:
                target()
            except Exception as error:  # keep the GUI alive no matter what
                self._emit("log", f"Unexpected error: {error}")
                self._emit("state", STATE_ERROR)
            finally:
                self._emit("_worker_done", None)

        self._worker = threading.Thread(target=wrapper, daemon=True)
        self._worker.start()

    def _on_mic_click(self):
        self._run_in_background(self.assistant.run_interaction)

    def _drain_events(self):
        try:
            while True:
                event_type, payload = self.events.get_nowait()
                self._handle_event(event_type, payload)
        except queue.Empty:
            pass
        self.root.after(80, self._drain_events)

    def _handle_event(self, event_type, payload):
        if event_type == "state":
            color = STATE_COLORS.get(payload, "#555")
            self.status_label.configure(text=payload, bg=color)
        elif event_type == "transcript":
            self._append(self.conversation, f"\nUser:\n{payload}\n")
        elif event_type == "message":
            speaker, text = payload
            self._append(self.conversation, f"\n{speaker}:\n{text}\n")
        elif event_type == "log":
            self._append(self.activity, f"- {payload}\n")
        elif event_type == "exit":
            self._append(self.activity, "- Shutting down...\n")
            self.root.after(1200, self.root.destroy)
        elif event_type == "_worker_done":
            self.mic_button.configure(state="normal")


def main():
    root = tk.Tk()
    CatCodeDidiGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
