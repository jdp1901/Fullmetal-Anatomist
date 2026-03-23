"""Chapter API routes."""

import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.database import Chapter, Subject, get_session
from backend.file_ingestor import extract_text

router = APIRouter(prefix="/api/chapters", tags=["chapters"])


class ChapterCreate(BaseModel):
    subject_id: int
    title: str
    chapter_number: int = 0
    raw_content: str


@router.post("", status_code=201)
def create_chapter(body: ChapterCreate, session: Session = Depends(get_session)):
    subject = session.get(Subject, body.subject_id)
    if not subject:
        raise HTTPException(404, "Subject not found")
    chapter = Chapter(**body.model_dump())
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


@router.post("/upload", status_code=201)
async def upload_chapter(
    file: UploadFile = File(...),
    subject_id: int = Form(...),
    title: str = Form(""),
    chapter_number: int = Form(0),
    session: Session = Depends(get_session),
):
    subject = session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(404, "Subject not found")

    suffix = Path(file.filename or "upload.txt").suffix.lower()
    if suffix not in (".txt", ".pdf", ".docx"):
        raise HTTPException(400, "Unsupported file type. Use .txt, .pdf, or .docx")

    # Save to temp file and extract
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        text = extract_text(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    if not title:
        title = file.filename or "Untitled Chapter"

    chapter = Chapter(
        subject_id=subject_id,
        title=title,
        chapter_number=chapter_number,
        raw_content=text,
    )
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


@router.get("/{chapter_id}")
def get_chapter(chapter_id: int, session: Session = Depends(get_session)):
    chapter = session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")
    return chapter


@router.delete("/{chapter_id}")
def delete_chapter(chapter_id: int, session: Session = Depends(get_session)):
    chapter = session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")
    session.delete(chapter)
    session.commit()
    return {"ok": True}
