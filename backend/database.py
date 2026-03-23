"""SQLModel database setup — models, engine, and session management."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

from backend.config import DB_PATH

# ── Models ──────────────────────────────────────────────────────────────────


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    chapters: list["Chapter"] = Relationship(back_populates="subject")


class Chapter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    title: str
    chapter_number: int = 0
    raw_content: str = ""
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    subject: Optional[Subject] = Relationship(back_populates="chapters")
    worksheets: list["Worksheet"] = Relationship(back_populates="chapter")


class Worksheet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: int = Field(foreign_key="chapter.id")
    title: str
    difficulty: str = "medium"  # easy | medium | hard
    status: str = "generating"  # generating | ready | error
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    chapter: Optional[Chapter] = Relationship(back_populates="worksheets")
    questions: list["Question"] = Relationship(back_populates="worksheet")


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worksheet_id: int = Field(foreign_key="worksheet.id")
    order: int = 0
    question_text: str
    answer_text: str
    explanation: str = ""
    section_heading: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    worksheet: Optional[Worksheet] = Relationship(back_populates="questions")


class AppSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    llm_provider: str = "gemini"  # gemini | openai | anthropic
    api_key_encrypted: str = ""  # Fernet-encrypted
    model_name: str = "gemini-2.0-flash"


# ── Engine & Session ────────────────────────────────────────────────────────

_engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def init_db() -> None:
    """Create all tables if they don't exist."""
    SQLModel.metadata.create_all(_engine)


def get_session():
    """FastAPI dependency — yields a DB session."""
    with Session(_engine) as session:
        yield session
