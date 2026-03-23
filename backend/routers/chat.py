"""Chat SSE route."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from sse_starlette.sse import EventSourceResponse

from backend.chat_agent import stream_chat
from backend.database import get_session

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str
    chapter_id: int | None = None


@router.post("")
async def chat(body: ChatMessage, session: Session = Depends(get_session)):
    return EventSourceResponse(
        stream_chat(
            message=body.message,
            chapter_id=body.chapter_id,
            session=session,
        )
    )
