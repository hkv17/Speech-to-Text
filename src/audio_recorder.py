import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import threading

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"
OUTPUT_PATH = "/tmp/stt_recording.wav"


class AudioRecorder:
    def __init__(self):
        self._chunks: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None
        self._lock = threading.Lock()

    def start(self) -> None:
        self._chunks = []
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=self._callback,
        )
        self._stream.start()

    def _callback(self, indata: np.ndarray, frames: int, time, status) -> None:
        with self._lock:
            self._chunks.append(indata.copy())

    def stop(self) -> np.ndarray:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        with self._lock:
            if not self._chunks:
                raise RuntimeError("No audio recorded")
            audio = np.concatenate(self._chunks, axis=0).flatten()

        return audio  # float32 array in [-1.0, 1.0], ready for mlx_whisper
