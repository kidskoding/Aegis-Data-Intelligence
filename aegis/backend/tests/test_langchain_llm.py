"""Tests for LangChain LLM service."""

from unittest.mock import patch

from aegis.services.langchain_llm import get_chat_model


def test_get_chat_model_returns_chatopenai():
    with patch("aegis.services.langchain_llm.settings") as mock_settings:
        mock_settings.openai_api_key = "test-key"
        model = get_chat_model()
        assert model.model_name == "gpt-4"
        assert model.temperature == 0.0


def test_get_chat_model_custom_temperature():
    with patch("aegis.services.langchain_llm.settings") as mock_settings:
        mock_settings.openai_api_key = "test-key"
        model = get_chat_model(temperature=0.7)
        assert model.temperature == 0.7
