import subprocess
import sys
import threading
from enum import Enum, auto

from src.audio_recorder import AudioRecorder
from src.clipboard_handler import copy_to_clipboard
from src.config import HISTORY_ENABLED, SOUND_ENABLED, SOUND_NAME
from src.history import HistoryManager
from src.hotkey_listener import HotkeyListener
from src.menu_bar import MenuBarController
from src.transcriber import Transcriber


class State(Enum):
    IDLE = auto()
    RECORDING = auto()
    TRANSCRIBING = auto()


class App:
    def __init__(self) -> None:
        self._state = State.IDLE
        self._lock = threading.Lock()
        self._recorder = AudioRecorder()
        self._transcriber = Transcriber()
        self._hotkey = HotkeyListener(on_f5=self._on_f5)
        self._history = HistoryManager()
        self._menu_bar = MenuBarController(history=self._history)

    def run(self) -> None:
        print("Press F5 to start recording. Press F5 again to stop and transcribe.")
        print("Note: first transcription will download the model (~1.5GB) and may take a few minutes.")
        self._hotkey.start()
        self._menu_bar.run()  # blocks; exits when user clicks Quit in menu bar
        self._hotkey.stop()

    def _on_f5(self) -> None:
        with self._lock:
            current = self._state

        if current == State.IDLE:
            self._start_recording()
        elif current == State.RECORDING:
            self._stop_and_transcribe()
        # Ignore F5 while TRANSCRIBING

    def _start_recording(self) -> None:
        with self._lock:
            self._state = State.RECORDING
        self._menu_bar.set_state(State.RECORDING)
        print("Recording... (press F5 to stop)")
        self._recorder.start()

    def _stop_and_transcribe(self) -> None:
        with self._lock:
            self._state = State.TRANSCRIBING
        self._menu_bar.set_state(State.TRANSCRIBING)
        print("Transcribing...")

        try:
            audio = self._recorder.stop()
            text = self._transcriber.transcribe(audio)

            if text:
                copy_to_clipboard(text)
                if HISTORY_ENABLED:
                    self._history.add(text)
                    self._menu_bar.refresh_history()
                print(f"Copied to clipboard: {text}")
                self._play_done_sound()
            else:
                print("No speech detected.")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        finally:
            with self._lock:
                self._state = State.IDLE
            self._menu_bar.set_state(State.IDLE)
            print("\nReady. Press F5 to record.")


    def _play_done_sound(self) -> None:
        if not SOUND_ENABLED:
            return
        sound_path = f"/System/Library/Sounds/{SOUND_NAME}.aiff"
        def _play() -> None:
            result = subprocess.run(["afplay", sound_path], capture_output=True)
            if result.returncode != 0:
                print(f"Sound error: {result.stderr.decode()}", file=sys.stderr)
        threading.Thread(target=_play, daemon=True).start()


if __name__ == "__main__":
    App().run()
