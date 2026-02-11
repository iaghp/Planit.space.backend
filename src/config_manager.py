"""Configuration manager for loading and validating YAML configs."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from dotenv import load_dotenv


class ConfigManager:
    """Manages loading and validation of configuration files."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the config manager.
        
        Args:
            config_dir: Path to config directory. Defaults to ./config
        """
        if config_dir is None:
            # Get the project root (parent of src/)
            project_root = Path(__file__).parent.parent
            config_dir = project_root / "config"
        
        self.config_dir = Path(config_dir)
        
        # Load environment variables
        load_dotenv()
        
    def load_profile(self) -> Dict[str, Any]:
        """Load user profile configuration.
        
        Returns:
            Dictionary containing profile data
            
        Raises:
            FileNotFoundError: If profile.yaml doesn't exist
        """
        profile_path = self.config_dir / "profile.yaml"
        
        if not profile_path.exists():
            example_path = self.config_dir / "profile.yaml.example"
            raise FileNotFoundError(
                f"Profile not found at {profile_path}. "
                f"Copy {example_path} to {profile_path} and customize it."
            )
        
        with open(profile_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_style(self) -> Dict[str, Any]:
        """Load cover letter style configuration.
        
        Returns:
            Dictionary containing style preferences
        """
        style_path = self.config_dir / "cover_letter_style.yaml"
        
        if not style_path.exists():
            # Return sensible defaults
            return self._default_style()
        
        with open(style_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_prompts(self) -> Dict[str, Any]:
        """Load AI prompt templates.
        
        Returns:
            Dictionary containing prompt templates
        """
        prompts_path = self.config_dir / "prompts.yaml"
        
        if not prompts_path.exists():
            # Return defaults
            return self._default_prompts()
        
        with open(prompts_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for specified provider.
        
        Args:
            provider: 'openai' or 'anthropic'
            
        Returns:
            API key or None if not set
        """
        if provider == "openai":
            return os.getenv("OPENAI_API_KEY")
        elif provider == "anthropic":
            return os.getenv("ANTHROPIC_API_KEY")
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _default_style(self) -> Dict[str, Any]:
        """Return default style configuration."""
        return {
            "page": {"size": "letter", "orientation": "portrait"},
            "margins": {"top": 72, "bottom": 72, "left": 72, "right": 72},
            "fonts": {
                "header": {"family": "Helvetica-Bold", "size": 12},
                "body": {"family": "Helvetica", "size": 11},
                "contact": {"family": "Helvetica", "size": 10},
                "signature": {"family": "Helvetica-Oblique", "size": 12}
            },
            "spacing": {
                "line_height": 1.2,
                "paragraph_spacing": 12,
                "section_spacing": 18
            },
            "signature": {
                "use_image": False,
                "show_typed_name": True,
                "spacing_above": 24
            },
            "constraints": {
                "max_pages": 1,
                "auto_adjust_font": True,
                "min_font_size": 9
            }
        }
    
    def _default_prompts(self) -> Dict[str, Any]:
        """Return default prompt configuration."""
        return {
            "cover_letter_system_prompt": (
                "You are an expert career advisor and professional writer."
            ),
            "cover_letter_user_template": (
                "Generate a professional cover letter for {role} at {company}."
            ),
            "ai_settings": {
                "temperature": 0.7,
                "max_tokens": 2000,
                "openai": {
                    "default_model": "gpt-4",
                    "fallback_model": "gpt-3.5-turbo"
                },
                "anthropic": {
                    "default_model": "claude-3-sonnet-20240229",
                    "fallback_model": "claude-3-haiku-20240307"
                }
            }
        }
