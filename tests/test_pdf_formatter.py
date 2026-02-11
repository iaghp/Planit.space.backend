"""Tests for PDF formatter."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.pdf_formatter import PDFFormatter, generate_filename
from src.config_manager import ConfigManager


class TestPDFFormatter:
    """Test PDF formatting functionality."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock config manager."""
        config = Mock(spec=ConfigManager)
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
        
        config.load_profile.return_value = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
        
        return config
    
    def test_generate_filename(self):
        """Test filename generation."""
        filename = generate_filename("Acme Corp", "CoverLetter")
        
        assert "CoverLetter" in filename
        assert "Acme_Corp" in filename
        assert filename.endswith(".pdf")
    
    def test_generate_filename_with_special_chars(self):
        """Test filename generation with special characters."""
        filename = generate_filename("Acme & Co. (Inc.)", "Resume")
        
        assert "Acme" in filename
        assert "Resume" in filename
        # Special chars should be removed or replaced
        assert "&" not in filename
        assert "(" not in filename
    
    @patch('src.pdf_formatter.SimpleDocTemplate')
    def test_create_cover_letter_pdf(self, mock_doc, mock_config, tmp_path):
        """Test PDF creation."""
        formatter = PDFFormatter(mock_config)
        
        output_path = tmp_path / "test.pdf"
        content = "John Doe\n123 Main St\n\nDear Hiring Manager,\n\nBody text."
        
        profile = mock_config.load_profile.return_value
        
        # This will call the mocked SimpleDocTemplate
        result = formatter.create_cover_letter_pdf(
            content,
            output_path,
            "Acme Corp",
            profile
        )
        
        assert result == output_path
        mock_doc.assert_called_once()
