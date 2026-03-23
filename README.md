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
- 📥 **PDF export** — blank worksheet + answer key for printing
- 💬 **Chat interface** — streaming AI assistant for follow-up questions
- 🔒 **Local-first** — your textbooks stay on your machine
- 🔑 **Multi-provider** — Gemini, OpenAI, or Anthropic

---

## 📋 Before You Start — What You'll Need

1. **An API key** from any ONE of these providers:
   - 🌟 [Google Gemini](https://aistudio.google.com/apikey) — **recommended,
     has a free tier!**
   - [OpenAI](https://platform.openai.com/api-keys)
   - [Anthropic](https://console.anthropic.com/)
2. **Python 3.11 or newer**
3. **Node.js 18 or newer**
4. **uv** (a fast Python package manager)
5. **Git** (to clone the repo)

Don't have these installed? Follow the step-by-step guide for your OS below.

---

## 🪟 Windows Setup (Step-by-Step)

If you already have Python, Node, uv, and Git installed, skip to
**"Launch the App"** at the bottom of this section.

### Step 1 — Install Python

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python 3.x.x"** button
3. Run the installer
4. **❗❗❗ CRITICAL: Check the box that says
   "Add Python to PATH" at the bottom of the first screen ❗❗❗**
5. Click "Install Now" and wait for it to finish

Verify it worked — open **Command Prompt** (search "cmd" in the Start menu)
and type:

```cmd
python --version
```

You should see something like `Python 3.12.x`. If you see an error or it
opens the Microsoft Store, Python wasn't added to PATH — re-run the
installer and check the PATH box.

### Step 2 — Install Node.js

1. Go to **https://nodejs.org/**
2. Download the **LTS** version (the green button)
3. Run the installer, click Next through everything (defaults are fine)

Verify:

```cmd
node --version
```

You should see `v20.x.x` or `v22.x.x`.

### Step 3 — Install Git

1. Go to **https://git-scm.com/download/win**
2. Download and run the installer (defaults are fine)
3. When it asks about the default editor, pick whatever you like
   (Notepad is fine)

Verify:

```cmd
git --version
```

### Step 4 — Install uv

Open **PowerShell** (search "PowerShell" in the Start menu) and paste:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Close and re-open your terminal** after installing so it's on your PATH.

Verify:

```cmd
uv --version
```

### Step 5 — Clone the Project & Launch the App

Open **Command Prompt** or **PowerShell** and run:

```cmd
git clone https://github.com/YOUR_USERNAME/fullmetal-anatomist.git
cd fullmetal-anatomist
python launch.py
```

That's it! The script will:
1. Create a Python virtual environment
2. Install all Python dependencies
3. Install frontend dependencies
4. Build the frontend
5. Start the server
6. Open your browser to **http://localhost:8765**

On first run, you'll see a **Setup Wizard** — pick your LLM provider,
paste your API key, and click "Save & Start".

### Daily Usage (Windows)

```cmd
cd fullmetal-anatomist
python launch.py
```

That's the only command. Every time. Browser opens automatically.

To stop the server, press **Ctrl+C** in the terminal.

---

## 🍎 macOS Setup (Step-by-Step)

### Option A — Quick install (if you have Homebrew)

```bash
brew install python@3.12 node git
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone https://github.com/YOUR_USERNAME/fullmetal-anatomist.git
cd fullmetal-anatomist
python3 launch.py
```

### Option B — Don't have Homebrew?

1. **Install Homebrew** (the macOS package manager):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Then follow Option A above.

### Daily Usage (macOS)

```bash
cd fullmetal-anatomist
python3 launch.py
```

---

## 🖥️ How to Use the App

### 1. First Run — Setup Wizard

When the browser opens, you'll see the **Setup Wizard**:

- **Pick a provider**: Gemini (recommended), OpenAI, or Anthropic
- **Paste your API key**: get one from the links above
- **Pick a model**: the default is fine to start
- Click **"Test Connection"** to make sure it works
- Click **"Save & Start"**

### 2. Study Flow

1. **Paste textbook content** into the chat, or **drag & drop**
   a `.txt`, `.pdf`, or `.docx` file
2. The agent will parse it and offer to generate a worksheet
3. Choose difficulty: **Easy** (definitions), **Medium**
   (mechanisms & clinical), or **Hard** (differentials & edge cases)
4. Fill in the blanks on screen, then click **"Check Answers"**
5. Download a **PDF** to print, or download the **Answer Key**

### 3. Worksheet Library

Click **📚 Library** in the top bar to see all your generated worksheets.
Filter by name, re-download PDFs, or delete old ones.

---

## 🏗️ Architecture

```
React 18 + Vite + Tailwind CSS
        │  REST + SSE (streaming)
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
- All text processing is **local** — content only leaves your machine
  to call the LLM API you chose
- No telemetry, no analytics, no cloud storage
- SQLite database is excluded from git via `.gitignore`

---

## 🚨 Troubleshooting

### "python is not recognized" (Windows)

Python wasn't added to PATH during install. Either:
- Re-run the Python installer and check **"Add Python to PATH"**
- Or use the full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`

### "npm install" hangs forever

You're probably behind a corporate proxy. The launch script handles this
automatically with Walmart's proxy settings. If you're not on Walmart's
network, remove the proxy env vars in `launch.py`.

### "uv not found"

Close your terminal and re-open it after installing uv. The installer
adds uv to your PATH but existing terminals won't see it.

### WeasyPrint errors on Windows

WeasyPrint needs GTK libraries. If PDF export fails, install the
GTK3 runtime:
1. Go to **https://github.com/nickvdp/gtk-for-windows** and
   download `gtk3-runtime-x.x.x.exe` (or similar)
2. Install it, restart the server

Alternatively, the app works fine without PDF export — you can still
use the interactive on-screen worksheets.

### Port 8765 is already in use

Another instance is probably running. Close it first, or set a
custom port:

```cmd
set FMA_PORT=9999
python launch.py
```

---

## 🧪 Running Tests (for developers)

```bash
# macOS / Linux
source venv/bin/activate
pytest tests/ -v

# Windows
venv\Scripts\activate
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
│   ├── components/
│   ├── hooks/
│   ├── api/client.ts
│   └── utils/scoring.ts
└── templates/
    └── worksheet.html     # PDF template
```

---

## 💬 Example Chat Flow

```
You:   [Pastes 3 pages from Robbins Pathology Chapter 12]

⚗️:    Got it! I've parsed this as:
       📖 Chapter 12: Cardiovascular Pathology
       ~3,200 words across 6 major sections.

       Want me to generate a worksheet?
       • Easy (definitions & basic recall)
       • Medium (mechanisms & clinical correlations)
       • Hard (differentials & edge cases)

You:   Medium, focus on atherosclerosis

⚗️:    ⚗️ Transmuting... ✨
       Generated 18 fill-in-the-blank questions.
       [📋 View Worksheet]  [📥 Download PDF]  [📥 Answer Key]

You:   Explain foam cells

⚗️:    Foam cells are lipid-laden macrophages that accumulate
       oxidized LDL in the subendothelial space...
```

---

MIT License — built with ⚗️ and too much caffeine.
