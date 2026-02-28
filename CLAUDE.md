# Speech-to-Text App

## Описание
Локальная программа speech-to-text для macOS M1 (Apple Silicon).
Слушает нажатие F5 глобально (в любом приложении), записывает голос,
транскрибирует через mlx-whisper локально, копирует результат в буфер обмена.
Языки: русский и английский (авто-определение моделью).

## Архитектура (State Machine)
```
IDLE --[F5]--> RECORDING --[F5]--> TRANSCRIBING --> IDLE
                                        |
                              копирует текст в буфер обмена
```

## Файлы
- `main.py` — точка входа, state machine, координация компонентов
- `src/audio_recorder.py` — запись с микрофона через sounddevice (16kHz, mono)
- `src/transcriber.py` — STT через mlx_whisper, модель whisper-medium-mlx
- `src/hotkey_listener.py` — глобальный слушатель клавиши F5 через pynput
- `src/clipboard_handler.py` — копирование в буфер через pyperclip
- `src/menu_bar.py` — иконка в menu bar через rumps (🎤 Idle / 🔴 Recording / ⏳ Transcribing)

## Tech Stack
- Python 3.11
- mlx-whisper (Apple Silicon native, Metal GPU)
- sounddevice (аудио запись)
- pynput (глобальные горячие клавиши)
- pyperclip (буфер обмена)
- rumps (macOS menu bar)

## Модель
- `mlx-community/whisper-medium-mlx` (~1.5GB)
- Скачивается автоматически при первом запуске в `~/.cache/huggingface/hub/`
- Поддерживает ru + en с авто-определением языка

## Разрешения (требуются однократно)
System Settings → Privacy & Security:
- **Accessibility** → добавить Terminal и VSCode (для перехвата клавиш)
- **Microphone** → добавить Terminal и VSCode (для записи аудио)

## Клавиша F5
На MacBook F5 по умолчанию = яркость клавиатуры.
Рекомендуется: System Settings → Keyboard → включить "Use F1, F2... as standard function keys"
Тогда F5 работает напрямую без Fn. Или нажимать Fn+F5.

## Запуск
```bash
source venv/bin/activate
python main.py
```

## Установка (первый раз)
```bash
brew install python@3.11
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
