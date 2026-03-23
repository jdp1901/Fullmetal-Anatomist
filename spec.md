# ⚗️ Fullmetal Anatomist

> *"Equivalent Exchange: You give it textbook chapters, it gives you passing grades."*

An AI-powered medical study agent that transmutes dense textbook content into
interactive fill-in-the-blank worksheets. Built for med students who'd rather
be watching anime than re-reading Harrison's for the 47th time.

---

## 🎯 Project Vision

Fullmetal Anatomist is a **self-hosted, local-first study tool** that:

1. Accepts raw textbook content (paste, upload `.txt` / `.pdf` / `.docx`)
2. Uses an LLM to parse chapters, identify key concepts, and generate
   **fill-in-the-blank worksheets** organized by chapter
3. Serves worksheets as **interactive HTML** (fill in on-screen) or
   **downloadable PDF** (print & study old-school)
4. Provides a chat interface to ask follow-up questions about the material
5. Runs entirely on the user's machine — no cloud, no subscriptions,
   just bring your own API key

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                    │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Chat   │  │  Worksheet   │  │   Worksheet   │  │
│  │ Interface │  │   Viewer     │  │   Library     │  │
│  └──────────┘  └──────────────┘  └───────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │ REST + SSE (streaming)
┌────────────────────▼────────────────────────────────┐
│               FastAPI Backend                       │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Agent   │  │  Worksheet   │  │     PDF       │  │
│  │  Core    │  │  Generator   │  │   Renderer    │  │
│  └──────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Provider │  │   Chapter    │  │   File        │  │
│  │ Manager  │  │   Parser     │  │   Ingestor    │  │
│  └──────────┘  └──────────────┘  └───────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                  SQLite (State)                     │
│  chapters │ worksheets │ questions │ settings       │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

| Layer      | Technology                             | Why                                      |
|------------|----------------------------------------|------------------------------------------|
| Frontend   | React 18 + Vite + Tailwind CSS         | Fast, modern, easy to theme              |
| Backend    | Python 3.11+ / FastAPI                 | Async, type-safe, easy to run            |
| LLM        | Pydantic AI (multi-provider)           | Clean provider abstraction               |
| Database   | SQLite via SQLModel                    | Zero config, portable, file-based        |
| PDF        | WeasyPrint or pdfkit                   | HTML→PDF conversion for worksheets       |
| File Parse | PyMuPDF (fitz) + python-docx           | PDF and DOCX text extraction             |
| Runner     | Single `launch.py` script              | One command to start everything          |

---

## 🧬 Data Model

### `Subject`
```
id: int (PK)
name: str              # e.g. "Pathology", "Pharmacology"
created_at: datetime
```

### `Chapter`
```
id: int (PK)
subject_id: int (FK → Subject)
title: str             # e.g. "Chapter 12: Cardiovascular Pathology"
chapter_number: int
raw_content: text      # Original pasted/extracted text
summary: text | null   # LLM-generated summary
created_at: datetime
```

### `Worksheet`
```
id: int (PK)
chapter_id: int (FK → Chapter)
title: str             # e.g. "Ch.12 - Cardiovascular Pathology Worksheet"
difficulty: str        # "easy" | "medium" | "hard"
status: str            # "generating" | "ready" | "error"
created_at: datetime
```

### `Question`
```
id: int (PK)
worksheet_id: int (FK → Worksheet)
order: int             # Display order within worksheet
question_text: str     # The sentence with _____ blanks
answer_text: str       # The correct fill-in answer(s)
section_heading: str   # Subsection grouping within chapter
created_at: datetime
```

### `AppSettings`
```
id: int (PK)
llm_provider: str      # "gemini" | "openai" | "anthropic"
api_key: str           # Encrypted at rest
model_name: str        # e.g. "gemini-2.0-flash", "gpt-4o-mini"
```

---

## 🖥️ Frontend Spec (React)

