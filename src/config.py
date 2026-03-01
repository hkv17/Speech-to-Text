# =============================================================================
# Configuration — edit this file to customise the app
# =============================================================================

# --- Model ------------------------------------------------------------------

# Whisper model to use for transcription.
# Options (trade-off: speed vs accuracy):
#   "mlx-community/whisper-small-mlx"      ~500 MB  fastest
#   "mlx-community/whisper-medium-mlx"     ~1.5 GB  balanced  ← default
#   "mlx-community/whisper-large-v3-mlx"   ~3 GB    most accurate
MODEL_NAME = "mlx-community/whisper-medium-mlx"

# Words/phrases to hint the model toward when transcribing mixed-language speech.
# Add technical terms that the model tends to mis-transcribe in Russian phonetics.
INITIAL_PROMPT = (
    "LLM, AI, API, Claude, Claude Code, Anthropic, "
    "Visual Studio Code, VS Code, Python, speech to text, "
    "prompt, token, GPT, ChatGPT, GitHub, JavaScript, TypeScript"
)

# --- Sound ------------------------------------------------------------------

# Play a sound when transcription is done and the text is in the clipboard.
SOUND_ENABLED = True

# macOS system sound name (files live in /System/Library/Sounds/).
# Options: Ping, Tink, Pop, Glass, Funk, Basso, Blow, Bottle,
#          Frog, Hero, Morse, Purr, Sosumi, Submarine
SOUND_NAME = "Ping"

# --- History ----------------------------------------------------------------

# Save transcription history to a local JSONL file.
HISTORY_ENABLED = True

# How many recent transcriptions to keep (older entries are trimmed).
HISTORY_MAX_ENTRIES = 15

# Number of recent transcriptions shown in the menu bar dropdown.
MENU_RECENT_COUNT = 3

# Max characters to show per item in the menu bar (longer texts are truncated).
MENU_RECENT_MAX_LENGTH = 50
