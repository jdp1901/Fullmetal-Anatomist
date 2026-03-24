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
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"stream_chat called with message: {message[:50]}...")
    
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

    try:
        agent = get_agent(
            system_prompt=CHAT_SYSTEM_PROMPT + context,
            session=session,
        )
        logger.info("Agent created successfully")

        async with agent.run_stream(message) as result:
            logger.info("Entering stream loop")
            chunk_count = 0
            async for chunk in result.stream_text(delta=True):
                chunk_count += 1
                yield f"data: {json.dumps({'type': 'delta', 'content': chunk})}\n\n"
            logger.info(f"Stream completed with {chunk_count} chunks")

        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    except Exception as e:
        logger.error(f"Error in stream_chat: {e}", exc_info=True)
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        raise