### Theme: "The Lab" 🧪
- **Color palette**: Deep navy (#0f172a) background, electric teal (#14b8a6)
  accents, white text, subtle molecule/helix SVG patterns
- **Font**: `JetBrains Mono` for worksheet content, `Inter` for UI
- **Vibe**: Clean, clinical, slightly sci-fi — like a futuristic lab notebook
- Subtle alchemy circle watermark on worksheets (on-brand 🔥)

### Pages / Views

#### 1. **Setup / Onboarding** (`/setup`)
- First-run only (redirects here if no API key configured)
- Provider selector dropdown: Gemini / OpenAI / Anthropic
- API key input (masked)
- Model selector (populated based on provider)
- "Test Connection" button
- Save & proceed

#### 2. **Dashboard / Home** (`/`)
- Left sidebar: Subject & chapter tree (collapsible)
- Center: Chat interface with the agent
- Right panel (toggleable): Active worksheet preview
- Top bar: Settings gear, provider badge, dark mode (default dark)

#### 3. **Chat Interface** (main interaction point)
- Streaming message display (SSE from backend)
- User can:
  - Paste textbook content directly into chat
  - Upload files (.txt, .pdf, .docx) via drag-and-drop or button
  - Say things like:
    - *"Generate a worksheet for this chapter"*
    - *"Make it harder" / "Make it easier"*
    - *"Focus on pharmacology terms"*
    - *"Explain this concept to me"*
    - *"Regenerate question 14"*
  - The agent parses intent and routes accordingly

#### 4. **Worksheet Viewer** (`/worksheet/:id`)
- Rendered HTML worksheet with:
  - Title & chapter info header
  - Section headings grouping related questions
  - Fill-in-the-blank questions with text inputs
  - "Check Answers" button (reveals correct answers inline,
    green for correct / red for incorrect)
  - Score summary at bottom
- Action bar:
  - 📥 **Download PDF** (print-ready, blanks only — no answers)
  - 📥 **Download Answer Key PDF** (with answers filled in)
  - 🖨️ **Print** (browser print dialog)
  - 🔄 **Regenerate** (re-run generation)

#### 5. **Worksheet Library** (`/library`)
- Grid/list of all generated worksheets
- Filter by subject, chapter, difficulty, date
- Bulk download as PDF
- Delete / archive worksheets

### Component Hierarchy
```
App
├── SetupWizard
├── Layout
│   ├── Sidebar
│   │   ├── SubjectTree
│   │   └── SubjectTreeItem
│   ├── TopBar
│   │   ├── ProviderBadge
│   │   └── SettingsButton
│   └── MainContent
│       ├── ChatView
│       │   ├── MessageList
│       │   │   ├── UserMessage
│       │   │   ├── AgentMessage
│       │   │   └── WorksheetCard (inline preview)
│       │   ├── ChatInput
│       │   └── FileUploadZone
│       ├── WorksheetViewer
│       │   ├── WorksheetHeader
│       │   ├── QuestionSection
│       │   │   └── FillInBlankQuestion
│       │   ├── ScoreSummary
│       │   └── WorksheetActions
│       └── WorksheetLibrary
│           ├── LibraryFilters
│           └── WorksheetGrid
│               └── WorksheetGridCard
└── SettingsModal
```

---

## ⚙️ Backend Spec (FastAPI)

### API Endpoints

#### Settings
```
GET    /api/settings              → Current provider/model config
PUT    /api/settings              → Update provider, key, model
POST   /api/settings/test         → Test LLM connection
```

#### Subjects & Chapters
```
GET    /api/subjects              → List all subjects
POST   /api/subjects              → Create subject
GET    /api/subjects/:id/chapters → List chapters for subject
POST   /api/chapters              → Create chapter (with raw content)
POST   /api/chapters/upload       → Upload file → extract text → create chapter
GET    /api/chapters/:id          → Get chapter detail
DELETE /api/chapters/:id          → Delete chapter
```

#### Worksheets
```
POST   /api/worksheets/generate   → Generate worksheet from chapter
                                     Body: { chapter_id, difficulty }
GET    /api/worksheets             → List all worksheets
GET    /api/worksheets/:id         → Get worksheet with questions
GET    /api/worksheets/:id/pdf     → Download worksheet as PDF
GET    /api/worksheets/:id/pdf?answers=true → Download answer key
GET    /api/worksheets/:id/html    → Get interactive HTML version
DELETE /api/worksheets/:id         → Delete worksheet
POST   /api/worksheets/:id/regenerate → Regenerate worksheet
```

#### Chat
```
POST   /api/chat                  → Send message (SSE streaming response)
                                     Body: { message, chapter_id? }
```

### Core Modules

#### `provider_manager.py` (~120 lines)
- Abstracts LLM provider switching via Pydantic AI
- Detects provider from API key format if not explicitly set:
  - Starts with `AIza` → Gemini
  - Starts with `sk-` → OpenAI
  - Starts with `sk-ant-` → Anthropic
- Exposes `get_agent()` → returns configured Pydantic AI Agent
- Handles model listing per provider

#### `chapter_parser.py` (~150 lines)
- Text chunking and chapter boundary detection
- Handles raw pasted text (looks for "Chapter X" patterns)
- PDF extraction via PyMuPDF
- DOCX extraction via python-docx
- Returns structured `Chapter` objects

#### `worksheet_generator.py` (~200 lines)
- Core LLM prompting logic
- Takes chapter content + difficulty → structured worksheet
- Prompt engineering for fill-in-the-blank generation:
  - Identifies key terms, definitions, processes, drug names,
    anatomical structures, pathways, etc.
  - Groups questions by section/topic within the chapter
  - Adjusts density and obscurity based on difficulty
- Uses Pydantic AI structured output for reliable JSON responses
- Output schema:
  ```python
  class GeneratedWorksheet(BaseModel):
      title: str
      sections: list[WorksheetSection]

  class WorksheetSection(BaseModel):
      heading: str
      questions: list[GeneratedQuestion]

  class GeneratedQuestion(BaseModel):
      question_text: str   # "The _____ nerve innervates the..."
      answer: str           # "vagus"
      explanation: str      # Brief context for answer key
  ```

#### `pdf_renderer.py` (~100 lines)
- Takes worksheet data → generates styled PDF
- Two modes: blank (for printing) and answer key
- Uses WeasyPrint with a medical-themed CSS template
- Includes header with subject, chapter, date, difficulty badge

#### `chat_agent.py` (~180 lines)
- Pydantic AI agent with tools for:
  - `create_chapter(content, title, subject)` — parse and store content
  - `generate_worksheet(chapter_id, difficulty)` — trigger generation
  - `explain_concept(concept, chapter_id)` — explain from context
  - `adjust_worksheet(worksheet_id, instruction)` — modify existing
- System prompt establishes the agent as a medical study assistant
- Streams responses via SSE

#### `file_ingestor.py` (~80 lines)
- Handles multipart file uploads
- Routes to appropriate parser (PDF, DOCX, TXT)
- Returns extracted text + detected chapter boundaries

#### `database.py` (~80 lines)
- SQLModel setup, engine creation, session management
- Auto-creates tables on first run
- All models defined here

---

## 📁 Project Structure

```
fullmetal-anatomist/
├── README.md                    # Install & usage instructions
├── SPEC.md                      # This file
├── LICENSE                      # MIT
├── .gitignore
├── pyproject.toml               # Python project config (uv)
├── launch.py                    # One-command launcher script
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, lifespan
│   ├── config.py                # Env/settings management
│   ├── database.py              # SQLModel models + engine
│   ├── provider_manager.py      # Multi-provider LLM abstraction
│   ├── chapter_parser.py        # Text extraction & chunking
│   ├── worksheet_generator.py   # LLM-powered question generation
│   ├── pdf_renderer.py          # HTML → PDF conversion
│   ├── chat_agent.py            # Pydantic AI chat agent
│   ├── file_ingestor.py         # File upload handling
│   └── routers/
│       ├── __init__.py
│       ├── settings.py          # /api/settings routes
│       ├── subjects.py          # /api/subjects routes
│       ├── chapters.py          # /api/chapters routes
│       ├── worksheets.py        # /api/worksheets routes
│       └── chat.py              # /api/chat SSE route
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── public/
│   │   ├── favicon.svg          # Alchemy circle + stethoscope
│   │   └── alchemy-watermark.svg
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css             # Tailwind + custom theme
│       ├── api/
│       │   └── client.ts         # Fetch wrapper + SSE handler
│       ├── components/
│       │   ├── Layout.tsx
│       │   ├── Sidebar.tsx
│       │   ├── TopBar.tsx
│       │   ├── ChatView.tsx
│       │   ├── ChatInput.tsx
│       │   ├── MessageList.tsx
│       │   ├── FileUploadZone.tsx
│       │   ├── WorksheetViewer.tsx
│       │   ├── FillInBlankQuestion.tsx
│       │   ├── WorksheetActions.tsx
│       │   ├── WorksheetLibrary.tsx
│       │   ├── SetupWizard.tsx
│       │   └── SettingsModal.tsx
│       ├── hooks/
│       │   ├── useChat.ts
│       │   ├── useWorksheet.ts
│       │   └── useSettings.ts
│       ├── types/
│       │   └── index.ts
│       └── utils/
│           └── scoring.ts
│
├── templates/
│   ├── worksheet.html           # Jinja2 template for PDF rendering
│   └── worksheet.css            # Print-optimized styles
│
└── tests/
    ├── test_chapter_parser.py
    ├── test_worksheet_generator.py
    ├── test_pdf_renderer.py
    └── test_api.py
```

---

## 🚀 Launch Flow

### `launch.py` — The One Script To Rule Them All

This is the magic. Med students run ONE command and everything works.

```python
# Pseudocode for launch.py
def main():
    print("⚗️ Fullmetal Anatomist — Starting up...")

    # 1. Check Python version (3.11+)
    # 2. Check if uv is installed, if not: install it
    # 3. Check if node is installed, if not: guide user
    # 4. Create/sync venv with uv
    # 5. Install Python deps: `uv sync`
    # 6. Install frontend deps: `npm install` (in frontend/)
    # 7. Build frontend: `npm run build` (in frontend/)
    # 8. Start FastAPI server (serves built frontend as static)
    # 9. Open browser to http://localhost:8765
    # 10. On first run → SetupWizard for API key
```

**Port**: `8765` (easy to remember: "8765 let's study and stay alive")

---

## 🧪 LLM Prompt Strategy

### Worksheet Generation Prompt (simplified)
```
You are a medical education expert creating fill-in-the-blank
study worksheets.

Given the following textbook chapter content, create a comprehensive
worksheet that tests key concepts. Rules:

1. Group questions by section/topic within the chapter
2. Each question should be a complete sentence with ONE key term
   replaced by a blank ("_____")
3. Prioritize: definitions, mechanisms, drug names, anatomical
   structures, clinical correlations, diagnostic criteria
4. Difficulty: {difficulty}
   - Easy: Basic definitions and straightforward recall
   - Medium: Relationships, mechanisms, clinical applications
   - Hard: Edge cases, differential diagnosis, multi-step reasoning
5. Aim for {target_count} questions covering all major topics
6. Include brief explanations for the answer key

Chapter content:
{chapter_content}
```

### Chapter Boundary Detection Prompt
```
Analyze this text and identify chapter/section boundaries.
Return the title and starting position of each chapter or
major section. Look for patterns like:
- "Chapter X: Title"
- Numbered sections (1.0, 2.0)
- Major heading patterns
- Topic shifts
```

---

## 📋 Implementation Phases

### Phase 1: Foundation (MVP) 🏗️
- [ ] Project scaffolding (pyproject.toml, package.json, configs)
- [ ] SQLite database setup with SQLModel
- [ ] Provider manager (Gemini + OpenAI + Anthropic via Pydantic AI)
- [ ] Settings API (save/load/test API key)
- [ ] Basic FastAPI app with CORS
- [ ] React app with Vite + Tailwind
- [ ] Setup wizard (API key onboarding)
- [ ] Basic layout shell (sidebar, topbar, main content)

### Phase 2: Core Engine 🧬
- [ ] Chapter parser (text extraction from paste / .txt)
- [ ] File ingestor (PDF + DOCX upload)
- [ ] Worksheet generator (LLM-powered fill-in-blank creation)
- [ ] Subjects & Chapters CRUD API
- [ ] Worksheet generation API
- [ ] Chat agent with Pydantic AI (streaming SSE)
- [ ] Chat UI with streaming messages

### Phase 3: Worksheet Experience 📝
- [ ] Interactive worksheet viewer (HTML fill-in-the-blank)
- [ ] Answer checking + scoring
- [ ] PDF generation (blank + answer key)
- [ ] Download buttons
- [ ] Worksheet library view
- [ ] Difficulty selector

### Phase 4: Polish & DX ✨
- [ ] launch.py one-command startup
- [ ] README with dead-simple install instructions
- [ ] Windows + macOS install guides with screenshots
- [ ] Error handling & user-friendly error messages
- [ ] Loading states & skeleton screens
- [ ] Print-optimized CSS for worksheets
- [ ] Alchemy circle watermark SVGs

### Phase 5: Nice-to-Haves 🌟
- [ ] Spaced repetition tracking (which questions you got wrong)
- [ ] "Explain this" button on each question
- [ ] Bulk chapter import (entire textbook PDF → auto-split)
- [ ] Worksheet sharing (export as standalone HTML)
- [ ] Study session timer
- [ ] Progress tracking per subject

---

## 🖨️ Worksheet PDF Layout

```
┌─────────────────────────────────────────┐
│  ⚗️ FULLMETAL ANATOMIST                │
│  Subject: Pathology                     │
│  Chapter 12: Cardiovascular Pathology   │
│  Difficulty: ██░░ Medium                │
│  Date: 2026-03-23                       │
├─────────────────────────────────────────┤
│                                         │
│  SECTION: Atherosclerosis               │
│  ─────────────────────────              │
│                                         │
│  1. The __________ is the most common   │
│     cause of coronary artery disease.   │
│                                         │
│  2. Foam cells are derived from         │
│     __________ that accumulate lipids   │
│     in the vessel intima.               │
│                                         │
│  SECTION: Valvular Heart Disease        │
│  ─────────────────────────              │
│                                         │
│  3. Rheumatic heart disease most        │
│     commonly affects the __________     │
│     valve.                              │
│                                         │
│  ...                                    │
│                                         │
├─────────────────────────────────────────┤
│  Score: ____ / 25    Name: ___________  │
└─────────────────────────────────────────┘
```

---

## 💻 Installation Instructions (for README)

### Prerequisites
- **Python 3.11+** (we'll help you install it)
- **Node.js 18+** (we'll help you install it)
- An API key from ONE of:
  - [Google Gemini](https://aistudio.google.com/apikey) (recommended,
    free tier available)
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic](https://console.anthropic.com/)

### macOS Install
```bash
# 1. Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python & Node
brew install python@3.12 node

# 3. Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Clone the repo
git clone https://github.com/YOUR_USERNAME/fullmetal-anatomist.git
cd fullmetal-anatomist

# 5. Launch! (this handles everything else)
python launch.py
```

### Windows Install
```powershell
# 1. Install Python from https://www.python.org/downloads/
#    ⚠️ CHECK "Add Python to PATH" during install!

# 2. Install Node.js from https://nodejs.org/
#    Use the LTS version

# 3. Install uv
powershell -ExecutionPolicy ByPass -c "
  irm https://astral.sh/uv/install.ps1 | iex
"

# 4. Clone the repo (or download ZIP from GitHub)
git clone https://github.com/YOUR_USERNAME/fullmetal-anatomist.git
cd fullmetal-anatomist

# 5. Launch!
python launch.py
```

### Daily Usage
```bash
# Just run this every time you want to study:
cd fullmetal-anatomist
python launch.py

# That's it. Browser opens automatically.
# Paste your textbook content → get worksheets → ace your exam.
```

---

## 🔐 Security Notes

- API keys stored in local SQLite, encrypted with Fernet
  (key derived from machine-specific identifier)
- All processing happens locally — textbook content never leaves
  your machine except to the LLM provider you choose
- No telemetry, no analytics, no tracking
- SQLite DB excluded from git via .gitignore

---

## 🎨 UI Mockup — Chat Flow Example

```
User: [Pastes 3 pages of Robbins Pathology Chapter 12]

Agent: ⚗️ Got it! I've parsed this as:
       📖 Chapter 12: Cardiovascular Pathology
       📊 ~3,200 words across 6 major sections

       I've saved this under Subject: Pathology.
       Want me to generate a worksheet? I can do:
       • Easy (definitions & basic recall)
       • Medium (mechanisms & clinical correlations)
       • Hard (differentials & edge cases)

User: Medium difficulty, focus on the atherosclerosis section

Agent: ⚗️ Transmuting... ✨
       Generated 18 fill-in-the-blank questions
       focused on atherosclerosis.

       [📋 View Worksheet]  [📥 Download PDF]  [📥 Answer Key]

User: Make question 7 harder

Agent: ⚗️ Updated! Question 7 now reads:
       "The oxidation of _____ within the subendothelial
       space triggers macrophage recruitment via _____
       receptor-mediated endocytosis."
       (Answers: LDL, scavenger)
```

---

## 🐕 Agent Builder Notes

This spec is designed so that an AI coding agent can build the entire
project from scratch by following the phases sequentially. Each phase
is self-contained and testable. Key principles:

1. **Start with the backend** — get the data model and API working first
2. **Use Pydantic AI** for all LLM interactions (clean provider switching)
3. **Keep files under 600 lines** — split into modules early
4. **Test API endpoints with curl** before building the frontend
5. **Build frontend components bottom-up** — start with small pieces,
   compose into pages
6. **launch.py is the last thing** — once everything works individually,
   wire it together

The agent should be able to `cat SPEC.md` and build this thing
phase by phase. Let's transmute some knowledge. ⚗️
