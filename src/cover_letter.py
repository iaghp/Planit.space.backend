"""Cover letter generation module."""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from src.ai_client import create_ai_client
from src.config_manager import ConfigManager


class CoverLetterGenerator:
    """Generates personalized cover letters using AI."""
    
    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        ai_provider: str = "openai"
    ):
        """Initialize the cover letter generator.
        
        Args:
            config_manager: Config manager instance
            ai_provider: AI provider to use ('openai' or 'anthropic')
        """
        self.config = config_manager or ConfigManager()
        self.ai_provider = ai_provider
        
    def generate(
        self,
        job_description: str,
        company: str,
        role: str,
        custom_notes: Optional[str] = None,
        hiring_manager: Optional[str] = None
    ) -> str:
        """Generate a cover letter.
        
        Args:
            job_description: Job description text
            company: Company name
            role: Job title
            custom_notes: Custom instructions for the AI
            hiring_manager: Hiring manager name (optional)
            
        Returns:
            Generated cover letter content (body only, without header/signature)
        """
        # Load configuration
        profile = self.config.load_profile()
        prompts_config = self.config.load_prompts()
        
        # Get API key
        api_key = self.config.get_api_key(self.ai_provider)
        if not api_key:
            raise ValueError(
                f"API key not found for {self.ai_provider}. "
                f"Set {self.ai_provider.upper()}_API_KEY in your .env file."
            )
        
        # Create AI client
        ai_settings = prompts_config.get("ai_settings", {})
        provider_settings = ai_settings.get(self.ai_provider, {})
        
        client = create_ai_client(
            provider=self.ai_provider,
            api_key=api_key,
            model=provider_settings.get("default_model"),
            config={
                "temperature": ai_settings.get("temperature", 0.7),
                "max_tokens": ai_settings.get("max_tokens", 2000)
            }
        )
        
        # Prepare profile information
        profile_info = self._format_profile_info(profile)
        experience_info = self._format_experience(profile.get("experience", []))
        
        # Get preferences
        prefs = profile.get("preferences", {})
        tone = prefs.get("tone", "professional")
        use_bullets = prefs.get("use_bullets", False)
        
        # Build prompt
        system_prompt = prompts_config.get(
            "cover_letter_system_prompt",
            "You are an expert career advisor and professional writer."
        )
        
        template = prompts_config.get(
            "cover_letter_user_template",
            "Generate a professional cover letter for {role} at {company}."
        )
        
        # Format the user prompt
        user_prompt = template.format(
            role=role,
            company=company,
            job_description=job_description,
            name=profile["personal_info"]["name"],
            profile_summary=profile.get("summary", ""),
            experience=experience_info,
            custom_notes=custom_notes or "None",
            tone=tone,
            use_bullets="Yes" if use_bullets else "No"
        )
        
        if hiring_manager:
            user_prompt += f"\n\nNote: Address the letter to {hiring_manager}."
        
        # Generate cover letter
        content = client.generate(user_prompt, system_prompt)
        
        return content
    
    def generate_full_letter(
        self,
        job_description: str,
        company: str,
        role: str,
        custom_notes: Optional[str] = None,
        hiring_manager: Optional[str] = None
    ) -> str:
        """Generate a complete cover letter with header and signature.
        
        Args:
            job_description: Job description text
            company: Company name
            role: Job title
            custom_notes: Custom instructions
            hiring_manager: Hiring manager name
            
        Returns:
            Complete cover letter text
        """
        profile = self.config.load_profile()
        
        # Generate the body
        body = self.generate(
            job_description,
            company,
            role,
            custom_notes,
            hiring_manager
        )
        
        # Build header
        personal_info = profile["personal_info"]
        address = profile.get("address", {})
        
        header_lines = [
            personal_info["name"],
            f"{address.get('street', '')}",
            f"{address.get('city', '')}, {address.get('state', '')} {address.get('zip', '')}",
            personal_info.get("phone", ""),
            personal_info.get("email", ""),
        ]
        
        header = "\n".join(line for line in header_lines if line.strip())
        
        # Add date
        date_str = datetime.now().strftime("%B %d, %Y")
        
        # Build complete letter
        prefs = profile.get("preferences", {})
        closing = prefs.get("closing", "Sincerely")
        signature_name = prefs.get("signature_name", personal_info["name"])
        
        full_letter = f"{header}\n\n{date_str}\n\n{body}\n\n{closing},\n\n{signature_name}"
        
        return full_letter
    
    def _format_profile_info(self, profile: Dict[str, Any]) -> str:
        """Format profile information for the AI."""
        info_parts = []
        
        if "summary" in profile:
            info_parts.append(f"Summary: {profile['summary']}")
        
        if "skills" in profile:
            skills_str = ", ".join(profile["skills"])
            info_parts.append(f"Skills: {skills_str}")
        
        return "\n".join(info_parts)
    
    def _format_experience(self, experiences: list) -> str:
        """Format work experience for the AI."""
        if not experiences:
            return "No experience provided"
        
        exp_parts = []
        for exp in experiences:
            exp_str = f"{exp['role']} at {exp['company']} ({exp['duration']})"
            if "highlights" in exp:
                highlights = "\n  - ".join(exp["highlights"])
                exp_str += f"\n  - {highlights}"
            exp_parts.append(exp_str)
        
        return "\n\n".join(exp_parts)


def load_job_description(source: str) -> str:
    """Load job description from text or file.
    
    Args:
        source: Either direct text or a file path
        
    Returns:
        Job description text
    """
    # Check if it's a file path
    path = Path(source)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    
    # Otherwise, treat as direct text
    return source
