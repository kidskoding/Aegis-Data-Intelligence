"""LangChain-based LLM service for new agents (Investigator and future)."""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from aegis.config import settings


def get_chat_model(temperature: float = 0.0) -> ChatOpenAI:
    """Create a ChatOpenAI instance with project settings.

    Lazy — does not fail if OPENAI_API_KEY is unset until the model is invoked.
    """
    return ChatOpenAI(
        model="gpt-4",
        temperature=temperature,
        api_key=settings.openai_api_key or "not-set",
    )
