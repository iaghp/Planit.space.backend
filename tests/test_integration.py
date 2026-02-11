"""Integration tests for the full pipeline."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.config_manager import ConfigManager
from src.cover_letter import CoverLetterGenerator
from src.pdf_formatter import PDFFormatter
from src.resume_tailor import ResumeTailor


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    @pytest.fixture
    def mock_config(self, tmp_path):
        """Create a mock config with temporary directory."""
        config = Mock(spec=ConfigManager)
        config.config_dir = tmp_path / "config"
        config.config_dir.mkdir()
        
        # Create profile
        profile = {
            "personal_info": {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "555-9876"
            },
            "address": {
                "street": "456 Oak Ave",
                "city": "Portland",
                "state": "OR",
                "zip": "97201"
            },
            "summary": "Experienced software engineer",
            "skills": ["Python", "React", "AWS"],
            "experience": [
                {
                    "company": "Tech Startup",
                    "role": "Senior Engineer",
                    "duration": "2019-2024",
                    "highlights": ["Led backend team", "Improved performance by 50%"]
                }
            ],
            "preferences": {
                "tone": "professional",
                "use_bullets": False,
                "closing": "Best regards",
                "signature_name": "Jane Smith"
            }
        }
        
        config.load_profile.return_value = profile
        config.load_style.return_value = {
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
        
        config.load_prompts.return_value = {
            "cover_letter_system_prompt": "You are an expert writer.",
            "cover_letter_user_template": "Generate cover letter for {role} at {company}",
            "resume_tailor_system_prompt": "You are a resume expert.",
            "resume_tailor_user_template": "Tailor resume:\n{resume_content}",
            "ai_settings": {
                "temperature": 0.7,
                "max_tokens": 2000,
                "openai": {"default_model": "gpt-4"},
                "anthropic": {"default_model": "claude-3-sonnet-20240229"}
            }
        }
        
        config.get_api_key.return_value = "test-api-key"
        
        return config
    
    @patch('src.cover_letter.create_ai_client')
    @patch('src.pdf_formatter.SimpleDocTemplate')
    def test_cover_letter_generation_workflow(
        self,
        mock_doc,
        mock_create_client,
        mock_config,
        tmp_path
    ):
        """Test the complete cover letter generation workflow."""
        # Mock AI client
        mock_client = Mock()
        mock_client.generate.return_value = (
            "Dear Hiring Manager,\n\n"
            "I am excited to apply for the Software Engineer position at Acme Corp. "
            "With my extensive experience in Python and React, I am confident I can contribute.\n\n"
            "Best regards"
        )
        mock_create_client.return_value = mock_client
        
        # Generate cover letter
        generator = CoverLetterGenerator(mock_config)
        content = generator.generate_full_letter(
            job_description="We need a Python developer with React experience",
            company="Acme Corp",
            role="Software Engineer",
            custom_notes="Emphasize leadership skills"
        )
        
        # Verify content
        assert "Jane Smith" in content
        assert "456 Oak Ave" in content
        assert "Dear Hiring Manager" in content
        assert "Best regards" in content
        
        # Create PDF
        formatter = PDFFormatter(mock_config)
        output_path = tmp_path / "cover_letter.pdf"
        
        result = formatter.create_cover_letter_pdf(
            content,
            output_path,
            "Acme Corp",
            mock_config.load_profile.return_value
        )
        
        assert result == output_path
        mock_doc.assert_called_once()
    
    @patch('src.resume_tailor.create_ai_client')
    def test_resume_tailoring_workflow(
        self,
        mock_create_client,
        mock_config,
        tmp_path
    ):
        """Test the resume tailoring workflow."""
        # Create a sample resume file
        resume_path = tmp_path / "resume.txt"
        resume_path.write_text(
            "Jane Smith\n"
            "Software Engineer\n\n"
            "Experience:\n"
            "- Tech Startup: Senior Engineer (2019-2024)\n"
            "- Built microservices with Python\n"
            "- Led team of 5 engineers"
        )
        
        # Mock AI client
        mock_client = Mock()
        mock_client.generate.return_value = (
            "Jane Smith\n"
            "Senior Software Engineer\n\n"
            "Tailored Experience:\n"
            "- Tech Startup: Senior Engineer (2019-2024)\n"
            "- Architected and built microservices platform using Python and AWS\n"
            "- Led cross-functional team of 5 engineers, mentoring junior developers"
        )
        mock_create_client.return_value = mock_client
        
        # Tailor resume
        tailor = ResumeTailor(mock_config)
        tailored = tailor.tailor_resume(
            resume_path,
            job_description="Looking for a Senior Software Engineer with Python and AWS experience",
            custom_notes="Emphasize leadership"
        )
        
        # Verify tailored content
        assert "Jane Smith" in tailored
        assert "Python and AWS" in tailored
        assert "Led cross-functional team" in tailored
        
        # Verify AI was called
        mock_client.generate.assert_called_once()
        call_args = mock_client.generate.call_args
        # The prompt should contain both the resume content and job description
        assert "Jane Smith" in call_args[0][0]
        assert "Emphasize leadership" in call_args[0][0]
    
    def test_config_manager_loads_correctly(self, tmp_path):
        """Test that ConfigManager loads configuration files."""
        # Create config directory with profile
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        profile_path = config_dir / "profile.yaml"
        profile_path.write_text("""
personal_info:
  name: "Test User"
  email: "test@example.com"
  phone: "555-1234"
address:
  street: "123 Test St"
  city: "Test City"
  state: "TS"
  zip: "12345"
preferences:
  tone: "professional"
        """)
        
        # Load config
        config = ConfigManager(config_dir)
        profile = config.load_profile()
        
        assert profile["personal_info"]["name"] == "Test User"
        assert profile["personal_info"]["email"] == "test@example.com"
        assert profile["address"]["city"] == "Test City"
        assert profile["preferences"]["tone"] == "professional"
