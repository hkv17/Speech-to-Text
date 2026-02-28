# Speech-to-Text

Локальная программа speech-to-text для macOS (Apple Silicon M1/M2/M3).
Слушает нажатие **F5** глобально, записывает голос, транскрибирует через
локальную нейросеть Whisper, помещает результат в буфер обмена.

---

## Быстрый старт

```bash
source venv/bin/activate
python main.py
```

Или нажать **F5** в VSCode (конфигурация запуска уже настроена).

---

## Использование

| Действие | Результат |
|---|---|
| Нажать **F5** | Начало записи |
| Нажать **F5** повторно | Остановка, транскрипция, текст в буфере обмена |
| **Cmd+V** в любом приложении | Вставить распознанный текст |
| **Ctrl+C** в терминале | Выход из программы |

Программа работает в фоне — VSCode можно свернуть, F5 будет перехватываться
в любом активном окне.

---

## Установка (первый раз)

```bash
brew install python@3.11   # или использовать имеющийся Python 3.11+
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Разрешения macOS (однократно)

- **System Settings → Privacy & Security → Accessibility** → добавить VSCode и Terminal
  _(нужно для глобального перехвата клавиш)_
- Доступ к микрофону запросится автоматически при первом запуске

---

## Настройка модели

Настройка находится в файле [`src/transcriber.py`](src/transcriber.py), строка `MODEL_NAME`.

| Модель | Размер | Скорость | Точность | Когда использовать |
|---|---|---|---|---|
| `mlx-community/whisper-small-mlx` | ~500 MB | Быстро | Хорошая | Если важна скорость |
| `mlx-community/whisper-medium-mlx` | ~1.5 GB | Средне | Очень хорошая | **По умолчанию** |
| `mlx-community/whisper-large-v3-mlx` | ~3 GB | Медленно | Отличная | Если важна точность |

**Как сменить модель:**

Откройте [`src/transcriber.py`](src/transcriber.py) и измените первую строку:

```python
MODEL_NAME = "mlx-community/whisper-large-v3-mlx"  # ← вставьте нужную
```

Модель скачается автоматически при первом запуске в `~/.cache/huggingface/hub/`.

### Добавить английские термины для лучшего распознавания

Если программа неправильно пишет технические термины (например, пишет
«клад кода» вместо «Claude Code»), добавьте нужное слово в `INITIAL_PROMPT`
в файле [`src/transcriber.py`](src/transcriber.py):

```python
INITIAL_PROMPT = (
    "LLM, AI, API, Claude, Claude Code, ВашТермин, ..."
)
```

---

## Настройка звукового сигнала

Настройка находится в файле [`src/config.py`](src/config.py).

### Включить / выключить звук

```python
SOUND_ENABLED = True   # звук включён
SOUND_ENABLED = False  # звук выключен
```

### Сменить звук

```python
SOUND_NAME = "Ping"  # ← название звука
```

**Доступные звуки macOS:**

| Название | Характер |
|---|---|
| `Ping` | Короткий, чёткий _(по умолчанию)_ |
| `Tink` | Тихий, мягкий |
| `Pop` | Лёгкий хлопок |
| `Glass` | Стеклянный |
| `Funk` | Низкий, глухой |
| `Hero` | Торжественный |
| `Basso` | Глубокий бас |
| `Blow` | Дуновение |
| `Bottle` | Бутылка |
| `Frog` | Лягушка |
| `Morse` | Морзе |
| `Purr` | Мурчание |
| `Sosumi` | Классический Mac |
| `Submarine` | Подводная лодка |

---

## Структура проекта

```
├── main.py                  # Точка входа
├── src/
│   ├── config.py            # Настройки (звук)
│   ├── audio_recorder.py    # Запись с микрофона
│   ├── transcriber.py       # Модель + промт для терминов
│   ├── hotkey_listener.py   # Перехват клавиши F5
│   └── clipboard_handler.py # Копирование в буфер
└── .claude/agents/          # Агенты для Claude Code
    ├── setup-checker.md     # Проверка окружения
    └── transcription-tester.md  # Тест качества
```
