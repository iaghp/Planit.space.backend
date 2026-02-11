"""Tests for cover letter generation."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.cover_letter import CoverLetterGenerator, load_job_description
from src.config_manager import ConfigManager


class TestCoverLetterGenerator:
    """Test cover letter generation functionality."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock config manager."""
        config = Mock(spec=ConfigManager)
        config.load_profile.return_value = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "555-1234"
            },
            "address": {
                "street": "123 Main St",
                "city": "City",
                "state": "ST",
                "zip": "12345"
            },
            "summary": "Experienced developer",
            "skills": ["Python", "JavaScript"],
            "experience": [
                {
                    "company": "Tech Corp",
                    "role": "Engineer",
                    "duration": "2020-2024",
                    "highlights": ["Built features"]
                }
            ],
            "preferences": {
                "tone": "professional",
                "use_bullets": False,
                "closing": "Sincerely",
                "signature_name": "John Doe"
            }
        }
        
        config.load_prompts.return_value = {
            "cover_letter_system_prompt": "You are an expert.",
            "cover_letter_user_template": "Generate for {role} at {company}",
            "ai_settings": {
                "temperature": 0.7,
                "max_tokens": 2000,
                "openai": {"default_model": "gpt-4"}
            }
        }
        
        config.get_api_key.return_value = "test-key"
        
        return config
    
    @patch('src.cover_letter.create_ai_client')
    def test_generate_cover_letter(self, mock_create_client, mock_config):
        """Test cover letter generation."""
        # Setup mock AI client
        mock_client = Mock()
        mock_client.generate.return_value = "Dear Hiring Manager,\n\nI am writing..."
        mock_create_client.return_value = mock_client
        
        # Generate cover letter
        generator = CoverLetterGenerator(mock_config)
        result = generator.generate(
            job_description="We need a Python developer",
            company="Acme Corp",
            role="Software Engineer"
        )
        
        assert "I am writing" in result
        mock_client.generate.assert_called_once()
    
    @patch('src.cover_letter.create_ai_client')
    def test_generate_full_letter(self, mock_create_client, mock_config):
        """Test full letter generation with header."""
        mock_client = Mock()
        mock_client.generate.return_value = "Dear Hiring Manager,\n\nLetter body."
        mock_create_client.return_value = mock_client
        
        generator = CoverLetterGenerator(mock_config)
        result = generator.generate_full_letter(
            job_description="Job desc",
            company="Acme",
            role="Engineer"
        )
        
        assert "John Doe" in result
        assert "123 Main St" in result
        assert "Sincerely" in result
    
    def test_load_job_description_from_text(self):
        """Test loading job description from text."""
        text = "We are hiring a developer"
        result = load_job_description(text)
        assert result == text
    
    def test_load_job_description_from_file(self, tmp_path):
        """Test loading job description from file."""
        job_file = tmp_path / "job.txt"
        job_file.write_text("Job description content")
        
        result = load_job_description(str(job_file))
        assert result == "Job description content"
