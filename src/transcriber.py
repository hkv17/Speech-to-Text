import mlx_whisper

MODEL_NAME = "mlx-community/whisper-medium-mlx"

# Hint the model about English terms that appear in Russian speech.
# Add your own technical terms here to improve mixed-language accuracy.
INITIAL_PROMPT = (
    "LLM, AI, API, Claude, Claude Code, Anthropic, "
    "Visual Studio Code, VS Code, Python, speech to text, "
    "prompt, token, GPT, ChatGPT, GitHub, JavaScript, TypeScript"
)


class Transcriber:
    def __init__(self) -> None:
        self._model_name = MODEL_NAME

    def transcribe(self, audio) -> str:
        result = mlx_whisper.transcribe(
            audio,
            path_or_hf_repo=self._model_name,
            language=None,  # auto-detect between ru/en
            initial_prompt=INITIAL_PROMPT,
        )
        return result["text"].strip()
