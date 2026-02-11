"""Tests for AI client module."""

import pytest
from unittest.mock import Mock, patch
from src.ai_client import AIClient, AIProvider, create_ai_client


class TestAIClient:
    """Test AIClient functionality."""
    
    def test_openai_provider_initialization(self):
        """Test OpenAI provider initialization."""
        with patch('src.ai_client.OpenAI') as mock_openai:
            client = AIClient(provider="openai", api_key="test-key")
            assert client.provider == AIProvider.OPENAI
            assert client.model == "gpt-4"
            mock_openai.assert_called_once_with(api_key="test-key")
    
    def test_anthropic_provider_initialization(self):
        """Test Anthropic provider initialization."""
        with patch('src.ai_client.Anthropic') as mock_anthropic:
            client = AIClient(provider="anthropic", api_key="test-key")
            assert client.provider == AIProvider.ANTHROPIC
            assert client.model == "claude-3-sonnet-20240229"
            mock_anthropic.assert_called_once_with(api_key="test-key")
    
    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises error."""
        with pytest.raises(ValueError, match="API key required"):
            AIClient(provider="openai", api_key=None)
    
    def test_invalid_provider_raises_error(self):
        """Test that invalid provider raises error."""
        with pytest.raises(ValueError):
            AIClient(provider="invalid", api_key="test")
    
    def test_custom_model(self):
        """Test custom model specification."""
        with patch('src.ai_client.OpenAI'):
            client = AIClient(provider="openai", api_key="test", model="gpt-3.5-turbo")
            assert client.model == "gpt-3.5-turbo"
    
    def test_create_ai_client_factory(self):
        """Test factory function."""
        with patch('src.ai_client.OpenAI'):
            client = create_ai_client("openai", "test-key")
            assert isinstance(client, AIClient)
            assert client.provider == AIProvider.OPENAI
