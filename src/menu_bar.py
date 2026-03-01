import subprocess

import rumps

from src.clipboard_handler import copy_to_clipboard
from src.config import MENU_RECENT_COUNT, MENU_RECENT_MAX_LENGTH
from src.history import HISTORY_FILE


class MenuBarController:
    _ICON = {"IDLE": "🎤", "RECORDING": "🔴", "TRANSCRIBING": "⏳"}
    _TEXT = {"IDLE": "Ready", "RECORDING": "Recording...", "TRANSCRIBING": "Transcribing..."}

    def __init__(self, history) -> None:
        self._history = history
        self._app = rumps.App("🎤", quit_button="Quit")
        self._status = rumps.MenuItem("Ready", callback=None)

        self._recent_items: list[rumps.MenuItem] = []
        for _ in range(MENU_RECENT_COUNT):
            item = rumps.MenuItem("", callback=self._copy_text)
            self._recent_items.append(item)

        self._open_history_item = rumps.MenuItem(
            "Open History File", callback=self._open_history
        )

        self._build_menu()

    def _build_menu(self) -> None:
        menu = [self._status, None]
        recent = list(reversed(self._history.get_recent(MENU_RECENT_COUNT)))
        for i, item in enumerate(self._recent_items):
            if i < len(recent):
                item.title = self._truncate(recent[i]["text"])
                item._full_text = recent[i]["text"]
            else:
                item.title = "—"
                item._full_text = ""
                item.set_callback(None)
            menu.append(item)
        menu.append(None)  # separator
        menu.append(self._open_history_item)
        self._app.menu = menu

    def refresh_history(self) -> None:
        recent = list(reversed(self._history.get_recent(MENU_RECENT_COUNT)))
        for i, item in enumerate(self._recent_items):
            if i < len(recent):
                item.title = self._truncate(recent[i]["text"])
                item._full_text = recent[i]["text"]
                item.set_callback(self._copy_text)
            else:
                item.title = "—"
                item._full_text = ""
                item.set_callback(None)

    def set_state(self, state) -> None:
        self._app.title = self._ICON[state.name]
        self._status.title = self._TEXT[state.name]

    def run(self) -> None:
        self._app.run()

    def _copy_text(self, sender) -> None:
        text = getattr(sender, "_full_text", "")
        if text:
            copy_to_clipboard(text)
            print(f"Copied from history: {text[:60]}...")

    def _open_history(self, _sender) -> None:
        if HISTORY_FILE.exists():
            subprocess.Popen(["open", "-t", str(HISTORY_FILE)])
        else:
            rumps.alert("No history file yet. Record something first!")

    @staticmethod
    def _truncate(text: str) -> str:
        if len(text) <= MENU_RECENT_MAX_LENGTH:
            return text
        return text[:MENU_RECENT_MAX_LENGTH] + "…"
