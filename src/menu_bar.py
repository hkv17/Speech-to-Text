import rumps


class MenuBarController:
    _ICON = {"IDLE": "🎤", "RECORDING": "🔴", "TRANSCRIBING": "⏳"}
    _TEXT = {"IDLE": "Ready", "RECORDING": "Recording...", "TRANSCRIBING": "Transcribing..."}

    def __init__(self) -> None:
        self._app = rumps.App("🎤", quit_button="Quit")
        self._status = rumps.MenuItem("Ready", callback=None)
        self._app.menu = [self._status, None]  # None = separator before Quit

    def set_state(self, state) -> None:
        self._app.title = self._ICON[state.name]
        self._status.title = self._TEXT[state.name]

    def run(self) -> None:
        self._app.run()
