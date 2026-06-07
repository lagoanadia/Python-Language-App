# Python Language App

A desktop app for learning Swedish through AI conversation and vocabulary tracking — built with Python, Ollama, and CustomTkinter.

**[→ View the code](app.py)**

---

## What it does

- **AI Chat** — conversational Swedish tutor powered by a local Ollama model (llama3.2). Responses are always in Swedish with English translation in parentheses, and mistakes are corrected in real time.
- **Vocabulary Tracker** — add words you encounter in conversation, save their translation, and persist them across sessions via CSV.
- **Quiz Mode** — flashcard-style quiz that pulls unlearnt words from your vocabulary list and tracks which ones you've mastered.

---

## Stack

- Python 3
- [Ollama](https://ollama.com) — local LLM inference (no API key needed)
- llama3.2 — language model
- CustomTkinter — desktop UI
- CSV — lightweight local data storage

---

## Project structure

```
Python-Language-App/
├── data/
│   ├── vocabulary.csv     # saved words and translations
│   └── quiz.csv           # word status (unlearnt / learnt)
├── app.py                 # main UI — chat, vocab list, quiz mode
├── ai.py                  # Ollama chat with conversation history
├── vocab.py               # vocabulary CSV CRUD
├── quiz.py                # quiz CSV CRUD and word status tracking
└── README.md
```

---

## How to run

**1. Install dependencies:**
```bash
pip install customtkinter ollama
```

**2. Install and run Ollama:**

Download from [ollama.com](https://ollama.com), then:
```bash
ollama pull llama3.2
```

**3. Run the app:**
```bash
python app.py
```

---

## Features

- AI conversation stays in context — full message history passed on every call
- Vocabulary persists across sessions — loaded automatically on startup
- Quiz mode tracks learnt vs unlearnt words and updates status in real time
- Delete words from both vocab list and quiz simultaneously

---

*Built as a personal language learning tool during my first year of DAM (Desarrollo de Aplicaciones Multiplataforma).*
