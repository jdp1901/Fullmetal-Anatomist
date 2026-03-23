"""Chat agent with Pydantic AI — streaming SSE responses."""

from __future__ import annotations

import json
from typing import AsyncIterator

from pydantic_ai import Agent
from sqlmodel import Session

from backend.database import Chapter, Subject, get_session
from backend.provider_manager import get_agent
from backend.worksheet_generator import generate_worksheet

CHAT_SYSTEM_PROMPT = """You are the Fullmetal Anatomist ⚗️ — a brilliant, slightly sarcastic 
medical study assistant. You help med students by:

1. Accepting pasted textbook content and saving it as chapters
2. Generating fill-in-the-blank worksheets from chapters
3. Explaining medical concepts clearly and concisely
4. Adjusting worksheet difficulty on request

You speak with confidence and a touch of alchemy-themed flair. Keep responses 
concise but thorough. When a user pastes textbook content, acknowledge it and 
offer to generate a worksheet.

IMPORTANT: When the user pastes large blocks of medical text, treat it as 
textbook content to be saved as a chapter. Ask for the subject name if not 
obvious.

You are NOT a general-purpose chatbot. Stay focused on medical study assistance."""


async def stream_chat(
    message: str,
    chapter_id: int | None = None,
    session: Session | None = None,
) -> AsyncIterator[str]:
    """Stream a chat response as SSE data lines."""
    own_session = session is None
    if own_session:
        session = next(get_session())

    context = ""
    if chapter_id:
        chapter = session.get(Chapter, chapter_id)
        if chapter:
            context = (
                f"\n\nCurrent chapter context: {chapter.title}\n"
                f"Content preview: {chapter.raw_content[:5000]}\n"
            )

    agent = get_agent(
        system_prompt=CHAT_SYSTEM_PROMPT + context,
        session=session,
    )

    async with agent.run_stream(message) as result:
        async for chunk in result.stream_text(delta=True):
            yield f"data: {json.dumps({'type': 'delta', 'content': chunk})}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"
