"""Worksheet API routes."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.database import Chapter, Question, Worksheet, get_session
from backend.worksheet_generator import generate_worksheet

router = APIRouter(prefix="/api/worksheets", tags=["worksheets"])


class WorksheetGenerate(BaseModel):
    chapter_id: int
    difficulty: str = "medium"


@router.post("/generate", status_code=201)
async def generate(body: WorksheetGenerate, session: Session = Depends(get_session)):
    chapter = session.get(Chapter, body.chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")
    worksheet = await generate_worksheet(
        chapter_id=body.chapter_id,
        difficulty=body.difficulty,
        session=session,
    )
    return {"id": worksheet.id, "title": worksheet.title, "status": worksheet.status}


@router.get("")
def list_worksheets(session: Session = Depends(get_session)):
    worksheets = session.exec(select(Worksheet)).all()
    results = []
    for w in worksheets:
        chapter = session.get(Chapter, w.chapter_id)
        q_count = len(
            session.exec(
                select(Question).where(Question.worksheet_id == w.id)
            ).all()
        )
        results.append({
            "id": w.id,
            "title": w.title,
            "difficulty": w.difficulty,
            "status": w.status,
            "question_count": q_count,
            "chapter_title": chapter.title if chapter else None,
            "created_at": w.created_at.isoformat(),
        })
    return results


@router.get("/{worksheet_id}")
def get_worksheet(worksheet_id: int, session: Session = Depends(get_session)):
    worksheet = session.get(Worksheet, worksheet_id)
    if not worksheet:
        raise HTTPException(404, "Worksheet not found")
    questions = session.exec(
        select(Question)
        .where(Question.worksheet_id == worksheet_id)
        .order_by(Question.order)
    ).all()
    chapter = session.get(Chapter, worksheet.chapter_id)
    return {
        "id": worksheet.id,
        "title": worksheet.title,
        "difficulty": worksheet.difficulty,
        "status": worksheet.status,
        "created_at": worksheet.created_at.isoformat(),
        "chapter_title": chapter.title if chapter else None,
        "questions": [
            {
                "id": q.id,
                "order": q.order,
                "question_text": q.question_text,
                "answer_text": q.answer_text,
                "explanation": q.explanation,
                "section_heading": q.section_heading,
            }
            for q in questions
        ],
    }


@router.delete("/{worksheet_id}")
def delete_worksheet(worksheet_id: int, session: Session = Depends(get_session)):
    worksheet = session.get(Worksheet, worksheet_id)
    if not worksheet:
        raise HTTPException(404, "Worksheet not found")
    # Delete questions first
    questions = session.exec(
        select(Question).where(Question.worksheet_id == worksheet_id)
    ).all()
    for q in questions:
        session.delete(q)
    session.delete(worksheet)
    session.commit()
    return {"ok": True}


@router.post("/{worksheet_id}/regenerate", status_code=201)
async def regenerate(
    worksheet_id: int, session: Session = Depends(get_session)
):
    worksheet = session.get(Worksheet, worksheet_id)
    if not worksheet:
        raise HTTPException(404, "Worksheet not found")
    # Delete old questions
    old_qs = session.exec(
        select(Question).where(Question.worksheet_id == worksheet_id)
    ).all()
    for q in old_qs:
        session.delete(q)
    session.delete(worksheet)
    session.commit()
    # Regenerate
    new_ws = await generate_worksheet(
        chapter_id=worksheet.chapter_id,
        difficulty=worksheet.difficulty,
        session=session,
    )
    return {"id": new_ws.id, "title": new_ws.title, "status": new_ws.status}


@router.get("/{worksheet_id}/pdf")
def download_pdf(
    worksheet_id: int,
    answers: bool = False,
    session: Session = Depends(get_session),
):
    from backend.pdf_renderer import render_worksheet_pdf

    worksheet = session.get(Worksheet, worksheet_id)
    if not worksheet:
        raise HTTPException(404, "Worksheet not found")
    questions = session.exec(
        select(Question)
        .where(Question.worksheet_id == worksheet_id)
        .order_by(Question.order)
    ).all()
    chapter = session.get(Chapter, worksheet.chapter_id)

    pdf_bytes = render_worksheet_pdf(worksheet, questions, chapter, show_answers=answers)

    filename = f"{worksheet.title.replace(' ', '_')}"
    if answers:
        filename += "_ANSWER_KEY"
    filename += ".pdf"

    from fastapi.responses import Response

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
