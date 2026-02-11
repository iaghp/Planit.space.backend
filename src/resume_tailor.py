"""Resume tailoring module using AI."""

from pathlib import Path
from typing import Optional
import PyPDF2
from docx import Document

from src.ai_client import create_ai_client
from src.config_manager import ConfigManager


class ResumeTailor:
    """Tailors resumes to specific job descriptions using AI."""
    
    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        ai_provider: str = "openai"
    ):
        """Initialize the resume tailor.
        
        Args:
            config_manager: Config manager instance
            ai_provider: AI provider to use
        """
        self.config = config_manager or ConfigManager()
        self.ai_provider = ai_provider
    
    def tailor_resume(
        self,
        resume_path: Path,
        job_description: str,
        custom_notes: Optional[str] = None
    ) -> str:
        """Tailor a resume to a job description.
        
        Args:
            resume_path: Path to base resume file
            job_description: Job description text
            custom_notes: Additional instructions
            
        Returns:
            Tailored resume content
        """
        # Load resume content
        resume_content = self._load_resume(resume_path)
        
        # Get API key
        api_key = self.config.get_api_key(self.ai_provider)
        if not api_key:
            raise ValueError(
                f"API key not found for {self.ai_provider}. "
                f"Set {self.ai_provider.upper()}_API_KEY in your .env file."
            )
        
        # Load prompts
        prompts_config = self.config.load_prompts()
        ai_settings = prompts_config.get("ai_settings", {})
        provider_settings = ai_settings.get(self.ai_provider, {})
        
        # Create AI client
        client = create_ai_client(
            provider=self.ai_provider,
            api_key=api_key,
            model=provider_settings.get("default_model"),
            config={
                "temperature": ai_settings.get("temperature", 0.7),
                "max_tokens": ai_settings.get("max_tokens", 2000)
            }
        )
        
        # Build prompt
        system_prompt = prompts_config.get(
            "resume_tailor_system_prompt",
            "You are an expert resume writer."
        )
        
        template = prompts_config.get(
            "resume_tailor_user_template",
            "Tailor this resume for the following job:\n\nJob Description:\n{job_description}\n\nResume:\n{resume_content}"
        )
        
        user_prompt = template.format(
            job_description=job_description,
            resume_content=resume_content
        )
        
        if custom_notes:
            user_prompt += f"\n\nCustom Instructions: {custom_notes}"
        
        # Generate tailored resume
        tailored_content = client.generate(user_prompt, system_prompt)
        
        return tailored_content
    
    def _load_resume(self, path: Path) -> str:
        """Load resume content from various file formats.
        
        Args:
            path: Path to resume file
            
        Returns:
            Resume text content
        """
        suffix = path.suffix.lower()
        
        if suffix == '.pdf':
            return self._load_pdf(path)
        elif suffix in ['.docx', '.doc']:
            return self._load_docx(path)
        elif suffix == '.txt':
            return path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Unsupported resume format: {suffix}")
    
    def _load_pdf(self, path: Path) -> str:
        """Load text from PDF file."""
        text_parts = []
        
        with open(path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _load_docx(self, path: Path) -> str:
        """Load text from DOCX file."""
        doc = Document(str(path))
        
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        
        return "\n\n".join(text_parts)


def load_resume_content(source: str) -> str:
    """Load resume from file or text.
    
    Args:
        source: File path or direct text
        
    Returns:
        Resume content
    """
    path = Path(source)
    
    if path.exists() and path.is_file():
        tailor = ResumeTailor()
        return tailor._load_resume(path)
    
    # Treat as direct text
    return source
