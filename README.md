# Speech-to-Text (macOS, Offline, Whisper)

A local speech-to-text utility for macOS on Apple Silicon (M1/M2/M3).
It listens for the **F5** global hotkey, records your voice, transcribes it using
a local Whisper model, and copies the result to your clipboard.

## TL;DR

- Offline transcription — audio never leaves your machine
- macOS + Apple Silicon only (M1/M2/M3)
- Global hotkey: press **F5** to start / stop recording
- Result is copied to the clipboard automatically
- Menu bar icon shows live status and lets you re-copy recent transcriptions
- Transcription history saved locally; last 15 entries are kept
- Requires **Accessibility** permission (global hotkey) and **Microphone** permission (recording)
- Hotkey conflict: F5 may be captured by other apps or IDEs (including VSCode debugger)

---

## How it works

```
F5 → start recording → F5 → stop → transcribe (Whisper) → copy to clipboard → paste anywhere
```

---

## Quick Start

If running for the first time, the model downloads automatically (~1.5 GB).

```bash
source venv/bin/activate
python main.py
```

A launch configuration for VSCode is already included — you can also press **F5** inside VSCode
to start the app (note: this will be consumed by the debugger, not the app itself, while VSCode is focused).

---

## Usage

| Action                        | Result                                     |
| ----------------------------- | ------------------------------------------ |
| Press **F5**                  | Start recording                            |
| Press **F5** again            | Stop → transcribe → copy text to clipboard |
| **Cmd+V** anywhere            | Paste the recognised text                  |
| Click a recent item in menu   | Copy that transcription to clipboard again |
| **Open History File** in menu | Open full history in text editor           |
| **Quit** in menu bar          | Exit the app                               |

The program runs in the background — you can minimise VSCode/Terminal and
**F5** will still be captured in any active window.

## Menu Bar

The menu bar icon shows the current state at a glance:

| Icon | State          |
| ---- | -------------- |
| 🎤   | Idle, ready    |
| 🔴   | Recording      |
| ⏳   | Transcribing   |

Clicking the menu bar icon opens a dropdown with:
- **Status line** — current state in text
- **Last 3 transcriptions** — click any to copy it to the clipboard again
- **Open History File** — opens the full history (last 15 entries) in a text editor
- **Quit** — exits the app

---

## Installation (first time)

```bash
brew install python@3.11    # or use an existing Python 3.11+
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS Permissions (one-time)

**Accessibility** — required for global hotkey capture:

> System Settings → Privacy & Security → Accessibility

Add **Terminal** (or iTerm) and **VSCode** (if running from VSCode).
You may need to restart the app after granting the permission.

**Microphone** — macOS will prompt automatically on first run. Allow it.

---

## Configuration

All settings are in [`src/config.py`](src/config.py).

### Whisper model

```python
MODEL_NAME = "mlx-community/whisper-medium-mlx"
```

| Model                                | Size    | Speed  | Accuracy  | Use when         |
| ------------------------------------ | ------- | ------ | --------- | ---------------- |
| `mlx-community/whisper-small-mlx`    | ~500 MB | Fast   | Good      | Speed matters    |
| `mlx-community/whisper-medium-mlx`   | ~1.5 GB | Medium | Very good | **Default**      |
| `mlx-community/whisper-large-v3-mlx` | ~3 GB   | Slow   | Excellent | Accuracy matters |

Models are cached automatically at `~/.cache/huggingface/hub/`.

### Domain-specific terms (improve recognition of technical vocabulary)

If the model mis-transcribes technical terms (e.g. writes "клад кода" instead of "Claude Code"),
add them to `INITIAL_PROMPT` in [`src/config.py`](src/config.py):

```python
INITIAL_PROMPT = (
    "LLM, AI, API, Claude, Claude Code, YourTerm, ..."
)
```

### History

```python
HISTORY_ENABLED = True       # set to False to disable
HISTORY_MAX_ENTRIES = 15     # how many entries to keep in the file
MENU_RECENT_COUNT = 3        # how many to show in the menu bar dropdown
MENU_RECENT_MAX_LENGTH = 50  # max characters per item before truncating
```

History is saved to:
```
~/Library/Application Support/SpeechToText/history.jsonl
```

Each line is a JSON object: `{"ts": "2024-01-15T10:30:00", "text": "your transcription"}`.

---

### Sound feedback

```python
SOUND_ENABLED = True   # set to False to disable
SOUND_NAME = "Ping"    # name of the macOS system sound
```

Available sounds (files in `/System/Library/Sounds/`):

| Name        | Character                |
| ----------- | ------------------------ |
| `Ping`      | Short, crisp *(default)* |
| `Tink`      | Soft, quiet              |
| `Pop`       | Light pop                |
| `Glass`     | Glass tap                |
| `Funk`      | Low thud                 |
| `Hero`      | Triumphant               |
| `Basso`     | Deep bass                |
| `Blow`      | Breeze                   |
| `Bottle`    | Bottle blow              |
| `Frog`      | Frog croak               |
| `Morse`     | Morse beep               |
| `Purr`      | Purring                  |
| `Sosumi`    | Classic Mac              |
| `Submarine` | Sonar ping               |

---

## Troubleshooting

**F5 does not work globally**
- Make sure Accessibility permission is granted to the app you run from (Terminal / VSCode).
- Restart Terminal/VSCode after enabling the permission.
- Check that no other app is consuming F5 (browsers, IDEs, etc.).

**No microphone input / silence recorded**
- Check System Settings → Privacy & Security → Microphone and allow access.
- Verify the correct input device is selected in macOS Sound settings.

**Transcription is slow**
- Switch to a smaller model (`whisper-small-mlx`) in [`src/config.py`](src/config.py).
- The first run is slower while the model downloads.

**Technical terms are mis-transcribed**
- Add your terms to `INITIAL_PROMPT` in [`src/config.py`](src/config.py) (see Configuration above).

---

## Project structure

```
├── main.py                      # Entry point, state machine
├── src/
│   ├── config.py                # All settings (model, prompt, sound, history)
│   ├── audio_recorder.py        # Microphone recording
│   ├── transcriber.py           # Whisper inference
│   ├── hotkey_listener.py       # Global F5 listener
│   ├── clipboard_handler.py     # Clipboard integration
│   ├── menu_bar.py              # Menu bar icon and history dropdown
│   └── history.py               # JSONL history storage
└── .claude/agents/              # Claude Code agents
    ├── setup-checker.md         # Environment checks
    └── transcription-tester.md  # Transcription quality tests
```
