import mlx_whisper

from src.config import INITIAL_PROMPT, MODEL_NAME


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
