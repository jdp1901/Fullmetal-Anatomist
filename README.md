# ⚗️ Fullmetal Anatomist

> *"Equivalent Exchange: You give it textbook chapters, it gives you passing grades."*

An AI-powered medical study agent that transmutes dense textbook content into
interactive fill-in-the-blank worksheets. Built for med students who'd rather
be watching anime than re-reading Harrison's for the 47th time.

---

## ✨ Features

- 📄 **Paste or upload** textbook content (.txt, .pdf, .docx)
- 🤖 **AI-generated worksheets** — fill-in-the-blank, organized by section
- 🎚️ **Difficulty levels** — Easy / Medium / Hard
- ✅ **Interactive grading** — check answers, see your score
- 📥 **PDF export** — blank worksheet + answer key
- 💬 **Chat interface** — streaming AI assistant for follow-up questions
- 🔒 **Local-first** — your textbooks never leave your machine (except to your chosen LLM provider)
- 🔑 **Multi-provider** — Gemini, OpenAI, or Anthropic

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- An API key from **one** of:
  - [Google Gemini](https://aistudio.google.com/apikey) *(recommended — free tier available)*
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic](https://console.anthropic.com/)

### macOS

```bash
# Install Python & Node if needed
brew install python@3.12 node

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo
git clone https://github.com/YOUR_USERNAME/fullmetal-anatomist.git
cd fullmetal-anatomist

# Launch! (handles venv, deps, frontend build, and opens your browser)
python launch.py
```

### Windows

```powershell
# Install Python from https://www.python.org/downloads/
# ⚠️ CHECK "Add Python to PATH" during install!

# Install Node.js LTS from https://nodejs.org/

# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone & launch
git clone https://github.com/YOUR_USERNAME/fullmetal-anatomist.git
cd fullmetal-anatomist
python launch.py
```

### Daily Usage

```bash
cd fullmetal-anatomist
python launch.py
# Browser opens automatically at http://localhost:8765
```

---

## 🏗️ Architecture

```
React 18 + Vite + Tailwind
        │  REST + SSE
FastAPI + SQLModel + SQLite
        │
Pydantic AI (Gemini / OpenAI / Anthropic)
```

| Layer    | Tech                           |
|----------|--------------------------------|
| Frontend | React 18, Vite, Tailwind CSS   |
| Backend  | Python 3.11+, FastAPI          |
| LLM      | Pydantic AI (multi-provider)   |
| Database | SQLite via SQLModel            |
| PDF      | WeasyPrint + Jinja2            |
| Parsing  | PyMuPDF, python-docx           |

---

## 🔐 Security

- API keys are **Fernet-encrypted** at rest using a machine-derived key
- All text processing is **local** — content only leaves your machine to call the LLM API
- No telemetry, no analytics, no cloud storage
- SQLite database is excluded from git via `.gitignore`

---

## 🧪 Running Tests

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pytest tests/ -v
```

---

## 📁 Project Structure

```
fullmetal-anatomist/
├── launch.py              # One-command startup
├── pyproject.toml
├── backend/
│   ├── main.py            # FastAPI app
│   ├── database.py        # SQLModel models
│   ├── provider_manager.py
│   ├── chapter_parser.py  # Chapter boundary detection
│   ├── worksheet_generator.py
│   ├── pdf_renderer.py
│   ├── chat_agent.py
│   ├── file_ingestor.py
│   └── routers/
├── frontend/src/
│   ├── components/        # React components
│   ├── hooks/             # Custom hooks
│   ├── api/client.ts      # Fetch + SSE client
│   └── utils/scoring.ts
└── templates/
    └── worksheet.html     # PDF template
```

---

## 💬 Example Chat Flow

```
You:   [Pastes Robbins Chapter 12]

⚗️:    Got it! Parsed as: Chapter 12: Cardiovascular Pathology
       ~3,200 words across 6 major sections.
       Want a worksheet? Easy / Medium / Hard?

You:   Medium, focus on atherosclerosis

⚗️:    ⚗️ Transmuting... ✨
       Generated 18 fill-in-the-blank questions.
       [View Worksheet] [Download PDF] [Answer Key]

You:   Explain foam cells

⚗️:    Foam cells are lipid-laden macrophages that...
```

---

MIT License — built with ⚗️ and too much caffeine.
