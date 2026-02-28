import json
from datetime import datetime
from pathlib import Path

from src.config import HISTORY_MAX_ENTRIES

HISTORY_DIR = Path.home() / "Library" / "Application Support" / "SpeechToText"
HISTORY_FILE = HISTORY_DIR / "history.jsonl"


class HistoryManager:
    def add(self, text: str) -> None:
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        entry = {"ts": datetime.now().isoformat(timespec="seconds"), "text": text}
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self._trim()

    def get_recent(self, n: int) -> list[dict]:
        if not HISTORY_FILE.exists():
            return []
        lines = HISTORY_FILE.read_text(encoding="utf-8").strip().splitlines()
        entries = [json.loads(line) for line in lines]
        return entries[-n:]

    def _trim(self) -> None:
        if not HISTORY_FILE.exists():
            return
        lines = HISTORY_FILE.read_text(encoding="utf-8").strip().splitlines()
        if len(lines) > HISTORY_MAX_ENTRIES:
            trimmed = lines[-HISTORY_MAX_ENTRIES:]
            HISTORY_FILE.write_text("\n".join(trimmed) + "\n", encoding="utf-8")
