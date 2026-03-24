"""Settings API routes."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.database import AppSettings, get_session
from backend.encryption import decrypt_key, encrypt_key
from backend.provider_manager import (
    DEFAULT_MODELS,
    MODEL_OPTIONS,
    detect_provider,
    test_connection,
)

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingsOut(BaseModel):
    llm_provider: str
    model_name: str
    has_api_key: bool
    api_key: str | None = None
    model_options: dict[str, list[str]] = MODEL_OPTIONS


class SettingsIn(BaseModel):
    llm_provider: str | None = None
    api_key: str | None = None
    model_name: str | None = None


@router.get("", response_model=SettingsOut)
def get_settings(session: Session = Depends(get_session)):
    row = session.exec(select(AppSettings)).first()
    if not row:
        return SettingsOut(llm_provider="gemini", model_name="gemini-2.0-flash", has_api_key=False)
    return SettingsOut(
        llm_provider=row.llm_provider,
        model_name=row.model_name,
        has_api_key=bool(row.api_key_encrypted),
        api_key=decrypt_key(row.api_key_encrypted) if row.api_key_encrypted else None,
    )


@router.put("", response_model=SettingsOut)
def update_settings(body: SettingsIn, session: Session = Depends(get_session)):
    row = session.exec(select(AppSettings)).first()
    if not row:
        row = AppSettings()
        session.add(row)

    if body.api_key:
        row.api_key_encrypted = encrypt_key(body.api_key)
        if not body.llm_provider:
            row.llm_provider = detect_provider(body.api_key)
        if not body.model_name:
            row.model_name = DEFAULT_MODELS.get(row.llm_provider, "gemini-2.0-flash")

    if body.llm_provider:
        row.llm_provider = body.llm_provider
    if body.model_name:
        row.model_name = body.model_name

    session.commit()
    session.refresh(row)

    return SettingsOut(
        llm_provider=row.llm_provider,
        model_name=row.model_name,
        has_api_key=bool(row.api_key_encrypted),
        api_key=decrypt_key(row.api_key_encrypted) if row.api_key_encrypted else None,
    )


@router.post("/test")
async def test_llm(session: Session = Depends(get_session)):
    return await test_connection(session)
