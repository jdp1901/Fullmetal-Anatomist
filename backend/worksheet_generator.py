"""Worksheet generation via LLM — fill-in-the-blank question creation."""

from __future__ import annotations

from pydantic import BaseModel
from pydantic_ai import Agent
from sqlmodel import Session

from backend.database import Chapter, Question, Worksheet, get_session
from backend.provider_manager import get_agent


# ── Structured output schemas ───────────────────────────────────────────


class GeneratedQuestion(BaseModel):
    question_text: str  # Sentence with _____ blanks
    answer: str  # Correct fill-in
    explanation: str  # Brief context


class WorksheetSection(BaseModel):
    heading: str
    questions: list[GeneratedQuestion]


class GeneratedWorksheet(BaseModel):
    title: str
    sections: list[WorksheetSection]


# ── Prompt template ───────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert medical educator specializing in board exam 
preparation (USMLE/COMLEX). You create comprehensive fill-in-the-blank study 
worksheets from textbook content.

Rules:
1. Group questions by section/topic within the chapter.
2. Each question must be a complete sentence with ONE key term replaced by 
   "_____" (five underscores).
3. Prioritize: definitions, mechanisms, drug names, anatomical structures, 
   clinical correlations, diagnostic criteria, and pathways.
4. Include a brief explanation for each answer.
5. Cover ALL major topics exhaustively.
6. Use precise, high-yield medical terminology."""

DIFFICULTY_GUIDE = {
    "easy": "Focus on basic definitions and straightforward recall. "
    "Aim for 40-50 questions.",
    "medium": "Include relationships, mechanisms, and clinical applications. "
    " 60-70 questions.",
    "hard": "Cover edge cases, differential diagnosis, and multi-step reasoning. "
    "Aim for 70-80+ questions.",
}


# ── Generator ─────────────────────────────────────────────────────


async def generate_worksheet(
    chapter_id: int,
    difficulty: str = "medium",
    session: Session | None = None,
) -> Worksheet:
    """Generate a fill-in-the-blank worksheet for a chapter."""
    own_session = session is None
    if own_session:
        session = next(get_session())

    chapter = session.get(Chapter, chapter_id)
    if not chapter:
        raise ValueError(f"Chapter {chapter_id} not found")

    # Create worksheet record (status=generating)
    worksheet = Worksheet(
        chapter_id=chapter_id,
        title=f"{chapter.title} — Worksheet",
        difficulty=difficulty,
        status="generating",
    )
    session.add(worksheet)
    session.commit()
    session.refresh(worksheet)

    try:
        agent: Agent = get_agent(
            system_prompt=SYSTEM_PROMPT,
            result_type=GeneratedWorksheet,
            session=session,
        )

        user_prompt = (
            f"Difficulty: {difficulty}\n"
            f"{DIFFICULTY_GUIDE.get(difficulty, DIFFICULTY_GUIDE['medium'])}\n\n"
            f"Chapter content:\n{chapter.raw_content[:30000]}"
        )

        result = await agent.run(user_prompt)
        generated: GeneratedWorksheet = result.data

        # Persist questions
        order = 1
        for section in generated.sections:
            for q in section.questions:
                question = Question(
                    worksheet_id=worksheet.id,
                    order=order,
                    question_text=q.question_text,
                    answer_text=q.answer,
                    explanation=q.explanation,
                    section_heading=section.heading,
                )
                session.add(question)
                order += 1

        worksheet.title = generated.title or worksheet.title
        worksheet.status = "ready"
        session.commit()
        session.refresh(worksheet)

    except Exception as e:
        worksheet.status = "error"
        session.commit()
        raise e

    return worksheet
