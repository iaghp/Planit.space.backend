"""Unified AI client supporting OpenAI and Anthropic APIs."""

import time
from typing import Optional, Dict, Any
from enum import Enum

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AIProvider(Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class AIClient:
    """Unified AI client with support for multiple providers."""
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        max_retries: int = 3
    ):
        """Initialize the AI client.
        
        Args:
            provider: 'openai' or 'anthropic'
            api_key: API key for the provider
            model: Model name (uses default if not specified)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            max_retries: Number of retries on failure
        """
        self.provider = AIProvider(provider.lower())
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        
        # Initialize the appropriate client
        if self.provider == AIProvider.OPENAI:
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
            if not api_key:
                raise ValueError("OpenAI API key required")
            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-4"
            
        elif self.provider == AIProvider.ANTHROPIC:
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("Anthropic package not installed. Run: pip install anthropic")
            if not api_key:
                raise ValueError("Anthropic API key required")
            self.client = Anthropic(api_key=api_key)
            self.model = model or "claude-3-sonnet-20240229"
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate text using the configured AI provider.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text
            
        Raises:
            Exception: If generation fails after all retries
        """
        for attempt in range(self.max_retries):
            try:
                if self.provider == AIProvider.OPENAI:
                    return self._generate_openai(prompt, system_prompt, **kwargs)
                elif self.provider == AIProvider.ANTHROPIC:
                    return self._generate_anthropic(prompt, system_prompt, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"API call failed (attempt {attempt + 1}/{self.max_retries}). "
                      f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
        
        raise Exception("Failed to generate text after all retries")
    
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate text using OpenAI API."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens)
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate text using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            system=system_prompt or "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()


def create_ai_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> AIClient:
    """Factory function to create an AI client.
    
    Args:
        provider: 'openai' or 'anthropic'
        api_key: API key for the provider
        model: Model name (optional)
        config: Additional configuration (optional)
        
    Returns:
        Configured AIClient instance
    """
    config = config or {}
    
    return AIClient(
        provider=provider,
        api_key=api_key,
        model=model,
        temperature=config.get("temperature", 0.7),
        max_tokens=config.get("max_tokens", 2000),
        max_retries=config.get("max_retries", 3)
    )
