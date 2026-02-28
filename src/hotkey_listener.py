import threading
from typing import Callable
from pynput import keyboard


class HotkeyListener:
    """Listens for F5 key press globally and calls the provided callback."""

    def __init__(self, on_f5: Callable[[], None]) -> None:
        self._on_f5 = on_f5
        self._listener: keyboard.Listener | None = None

    def start(self) -> None:
        self._listener = keyboard.Listener(on_press=self._on_press)
        self._listener.daemon = True
        self._listener.start()

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        try:
            is_f5 = key == keyboard.Key.f5 or (hasattr(key, "vk") and key.vk == 176)
            if is_f5:
                thread = threading.Thread(target=self._on_f5, daemon=True)
                thread.start()
        except Exception:
            pass
