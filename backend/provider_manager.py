"""Multi-provider LLM abstraction via Pydantic AI."""

from __future__ import annotations

from pydantic_ai import Agent
from sqlmodel import Session, select

from backend.database import AppSettings, get_session
from backend.encryption import decrypt_key

# Provider → default model mapping
DEFAULT_MODELS: dict[str, str] = {
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-5.4-mini",
    "anthropic": "claude-sonnet-4-6",
}

MODEL_OPTIONS: dict[str, list[str]] = {
    "gemini": [
        "gemini-3.1-pro-preview",
        "gemini-3-flash-preview",
        "gemini-3.1-flash-lite-preview",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    "openai": [
        "gpt-5.4",
        "gpt-5.4-mini",
    ],
    "anthropic": [
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        "claude-haiku-4-5-20251001",
    ],
}


def detect_provider(api_key: str) -> str:
    """Best-guess provider from API key prefix."""
    if api_key.startswith("sk-ant-"):
        return "anthropic"
    if api_key.startswith("sk-"):
        return "openai"
    return "gemini"


def _pydantic_model_name(provider: str, model: str) -> str:
    """Return the model string Pydantic AI expects."""
    prefix_map = {"gemini": "google-gla", "openai": "openai", "anthropic": "anthropic"}
    prefix = prefix_map.get(provider, provider)
    return f"{prefix}:{model}"


def _env_var_for_provider(provider: str) -> str:
    return {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }[provider]


def load_settings(session: Session) -> AppSettings | None:
    return session.exec(select(AppSettings)).first()


def get_agent(
    system_prompt: str,
    output_type=str,
    session: Session | None = None,
    tools: list | None = None,
) -> Agent:
    """Build a Pydantic AI Agent from the stored settings."""
    import os

    own_session = session is None
    if own_session:
        session = next(get_session())

    settings = load_settings(session)
    if not settings or not settings.api_key_encrypted:
        raise RuntimeError("No LLM provider configured — visit /setup first.")

    api_key = decrypt_key(settings.api_key_encrypted)
    provider = settings.llm_provider
    model = settings.model_name

    # Set the env var Pydantic AI expects
    os.environ[_env_var_for_provider(provider)] = api_key

    model_name = _pydantic_model_name(provider, model)

    agent = Agent(
        model_name,
        system_prompt=system_prompt,
        output_type=result_type,
    )
    if tools:
        for tool in tools:
            agent.tool_plain(tool)

    return agent


async def test_connection(session: Session) -> dict:
    """Quick smoke test: send a trivial prompt and see if we get a response."""
    try:
        agent = get_agent("You are a helpful assistant.", session=session)
        result = await agent.run("Say 'OK' and nothing else.")
        return {"success": True, "message": result.output}
    except Exception as e:
        return {"success": False, "message": str(e)}
