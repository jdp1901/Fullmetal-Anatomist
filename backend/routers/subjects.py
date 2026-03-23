"""Subject API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.database import Chapter, Subject, get_session

router = APIRouter(prefix="/api/subjects", tags=["subjects"])


class SubjectCreate(BaseModel):
    name: str


@router.get("")
def list_subjects(session: Session = Depends(get_session)):
    subjects = session.exec(select(Subject)).all()
    result = []
    for s in subjects:
        chapters = session.exec(
            select(Chapter).where(Chapter.subject_id == s.id)
        ).all()
        result.append({
            "id": s.id,
            "name": s.name,
            "created_at": s.created_at.isoformat(),
            "chapters": [
                {"id": c.id, "title": c.title, "chapter_number": c.chapter_number}
                for c in chapters
            ],
        })
    return result


@router.post("", status_code=201)
def create_subject(body: SubjectCreate, session: Session = Depends(get_session)):
    subject = Subject(name=body.name)
    session.add(subject)
    session.commit()
    session.refresh(subject)
    return subject


@router.get("/{subject_id}/chapters")
def list_chapters(subject_id: int, session: Session = Depends(get_session)):
    subject = session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(404, "Subject not found")
    chapters = session.exec(
        select(Chapter).where(Chapter.subject_id == subject_id)
    ).all()
    return chapters
